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
	
	spouses = models.ManyToManyField('self', null=True,symmetrical=True,db_table="dman_spouses")
	
	objects = PersonManager()
	
	def gen_spouse_list(self):
		return ",".join([str(x.id) for x in self.souses.all()])
	
	def fathers(self):
		if self.father is not None:
			return [self.father]
		return []
	
	def children(self):
		# Find all the children of a person
		if self.gender=='M':
			return Person.objects.filter(father=self)
		else:
			return Person.objects.filter(mother=self)
			
	def sons(self):
		return self.children().filter(gender='M')
		
	def daughters(self):
		return self.children().filter(gender='F')
	
	def __unicode__(self):
		return self.name
	
	class Admin:
		pass
