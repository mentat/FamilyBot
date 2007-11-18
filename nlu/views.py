# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

def ask(request):
	if request.method=='GET':
		return render_to_response('ask.html')
	else:
		return HttpResponse(request.POST.get('question'))