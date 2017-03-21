from rest_framework import serializers
from .models.models import UserType, Quiz, QuizComment, Question, QuestionImage, QuestionAudio, QuestionAnswer, SubmittedQuiz, SubmittedQuizAnswer

class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = ('__all__')

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ('__all__')

class QuizCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizComment
        fields = ('__all__')

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('__all__')

class QuestionImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionImage
        fields = ('__all__')

class QuestionAudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAudio
        fields = ('__all__')

class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('__all__')

class SubmittedQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubmittedQuiz
        fields = ('__all__')

class SubmittedQuizAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubmittedQuizAnswer
        fields = ('__all__')
