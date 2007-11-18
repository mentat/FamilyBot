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