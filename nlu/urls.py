from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'nlu.views.ask')
)
