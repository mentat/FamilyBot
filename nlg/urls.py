from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^graphic/$', 'nlg.views.generateGraphvizFile')
)
