from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.db.models import Q

import simplejson

from models import Person

FRAMES = [
	{
		'name':'father',
		'aliases': ['sire'],
		'max_cardinality': 1,
		'query': lambda subject: set([x.father.id for x in subject]),
		'errors': {
			'cardinality':'They do not share a common father.',
			'subject':'I do not know who %s {{%s|length|pluralize:"is,are"}}.',
			'no_data':'%s {{%s|length|pluralize:"has,have"}} no father.'
		},
	},
	{
		'name':'son',
		'aliases': ['sons'],
		'max_cardinality': None,
		'query': lambda subject: [set([y['id'] for y in x.sons().values('id')]) for x in subject],
		'errors': {
			'subject':'I do not know who %s {{%s|length|pluralize:"is,are"}}.',
			'no_data':'%s {{%s|length|pluralize:"has,have"}} no sons.'
		},
	}
]

def get_greats(subject, count, model):
	# Resolve greats
	if count==0:
		return [subject]
	data = []
	if type(subject)==list:
		for x in subject:
			for y in model(x):
				data += get_greats(y, count-1, model)
	else:
		for y in model(subject):
			data += get_greats(y, count-1, model)
	return data

def understand_relation(request, parse):
	# Relation: required nodes: Relation_Type, Person_Name
	
	required = set(['Relation_Type', 'Person_Name'])
	available = set()
	values = dict()
	for frame in parse:
		last_node_name = ''
		for node in frame['nodes']:
			
			if len(node['name']) > 0:
				last_node_name = node['name'][0]
			available.add(last_node_name)
			if last_node_name in values:
				values[last_node_name].append(node['value'])
			else:
				values[last_node_name]=[node['value']]
		
	if available != required:
		return HttpResponse("I'm missing %s." % ", ".join(required-available))

	relation = " ".join(x.lower() for x in values['Relation_Type'])
	
	# If subjects are anded--use intersection
	subject_and = True
	if subject_and is True:
		operator = set.intersection
	else:
		operator = set.union
		
	return generate_genealogy(request, operator, values, relation)
	
def _check_context(request, relation, what):
	" Check the current context for a subject for anaphora resolution. ."
	if request.session.get('context') is None:
		return Person.objects.none()
		
	context = request.session['context']
	
	def find_in_context(plural=False, male=True):
		print "Context is %s" % context
		for x in context:
			# Todo: remember same query--not needed now
			#if not x['name'].lower() == relation.lower():
			#	continue
			genders = [y['gender'] for y in x['subject']]
			print genders
			if not plural and male and len(genders)==1 and 'M' in genders:
				print "Male match"
				return Person.objects.filter(id__in=[y['id'] for y in x['subject']])
			if not plural and not male and len(genders)==1 and 'F' in genders:
				return Person.objects.filter(id__in=[y['id'] for y in x['subject']])
			if plural and len(genders)>1:
				return Person.objects.filter(id__in=[y['id'] for y in x['subject']])
			else:
				return Person.objects.none()

	if what in ['him','his']:
		return find_in_context() # sexist call
	elif what in ['her','hers']:
		return find_in_context(male=False)
	elif what in ['they','their','them']:
		return find_in_context(male=False, )

def generate_genealogy(request, operator, values, relation):
	" Get the data for the response based on relation, subject, and op. "
	# Build list of subjects
	subject = Person.objects.none()
	subject_strings = []
	for val in values['Person_Name']:
		subject_strings.append(val.lower())
		if val.lower() in ['his','him','her','they','their','them']:
			subject |= _check_context(request,relation,val.lower())
		else:
			subject |= Person.objects.filter(name__iexact=val)
			
	# Check if we just dont know who this is.
	if subject.count() == 0:
		return HttpResponse(u"I do not know who '%s' is." % (" ".join(subject_strings)) )
		
	if relation=='father':	
		data = set([x.father.id for x in subject if x.father is not None])
		if len(data)!=1:
			return HttpResponse(u"They do not share a common father.")
		data = Person.objects.filter(id__in=data)
	elif relation=='mother':
		data = [x.mother for x in subject]
	elif relation=='wife':
		data = subject[0].spouses.filter(gender='F')
	elif relation=='husband':
		data = subject[0].spouses.filter(gender='M')
	elif relation.startswith('child'):
		data = subject[0].children()
	elif relation.find('grand') != -1 or relation.find('great') != -1:
		# handle grands/greats
		greats = relation.count('grand') + relation.count('great') + 1
		if relation.find('child') != -1 or relation.find('son') != -1:
			data = get_greats(list(subject), greats, Person.children)
		elif relation.find('father') != -1 or relation.find('dad') != -1:
			data = get_greats(list(subject), greats, Person.fathers)
			
	elif relation.startswith('son'):
		data = Person.objects.filter(id__in=reduce(
			lambda x,y: operator(x, y),
			[set([y['id'] for y in x.sons().values('id')]) for x in subject])
		)
	elif relation.startswith('brother'):
		data = set(x['id'] for x in subject[0].father.sons().values('id')) - set([x.id for x in subject])
		data = Person.objects.filter(id__in=data)
	elif relation.startswith('sister'):
		data = set(x['id'] for x in subject[0].father.daughters().values('id')) - set([x.id for x in subject])
		data = Person.objects.filter(id__in=data)	
	elif relation.startswith('daughter'):
		data = subject[0].daughters()
	else:
		return HttpResponse('I do not understand that relation (%s).' % relation)
	
	if len(data)==0:
		return HttpResponse('I cannot find that data.')
		
	actions = [{'name':relation , 'subject':subject, 'data':data, 'context':list(data) + list(subject)}]
	
	if request.session.get('context') is None:
		request.session['context'] = [{'name':relation, 'subject':[s.get_values() for s in subject]}]
	else:
		session_context = request.session['context']
		session_context.insert(0, {'name':relation, 'subject':[s.get_values() for s in subject]})
		request.session['context'] = session_context
	
	return render_to_response('data.json', {'actions':actions}, mimetype='text/json')
	
def load(request, subject, relation):
	# A more direct inferface to the DMAN
	return generate_genealogy(request, set.intersection, {'Person_Name':[subject]}, relation)
	
def context(request):
	if request.session.get('context') is None:
		return HttpResponse('{}')
	else:
		try:
			return HttpResponse(simplejson.dumps(request.session['context']))
		except:
			del request.session['context']
			return HttpResponse('{}')
	
def understand(request):
	# Understand a message from the NLU
	
	try:
		instance = simplejson.loads(request['payload'])
	except KeyError:
		return HttpResponse("Invalid Arguments")
		
	for parse in instance:
		if parse[0]['name']=='Relation':
			return understand_relation(request, parse)
	
	