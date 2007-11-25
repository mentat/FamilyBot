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

def understand_relation(parse):
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
		
	return get_data(operator, values, relation)
		
def get_data(operator, values, relation):
	
	# Build list of subjects
	subject = Person.objects.none()
	for val in values['Person_Name']:
		subject |= Person.objects.filter(name__iexact=val)
		
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
		greats = relation.count('grand') + relation.count('great') + 1
		data = get_greats(list(subject), greats, Person.children)
	elif relation.startswith('son'):
		data = Person.objects.filter(id__in=reduce(
			lambda x,y: operator(x, y),
			[set([y['id'] for y in x.sons().values('id')]) for x in subject])
		)
	elif relation.startswith('brother'):
		data = set(x['id'] for x in subject[0].father.sons().values('id')) - set([x.id for x in subject])
		data = Person.objects.filter(id__in=data)
		
	elif relation.startswith('daughter'):
		data = subject[0].daughters()
	else:
		return HttpResponse('I do not understand that relation (%s).' % relation)
	
	if len(data)==0:
		return HttpResponse('I cannot find that data.')
		
	return render_to_response('data.html', {'subject':subject, 'data':data, 'values':values})
	
def load(request, subject, relation):
	# A more direct inferface to the DMAN
	
	return get_data(set.intersection, {'Person_Name':[subject]}, relation)
	
def understand(request):
	# Understand a message from the NLU
	
	try:
		instance = simplejson.loads(request['payload'])
	except KeyError:
		return HttpResponse("Invalid Arguments")
		
	for parse in instance:
		if parse[0]['name']=='Relation':
			return understand_relation(parse)
	
