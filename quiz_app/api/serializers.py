from rest_framework import serializers
from quiz_app.models import Quiz, Question

class QuestionPostSerializer(serializers.ModelSerializer):
      """
    Create/update `Question` records.

    Behavior
    --------
    - Accepts full question payload: `question_title`, `question_options`, and `answer`.
    - Persists changes via the parent view's `.create()` / `.update()`.
    - Includes `id`, `created_at`, `updated_at` in the representation for client awareness.

    Validation
    ----------
    - Relies on model validation for field-level rules (e.g., choices/length).
    - Add serializer `validate_*` methods if cross-field checks are required.

    Security
    --------
    - Does not expose any sensitive fields beyond question content.
    """
    class Meta:
        """Serializer for creating/updating question data."""
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']

class QuestionGetSerializer(serializers.ModelSerializer):
        """
    Read-only representation of `Question` data without timestamps.

    Behavior
    --------
    - Used for nested reads where audit metadata is unnecessary.
    - Returns `id`, `question_title`, `question_options`, and `answer` only.

    Security
    --------
    - Minimizes surface area by omitting `created_at`/`updated_at`.
    """

    class Meta:
        """Serializer for retrieving question data without timestamps."""
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']

class QuizGetPatchSerializer(serializers.ModelSerializer):
    """
    Retrieve and partially update `Quiz` entities.

    Behavior
    --------
    - `questions`: nested, read-only list rendered via `QuestionGetSerializer`.
      Use write-focused serializers for creation/updating of questions.
    - `video_url`: exposed as read-only string field.
    - Supports `GET` and `PATCH` (partial updates) on quiz-level fields.

    Response Shape
    --------------
    - Returns `id`, `title`, `description`, `created_at`, `updated_at`,
      `video_url`, and nested `questions`.

    Security
    --------
    - Nested questions are read-only to prevent unintended mass updates.
    - No user data is exposed.
    """
    
    questions = QuestionGetSerializer(many=True, read_only=True)
    video_url = serializers.CharField(read_only=True)

    class Meta:
        """Serializer for retrieving and updating quiz data."""
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

class CreateQuizPostSerializer(serializers.ModelSerializer):
    """
    Create a new `Quiz` with associated `Question` records in a single request.

    Behavior
    --------
    - Accepts top-level quiz fields plus a nested `questions` array.
    - `questions` entries are validated with `QuestionPostSerializer`.
    - `video_url` is required as a plain string.
    - Returns created quiz with nested questions.

    Atomicity
    ---------
    - Creation is performed imperatively in `create()`. If you require
      transactional guarantees across quiz + questions, wrap the method
      with `transaction.atomic`.

    Security
    --------
    - Does not infer ownership automatically. The current user is read from
      `self.context['request']` but **not** persisted unless your `Quiz`
      model defines such a field and you assign it.
    """
    
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
