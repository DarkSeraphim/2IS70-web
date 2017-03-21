from django.contrib import admin
from QuizMaster.models.models import UserType, Quiz, QuizComment, Question, QuestionImage, QuestionAudio, QuestionAnswer, SubmittedQuiz, SubmittedQuizAnswer

# Register your models here.
admin.site.register(UserType)
admin.site.register(Quiz)
admin.site.register(QuizComment)
admin.site.register(Question)
admin.site.register(QuestionImage)
admin.site.register(QuestionAudio)
admin.site.register(QuestionAnswer)
admin.site.register(SubmittedQuiz)
admin.site.register(SubmittedQuizAnswer)
