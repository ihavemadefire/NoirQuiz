from rest_framework import serializers
from .models import QuizQuestion

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'question_type', 'difficulty', 'points', 'answer']