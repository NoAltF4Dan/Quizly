from rest_framework import serializers
from quiz_app.models import Quiz, Question

class QuestionPostSerializer(serializers.ModelSerializer):
    class Meta:
        """Serializer for creating/updating question data."""
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']

class QuestionGetSerializer(serializers.ModelSerializer):
    class Meta:
        """Serializer for retrieving question data without timestamps."""
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']

