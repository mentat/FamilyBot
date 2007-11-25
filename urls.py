from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^familybot/', include('familybot.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),

	(r'^generate/', 'nlg.views.generate'),
	(r'^nlu/', include('familybot.nlu.urls')),
	(r'^dman/', include('familybot.dman.urls'))
)
