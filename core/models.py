from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Additional fields for the user model
    phone_number = models.CharField(max_length=15, blank=True)
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True)
    is_parent = models.BooleanField(default=True)

    groups = models.ManyToManyField(
    'auth.Group',
    related_name='custom_user_set',  # Avoids the clash with the default User model
    blank=True,
    )
  
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Avoids the clash with the default User model
        blank=True,
    )

    def __str__(self):
        return self.username

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=50)
    icon = models.CharField(max_length=10)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="lessons/", blank=True, null=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
      return f"{self.title} ({self.category.name})"

class LearningItem(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="learning_items/", blank=True, null=True)
    name_english = models.CharField(max_length=100)
    name_malay = models.CharField(max_length=100)
    name_arabic = models.CharField(max_length=100)

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to="quizzes/", blank=True, null=True)
    correct_answer = models.CharField(max_length=100)

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_id = models.CharField(max_length=100)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

class Progress(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('LearningItem', on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    stars = models.IntegerField(default=0)
    quiz_score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now=True)    
