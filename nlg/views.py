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
	#build up dictionaries of our request data
	context = response[1]
	main = response[0]
	contextNodes = dict([(x['id'], x) for x in context["result"]])
	mainNodes = dict([(x['id'], x) for x in main["result"]])
	templateNodes = _mergeContext(contextNodes,mainNodes)
	textOutput = render_to_string(templateName, {"main":mainNodes, "context":contextNodes})
	#clean up text output
	textOutput = textOutput.replace("\n", "").replace("\t","")
	voiceOutput = _voiceOutput(textOutput)
	graphvizOutput = _graphvizBuild(context, main, contextNodes, mainNodes)
	#graphvizOutput = render_to_string(templateName+".dot", {"response":response})
	htmlTemplateData = {"stringOutput":textOutput, "graph":graphvizOutput}
	return render_to_response("output.html", {"data":htmlTemplateData})
	

def _voiceOutput(textOutput):
	"""
	Generates voice output locally on the system. As of now, this is system dependent
	and requires OS X. It works with both tiger (10.4) and leopard (10.5), but sounds
	much better with leopard and the new "alex" voice
	"""
	print "Saying voice output: " + textOutput
	commands.getstatusoutput('say "%s"' % (textOutput))
	

def _mergeContext(contextNodes, mainNodes):
	"""
	Takes the context nodes (which contain detailed information about each person) and 
	the main nodes, which contains just the result of the query with IDs, to be looked 
	up in the context, and populates it with the necessary data for the text based
	template matching
	"""

	#	for node in mainNodes["subject"].iteritems()
	pass
	
def _graphvizBuild(context, main, contextNodes, mainNodes):
	"""
	Generates a graphviz template string for our request
	It will fill out a graph of the entirety of the request, but color in the referenced
	nodes a certain color based on the relationship
	"""
	graphvizString = "digraph " + context["action"] +	" {\n"
	for node in context["result"]:
		# build the style definition for the current node
		if mainNodes.get(node["id"]) == None:
			graphvizString += "\t" + node["title"] + " [style=filled fillcolor=black fontcolor=white]\n"
		else:
			graphvizString += "\t" + node["title"]
			if node["gender"] == 'M':
				graphvizString += " [style=filled fillcolor=\"#80C9FF\" fontcolor=white]\n"
			else: 
				graphvizString += " [style=filled fillcolor=\"#FF80B8\" fontcolor=white]\n"
		for spouse in node["spouse"]:
			if node["gender"] == 'M':
				spouseNodeName = node["title"]+"_"+contextNodes[spouse]["title"]
				spouseLabel = node["title"] + " & " + contextNodes[spouse]["title"]
			else:
				spouseNodeName= contextNodes[spouse]["title"] + "_" + node["title"]
				spouseLabel = contextNodes[spouse]["title"] + " & " + node["title"]
			graphvizString += "\t" + node["title"] + " -> " + spouseNodeName + "\n"
			graphvizString += "\t" + spouseNodeName + "[label=\"" + spouseLabel + "\" style=filled fillcolor=gray fontcolor=white]\n"
		if node.get("mother") != None and node.get("father") != None:
			# build a parent node, and a parent -> son relationship
			graphvizString += "\t" + contextNodes[node["father"]]["title"] + "_" + contextNodes[node["mother"]]["title"]
			graphvizString += " -> " + node["title"] +"\n"
		else:
			if node.get("mother") != None:
				# build the mother -> son relationship
				graphvizString += "\t" + contextNodes[node["mother"]]["title"] + " -> " + node["title"] +"\n"
			if node.get("father") != None:
				# build the father -> son relationship
				graphvizString += "\t" + contextNodes[node["father"]]["title"] + " -> " + node["title"] +"\n"
	
	graphvizString += "\n}"
	print graphvizString
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

