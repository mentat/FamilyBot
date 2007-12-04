import simplejson

from django.test.client import Client
from django.test import TestCase

class TemplateTest(TestCase):
	def testGenerateTemplate(self):
		client = Client()
		jsonRequest = simplejson.dumps(CHILDREN_JSON_REQUEST)
		testResponse = client.get('/generate/',{'payload':jsonRequest})
		self.assertEquals(testResponse.status_code, 200)
		#print testResponse
			
CHILDREN_JSON_REQUEST = 		{
			"actions": [
				{
					"type":"output",
					"action":"children",
					"subject": {"id":[1] },
					"result": [
						{"id":3 },{"id":4 },{"id":5 }
					]
				}, 
				{
					"type":"context",
					"action":"son",
					"subject": {"id":[1]},
					"result":[ 
						{"id":3, 
						"title":"Cain", 
						"mother":2,  
						"father":1, 
						"spouse":[], 
						"gender":"M"},

						{"id":4, 
						"title":"Abel", 
						"mother":2,  
						"father":1, 
						"spouse":[], 
						"gender":"M"},

						{"id":5, 
						"title":"Seth", 
						"mother":2,  
						"father":1, 
						"spouse":[], 
						"gender":"M"},

						{"id":1, 
						"title":"Adam",  "spouse":[2], 
						"gender":"M"},
						
						{"id":2,
						 "title":"Eve", "spouse":[1],
						"gender":"F"}
						
						

					]
				}

			]
		}

