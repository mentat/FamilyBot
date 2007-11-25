from django.shortcuts import render_to_response
from django.http import HttpResponse

import simplejson

def understand_relation(parse):
	# Relation: required nodes: Relation_Type, Person_Name
	
	required = set(['Relation_Type', 'Person_Name'])
	available = set()
	values = dict()
	for node in parse:
		available.append(node['name'])
		values[node['name']]=node['value']
	if available != required:
		return HttpResponse("I'm missing %s." % ", ".join(required-available))
	
def understand(request):
	# Understand a message from the NLU
	
	try:
		instance = simplejson.loads(request['payload'])
	except KeyError:
		return HttpResponse("Invalid Arguments")
		
	for parse in instance:
		if parse[0]['name']=='Relation':
			return understand_relation(parse)
	
