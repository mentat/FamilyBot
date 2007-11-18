from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^familybot/', include('familybot.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),

	(r'^test/', 'nlg.views.test')
)
