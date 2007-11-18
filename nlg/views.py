# Create your views here.
import simplejson, re
from familybot.nlg.language_templates import *
from django.http import HttpResponse

def generate(request):
	languageResponse = simplejson.loads(request["payload"])
	response = TEMPLATES[languageResponse["actions"][0]["action"]](languageResponse["actions"][0])
	return HttpResponse(response)
	
