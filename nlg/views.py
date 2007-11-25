import simplejson, re
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

import os, md5, commands, pprint
from tempfile import mkstemp

def generate(request):
	languageResponse = simplejson.loads(request["payload"])
	response = _processTemplate(languageResponse["actions"][0]["action"],languageResponse["actions"][0])
	return response

def _processTemplate(templateName, response):
	textOutput = render_to_string(templateName, {"response":response})
	graphvizOutput = render_to_string(templateName+".dot", {"response":response})
	htmlTemplateData = {"stringOutput":textOutput.strip(), "graph":graphvizOutput}
	return render_to_response("output.html", {"data":htmlTemplateData})
	
def generateGraphvizFile(request):
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

