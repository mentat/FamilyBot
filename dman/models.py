from django.db import models

# Create your models here.

class PersonManager(models.Manager):
	pass
		
class Person(models.Model):
	GENDER = (
		('M', 'Male'),
		('F', 'Female')
	)
	name = models.CharField(maxlength=100, db_index=True)
	mother = models.ForeignKey('self', blank=True, null=True, related_name='maternal')
	father = models.ForeignKey('self', blank=True, null=True, related_name='paternal')
	gender = models.CharField(maxlength=1, choices = GENDER, db_index=True)
	
	spouse = models.ManyToManyField('self', null=True, related_name="spouses")
	
	objects = PersonManager()
	
	def children(self):
		# Find all the children of a person
		if self.gender=='M':
			return Person.objects.filter(father=self)
		else:
			return Person.objects.filter(mother=self)
	
	def __unicode__(self):
		return self.name
	
	class Admin:
		pass
