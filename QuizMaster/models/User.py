from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 16)
    password = models.CharField(max_length = 64)
    email = models.CharField(max_length = 50)