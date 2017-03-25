from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from datetime import datetime

class UserType(models.Model):
  STUDENT = 'student'
  TEACHER = 'teacher'
  TYPES = (
    (STUDENT, 'Student'),
    (TEACHER, 'Teacher')
  )
  max_length = 0
  for tuple in TYPES:
    max_length = max(len(tuple[0]), max_length)

  type = models.CharField(max_length=max_length, choices=TYPES, default=STUDENT)
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='type')

  del max_length

"""class Group(models.Model):
  name =  models.CharField(max_length=50)
  users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groups')
"""

"""
User_Group:
  user -> fkey User
  group -> fkey Group
"""

class Quiz(models.Model):
  pass_threshold = models.PositiveSmallIntegerField()
  start_at = models.DateTimeField(default = datetime.now, blank = True)
  close_at = models.DateTimeField(default = datetime.now, blank = True)
  time_limit = models.IntegerField(null = True)
  published = models.BooleanField(default = False)
  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='quizes')
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizes')

"""
Group_Quiz
  quiz -> fkey Quiz
  group -> fkey Group
"""

class QuizComment(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='comments')
  reply_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
  created = models.DateTimeField()

class Question(models.Model):
  text = models.TextField()
  is_open = models.BooleanField()
  weight = models.PositiveSmallIntegerField() # Eliminates precision errors with later math
  answer = models.OneToOneField('QuestionAnswer', on_delete=models.CASCADE, related_name='+')
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

class QuestionImage(models.Model):
  image = models.TextField()
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='image')

class QuestionAudio(models.Model):
  audio = models.TextField()
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='audio')

class QuestionAnswer(models.Model):
  text = models.CharField(max_length=255, db_index=True)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

class SubmittedQuiz(models.Model):
  submitted_at = models.DateTimeField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submitted')

class SubmittedQuizAnswer(models.Model):
  quiz = models.ForeignKey(SubmittedQuiz, on_delete=models.CASCADE, related_name='answers')
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
  answer_text = models.CharField(max_length=255)
