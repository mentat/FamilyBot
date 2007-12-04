from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'nlu.views.ask'),
	(r'^graphic/(?P<key>.+)/$', 'nlu.views.graph'),
	(r'^refresh/$', 'nlu.views.refresh_grammar')
)
