import simplejson, re

def _processChildrenTemplate(response):
	template = "NAME has the children CHILD"
	name = re.compile(r'NAME')
	template = name.sub(response["subject"]["title"],template)
	childList = ", ".join([x['title'] for x in response["result"]])
	children = re.compile(r'CHILD')
	template = children.sub(childList,template)
	return template

TEMPLATES = { 
	"children":_processChildrenTemplate,
	 }
