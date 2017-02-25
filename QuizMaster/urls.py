from django.conf.urls import url
from django.contrib import admin

from QuizMaster.views import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^json/', views.json),
    url(r'^api/question/$', views.QuestionList.as_view()),
    url(r'^api/question/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view()),
]
