from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Lesson, LearningItem, Quiz, QuizQuestion, QuizOption,Progress
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class LearningItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningItem
        fields = '__all__'

class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = '__all__'

class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizOptionSerializer(source='quizoption_set', many=True)

    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'image', 'correct_answer', 'options']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(source='quizquestion_set', many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])


    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            phone_number=validated_data.get('phone_number', ''),
            is_parent=validated_data.get('is_parent', True)
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_parent']


class ProgressSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    lesson_title = serializers.ReadOnlyField(source="lesson.title", default=None)
    item_name = serializers.ReadOnlyField(source="item.name_english", default=None)
    quiz_title = serializers.ReadOnlyField(source="quiz.title", default=None)

    class Meta:
        model = Progress
        fields = [
            'id',
            'username',
            'lesson_title',
            'item_name',
            'quiz_title',
            'completed',
            'stars',
            'quiz_score',
            'completed_at',
        ]
        read_only_fields = ['completed_at', 'username', 'lesson_title', 'item_name', 'quiz_title']        