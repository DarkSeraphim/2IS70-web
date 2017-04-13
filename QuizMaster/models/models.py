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

class GroupMeta(models.Model):
  access_code = models.CharField(max_length=32)
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='own_groups')
  group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='meta')

class Quiz(models.Model):
  name = models.CharField(max_length=50)
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizes')
  groups = models.ManyToManyField(Group,
        through='Membership',
        through_fields=('quiz', 'group'),
        related_name='quizes')
  start_at = models.BigIntegerField(default = -1, blank = True)
  close_at = models.BigIntegerField(default = -1, blank = True)
  time_limit = models.IntegerField(null = True)
  pass_threshold = models.PositiveSmallIntegerField()
  published = models.BooleanField(default = False)

# TODO: rename
class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

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
  correct_answer = models.OneToOneField('QuestionAnswer', on_delete=models.CASCADE, related_name='+', null=True)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

class QuestionImage(models.Model):
  path = models.TextField()
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='image')

class QuestionAudio(models.Model):
  path = models.TextField()
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='audio')

class QuestionAnswer(models.Model):
  text = models.CharField(max_length=255, db_index=True)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

class SubmittedQuiz(models.Model):
  submitted_at = models.BigIntegerField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submitted')

class SubmittedQuizAnswer(models.Model):
  quiz = models.ForeignKey(SubmittedQuiz, on_delete=models.CASCADE, related_name='answers')
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
  answer_text = models.CharField(max_length=255)
