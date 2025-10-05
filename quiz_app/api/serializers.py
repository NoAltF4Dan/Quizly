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

class QuizGetPatchSerializer(serializers.ModelSerializer):
    questions = QuestionGetSerializer(many=True, read_only=True)
    video_url = serializers.CharField(read_only=True)

    class Meta:
        """Serializer for retrieving and updating quiz data."""
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

class CreateQuizPostSerializer(serializers.ModelSerializer):
    questions = QuestionPostSerializer(many=True)
    video_url = serializers.CharField()

    class Meta:
        """Serializer for creating a new quiz with associated questions."""
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

    def create(self, validated_data):        
        """Create a new quiz and associated questions."""
        user = self.context['request'].user
        questions_data = validated_data.pop('questions')
        
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            question = Question.objects.create(**question_data)
            quiz.questions.add(question)
            
        return quiz
