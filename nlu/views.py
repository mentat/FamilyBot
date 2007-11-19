# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core.cache import cache

import phoenix
import os, md5, commands
from tempfile import mkstemp

def generate_graphviz(graph):
	return """
	digraph test { one -> two; one -> three; three->four; }
	"""

def graph(request, key):
	graph = cache.get(key)
	if graph is None:
		raise Http404()
		
	dot = generate_graphviz(graph)
	tmpdot, dot_filename = mkstemp()
	tmppng, png_filename = mkstemp()
	
	dotf = open(dot_filename, 'w')
	dotf.write(dot)
	dotf.close()
	
	commands.getstatusoutput('dot -Tpng -o %s %s' % (png_filename, dot_filename))

	fout = open(png_filename, 'rb')
	png = fout.read()
	fout.close()

	os.remove(png_filename)
	os.remove(dot_filename)

	return HttpResponse(content=png, mimetype='image/png')

def ask(request):
	if request.method=='GET':
		return render_to_response('ask.html')
	else:
		question = request.POST.get('question')
		key = md5.new(question).hexdigest()
		parse = phoenix.parse(question)
		cache.set(key, parse, 60*60)
		return render_to_response('ask.html', {'message':parse, 'key':key})