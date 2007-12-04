# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core.cache import cache

import phoenix, simplejson
import os, md5, commands, pprint
from tempfile import mkstemp

def generate_graphviz(graph):
	dotput = "digraph test { \n"
	for parse in graph:
		framenum = 0
		for frame in parse:
			dotput += "%s -> %s%d;\n" % (frame['name'], frame['name'], framenum)
			last_node_name = None
			for node in frame['nodes']:
				if len(node['name']) > 0:
					last_node_name = node['name'][0]
					dotput += "%s%d -> %s;\n" % (frame['name'], framenum, node['name'][0])
					dotput += "%s -> %s;\n" % (node['name'][0], node['value'])
				else:
					dotput += "%s%d -> %s;\n" % (frame['name'], framenum, last_node_name)
					dotput += "%s -> %s;\n" % (last_node_name, node['value'])
					#dotput += "%s%d -> %s;\n" % (frame['name'], framenum, node['value'])
			framenum += 1
	dotput += "}"
	return dotput

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
		question = request.POST.get('question').replace("'s", "")
		key = md5.new(question).hexdigest()
		parse = phoenix.parse(question, dir="nlu/lib/Phoenix/FamilyGrammar", net="REL.net")
		cache.set(key, parse, 60*60)
		return render_to_response('ask.html', 
			{'message':pprint.pformat(parse), 'key':key,
			 'payload':simplejson.dumps(parse), 'question':request.POST.get('question','')}
		)
		
def refresh_grammar(request):
	
	from dman.models import Person
	import commands
	people = [x['name'] for x in Person.objects.all().values('name')]
	name_file = open('nlu/lib/Phoenix/FamilyGrammar/names','w')

	for p in people:
		name_file.write('\t(%s)\n' % p.lower())

	name_file.write("""	(his)
	(him)
	(her)
	(hers)
	(they)
	(them)
	(their)""")
	name_file.close()

	(stat, output) = commands.getstatusoutput('tcsh nlu/lib/Phoenix/FamilyGrammar/compile')
	return HttpResponse(output)