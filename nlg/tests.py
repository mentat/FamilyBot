import simplejson

from django.test.client import Client
from django.test import TestCase

class TemplateTest(TestCase):
	def testGenerateTemplate(self):
		client = Client()
		jsonRequest = simplejson.dumps(CHILDREN_JSON_REQUEST)
		testResponse = client.get('/generate/',{'payload':jsonRequest})
		self.assertEquals(testResponse.status_code, 200)
		print testResponse
			
CHILDREN_JSON_REQUEST = {
		'actions': [
			{
				'type':'output',
				'action':'children',
				'subject': {'id':1234, 'title':'mike'},
				'result': [
					{'id':333, 'title':'ann', 'gender':'F'}, {'id':334,'title':'jimmy', 'gender':'M'}
				]
			},
			{
				'type':'context',
				'action':'children',
				'subject': {'id':1234, 'title':'mike'},
				'result':[
					{'id':333, 'title':'ann','gender':'F', 'parent':1234},
					{'id':334,'title':'jimmy', 'gender':'M', 'parent':1234}
				]
			}
		]
	}
