from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
#from QuizMaster import QuizMasterConfig
from QuizMaster.models.models import Question
from QuizMaster.serializers import QuestionSerializer

def index(request):
  return HttpResponse("Hello world!")

def json(request):
  return JsonResponse({
    'foo': 1,
    'bar': 'bat'
  })

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
