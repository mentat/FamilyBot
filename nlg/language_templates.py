import simplejson, re
from django.shortcuts import render_to_response

def _processChildrenTemplate(response):
	template = "NAME has the children CHILD"
	name = re.compile(r'NAME')
	template = name.sub(response["subject"]["title"],template)
	childList = ", ".join([x['title'] for x in response["result"]])
	children = re.compile(r'CHILD')
	template = children.sub(childList,template)
	graphviz = render_to_response("graphviz.dot", {"response":response})
	print graphviz
	return template

TEMPLATES = { 
	"children":_processChildrenTemplate,
	 }
