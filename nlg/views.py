import simplejson, re
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

import os, md5, commands, pprint
from tempfile import mkstemp

def generate(request):
	languageResponse = simplejson.loads(request["payload"])
	response = _processTemplate(languageResponse["actions"][0]["action"],languageResponse["actions"])
	return response

def _processTemplate(templateName, response):
	"""
	Processes a template based on our request
	This is a two part process: first, we generate the natural language associated 
	with the answer for the request. We use thd django templating system for this, 
	based on the name of the relationship queried.
	Next, we generate the graphviz output for our request.
	"""
	textOutput = render_to_string(templateName, {"response":response[0]})
	graphvizOutput = _graphvizBuild({"response":response})
	#graphvizOutput = render_to_string(templateName+".dot", {"response":response})
	htmlTemplateData = {"stringOutput":textOutput.strip(), "graph":graphvizOutput}
	return render_to_response("output.html", {"data":htmlTemplateData})
	
def _graphvizBuild(response):
	"""
	Generates a graphviz template string for our request
	It will fill out a graph of the entirety of the request, but color in the referenced
	nodes a certain color based on the relationship
	"""
	context = response[1]
	main = response[0]
	contextNodes = dict([(x['id', x) for x in context["result"]])
	mainNodes = dict([(x['id', x) for x in main["result"]])
	graphvizString += "digraph " + context["action"] +	" {\n"
	
	for node in context["result"]:
		# build the style definition for the current node
		if main.get[node["id"]] == null:
			graphvizString += "\t" + node["title"] + " [style=filled fillcolor=black fontcolor=white]"
		else:
			graphvizString += "\t" + node["title"]
			if node["gender"] == 'M':
				graphvizString += " [style=filled fillcolor=\"#80C9FF\" fontcolor=white]\n"
			else: 
				graphvizString += " [style=filled fillcolor=\"#FF80B8\" fontcolor=white]\n"
		if node.get["mother"] != null:
			# build the mother -> son relationship
			graphvizString += "\t" + contextNodes[node["mother"]] + " -> " node["title"] +"\n"
		if node.get["father"] != null:
			# build the father -> son relationship
			graphvizString += "\t" + contextNodes[node["father"]] + " -> " node["title"] +"\n"
	
	graphvizString += "\n}"
	return graphvizString
			
	
def generateGraphvizFile(response):
	"""
	Generates a grapvhiz template file for use in our web application response.
	The actual parsing of the data for graphviz generation is already done at this 
	point, so we are simply creating a temporary file to send to the web browser
	"""
	tmpdot, dot_filename = mkstemp()
	tmppng, png_filename = mkstemp()

	dotf = open(dot_filename, 'w')
	dotf.write(request['graphviz'])
	dotf.close()

	commands.getstatusoutput('dot -Tpng -o %s %s' % (png_filename, dot_filename))

	fout = open(png_filename, 'rb')
	png = fout.read()
	fout.close()

	os.remove(png_filename)
	os.remove(dot_filename)

	return HttpResponse(content=png, mimetype='image/png')

