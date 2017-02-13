from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def index(request):
  return HttpResponse("Hello world!")

def json(request):
  return JsonResponse({
    'foo': 1,
    'bar': 'bat'
  })
