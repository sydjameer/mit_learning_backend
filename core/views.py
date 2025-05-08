from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Lesson, LearningItem, Quiz,Progress
from .serializers import (
    CategorySerializer,
    LessonSerializer,
    LearningItemSerializer,
    QuizSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    ProgressSerializer
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'id'

class LessonItemsView(APIView):
    def get(self, request, id):
        items = LearningItem.objects.filter(lesson_id=id)
        serializer = LearningItemSerializer(items, many=True)
        return Response(serializer.data)

class LessonQuizView(APIView):
    def get(self, request, id):
        try:
            quiz = Quiz.objects.get(lesson_id=id)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=404)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class CategoryLessonsView(APIView):
    def get(self, request, id):
        lessons = Lesson.objects.filter(category_id=id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ProgressListCreateView(generics.ListCreateAPIView):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)    