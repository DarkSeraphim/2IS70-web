from django.conf.urls import url
from django.contrib import admin

from QuizMaster.views import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^json/', views.json),
    url(r'^api/usertype/$', views.UserTypeList.as_view()),
    url(r'^api/usertype/(?P<pk>[0-9]+)/$', views.UserTypeDetail.as_view()),
    url(r'^api/quiz/$', views.QuizList.as_view()),
    url(r'^api/quiz/(?P<pk>[0-9]+)/$', views.QuizDetail.as_view()),
    url(r'^api/quizcomment/$', views.QuizCommentList.as_view()),
    url(r'^api/quizcomment/(?P<pk>[0-9]+)/$', views.QuizCommentDetail.as_view()),
    url(r'^api/question/$', views.QuestionList.as_view()),
    url(r'^api/question/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view()),
    url(r'^api/questionimage/$', views.QuestionImageList.as_view()),
    url(r'^api/questionimage/(?P<pk>[0-9]+)/$', views.QuestionImageDetail.as_view()),
    url(r'^api/questionaudio/$', views.QuestionAudioList.as_view()),
    url(r'^api/questionaudio/(?P<pk>[0-9]+)/$', views.QuestionAudioDetail.as_view()),
    url(r'^api/questionanswer/$', views.QuestionAnswerList.as_view()),
    url(r'^api/questionanswer/(?P<pk>[0-9]+)/$', views.QuestionAnswerDetail.as_view()),
    url(r'^api/submittedquiz/$', views.SubmittedQuizList.as_view()),
    url(r'^api/submittedquiz/(?P<pk>[0-9]+)/$', views.SubmittedQuizDetail.as_view()),
    url(r'^api/submittedquizanswer/$', views.SubmittedQuizAnswerList.as_view()),
    url(r'^api/submittedquizanswer/(?P<pk>[0-9]+)/$', views.SubmittedQuizAnswerDetail.as_view()),
]
