# Create your views here.
import simplejson

from django.http import HttpResponse
def test(request):
	x = simplejson.loads(request["payload"])
	return HttpResponse(x['hi'])