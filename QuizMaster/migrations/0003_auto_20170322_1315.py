# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-22 12:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizMaster', '0002_auto_20170322_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='questionanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionaudio',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionimage',
            name='question',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='group',
        ),
        migrations.RemoveField(
            model_name='quizcomment',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizcomment',
            name='reply_to',
        ),
        migrations.RemoveField(
            model_name='quizcomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='submittedquiz',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='submittedquiz',
            name='user',
        ),
        migrations.RemoveField(
            model_name='submittedquizanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='submittedquizanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='submittedquizanswer',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='usertype',
            name='user',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='QuestionAnswer',
        ),
        migrations.DeleteModel(
            name='QuestionAudio',
        ),
        migrations.DeleteModel(
            name='QuestionImage',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.DeleteModel(
            name='QuizComment',
        ),
        migrations.DeleteModel(
            name='SubmittedQuiz',
        ),
        migrations.DeleteModel(
            name='SubmittedQuizAnswer',
        ),
        migrations.DeleteModel(
            name='UserType',
        ),
    ]
