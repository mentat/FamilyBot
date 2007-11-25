from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q

import simplejson

from models import Person

def understand_relation(parse):
	# Relation: required nodes: Relation_Type, Person_Name
	
	required = set(['Relation_Type', 'Person_Name'])
	available = set()
	values = dict()
	for frame in parse:
		for node in frame['nodes']:
			print node
			available.add(node['name'][0])
			values[node['name'][0]]=node['value']
		
	if available != required:
		return HttpResponse("I'm missing %s." % ", ".join(required-available))
	
	relation = values['Relation_Type'].lower()
	subject = Person.objects.get(name__iexact=values['Person_Name'])
	
	if relation=='father':	
		data = [subject.father]
	elif relation=='mother':
		data = [subject.mother]
	elif relation=='wife':
		data = subject.spouses.filter(gender='F')
	elif relation=='husband':
		data = subject.spouses.filter(gender='M')
	elif relation.startswith('child'):
		data = subject.children()
	elif relation.startswith('son'):
		data = subject.sons()
	elif relation.startswith('daughter'):
		data = subject.daughters()
		
	return render_to_response('data.html', {'subject':subject, 'data':data, 'values':values})
	
def understand(request):
	# Understand a message from the NLU
	
	try:
		instance = simplejson.loads(request['payload'])
	except KeyError:
		return HttpResponse("Invalid Arguments")
		
	for parse in instance:
		if parse[0]['name']=='Relation':
			return understand_relation(parse)
	
