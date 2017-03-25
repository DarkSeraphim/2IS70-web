from django.conf.urls import url
from django.contrib import admin

from QuizMaster.views import views, usercontroller, groupcontroller, testcontroller
import RequestHandler
RH = RequestHandler


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^index/', views.index),
    #url(r'^json/', views.json),

    # Tom's API
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

    # Mark's API (https://gist.github.com/DarkSeraphim/5412ee94de04be8d4b7351e837bec935)
    url(r'^user/register/?$', 
        RH.of('POST', usercontroller.register)
          .build()), # POST
    url(r'^user/login/?$', 
        RH.of('POST', usercontroller.login)
          .build()), # POST
    url(r'^groups/?$' 
        RH.of('GET', groupcontroller.getAll)
          .forUserTypes(UserType.STUDENT, UserType.TEACHER)
          .build()), # GET
    url(r'^group/?$', 
        RH.of(['POST', 'PUT', 'DELETE'], groupcontroller.manageGroup)
          .forUserTypes(UserType.TEACHER)
          .build()), # POST, PUT?, DELETE
    url(r'^group/subscription/?$', 
        RH.of(['POST', 'DELETE'], groupcontroller.subscription)
          .forUserTypes(UserType.STUDENT)
          .build()), # POST, DELETE
    url(r'^tests/?$', 
        RH.of('GET', testcontroller.getAll)
          .forUserTypes(UserType.STUDENT, UserType.TEACHER)
          .build()), # GET
    url(r'^test/?$', 
        RH.of(['POST', 'PUT', 'DELETE'], testcontroller.manageTest)
          .forUserTypes(UserType.TEACHER)
          .build()), # POST, PUT?, DELETE
    url(r'^test/submit/?$', 
        RH.of('POST', testcontroller.submit)
          .forUserTypes(UserType.STUDENT)
          .build()), # POST
    url(r'^review/as_teacher/?$', 
        RH.of('GET', testcontroller.reviewAsTeacher)
          .forUserTypes(UserType.TEACHER)
          .build()), # GET
    url(r'^review/as_student/?$', 
        RH.of('GET', testcontroller.reviewAsStudent)
        .forUserTypes(UserType.STUDENT)
        .build()), # GET
]
