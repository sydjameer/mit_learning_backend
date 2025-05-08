from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/lessons', views.LessonListView.as_view()),
    path('api/lessons/<int:id>', views.LessonDetailView.as_view()),
    path('api/lessons/<int:id>/items', views.LessonItemsView.as_view()),
    path('api/lessons/<int:id>/quiz', views.LessonQuizView.as_view()),
    path('api/categories', views.CategoryListView.as_view()),
    path('api/categories/<str:id>', views.CategoryDetailView.as_view()),
    path('api/categories/<str:id>/lessons', views.CategoryLessonsView.as_view()),
    path('api/auth/register', views.RegisterView.as_view(), name='register'),
    path('api/auth/login', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/me', views.UserProfileView.as_view(), name='user_profile'),
    path('api/progress', views.ProgressListCreateView.as_view(), name='progress-list-create'),
]
