from django.conf.urls.defaults import *

urlpatterns = patterns('dman.views',
	(r'^understand/$', 'understand'),
	(r'^load/(?P<subject>[A-Za-z]+)/(?P<relation>[A-Za-z ]+)/', 'load')
)
