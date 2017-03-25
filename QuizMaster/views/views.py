from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
#from QuizMaster import QuizMasterConfig
from QuizMaster.models.models import UserType, Quiz, QuizComment, Question, QuestionImage, QuestionAudio, QuestionAnswer, SubmittedQuiz, SubmittedQuizAnswer
from QuizMaster.serializers import UserTypeSerializer, QuizSerializer, QuizCommentSerializer, QuestionSerializer, QuestionImageSerializer, QuestionAudioSerializer, QuestionAnswerSerializer, SubmittedQuizSerializer, SubmittedQuizAnswerSerializer

class UserTypeList(generics.ListCreateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizCommentList(generics.ListCreateAPIView):
    queryset = QuizComment.objects.all()
    serializer_class = QuizCommentSerializer

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionImageList(generics.ListCreateAPIView):
    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer

class QuestionAudioList(generics.ListCreateAPIView):
    queryset = QuestionAudio.objects.all()
    serializer_class = QuestionAudioSerializer

class QuestionAnswerList(generics.ListCreateAPIView):
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer

class SubmittedQuizList(generics.ListCreateAPIView):
    queryset = SubmittedQuiz.objects.all()
    serializer_class = SubmittedQuizSerializer

class SubmittedQuizAnswerList(generics.ListCreateAPIView):
    queryset = SubmittedQuizAnswer.objects.all()
    serializer_class = SubmittedQuizAnswerSerializer

class UserTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizComment.objects.all()
    serializer_class = QuizCommentSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer

class QuestionAudioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionAudio.objects.all()
    serializer_class = QuestionAudioSerializer

class QuestionAnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer

class SubmittedQuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubmittedQuiz.objects.all()
    serializer_class = SubmittedQuizSerializer

class SubmittedQuizAnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubmittedQuizAnswer.objects.all()
    serializer_class = SubmittedQuizAnswerSerializer
