from django.test.client import Client
from django.test import TestCase

class ManagerTest(TestCase):
	
	def testModels(self):
		from familybot.dman.models import Person
		
		tim = Person.objects.create(name='Timmy', gender='M')
		Person.objects.create(name='Johnny', gender='M', father=tim)
		Person.objects.create(name='Jane', gender='F', father=tim)
		
		self.assertEqual(tim.children().count(), 2)
		
		kim = Person.objects.create(name="Kim", gender='F')
		kim.spouses.add(tim)
		
		self.assertEqual(tim in kim.spouses.all(), True)
		
	def testUnderstanding(self):
		
		import simplejson
		
		payload = simplejson.dumps([
			[
				{'name': 'Relation', 'nodes': [
					{'name': ['Relation_Type'], 'value': 'FATHER'}
				]},
		  		{'nodes': [
					{'name': ['Person_Name'], 'value': 'CAIN'}
				], 'name': 'Relation'}
			]
		])
		client = Client()
		response = client.get('/dman/understand/',{'payload':payload})
		self.failUnlessEqual(response.status_code, 200)
		print response.content
		result = simplejson.loads(response.content)
			
		test = client.get('/dman/load/adam/sons/')
		self.failIfEqual(test.content.find('Abel'),-1)
		self.failIfEqual(test.content.find('Seth'),-1)
		self.failIfEqual(test.content.find('Cain'),-1)
		self.failUnlessEqual(test.status_code, 200)