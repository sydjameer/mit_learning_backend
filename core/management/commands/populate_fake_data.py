from django.core.management.base import BaseCommand
from faker import Faker
from core.models import User, Category, Lesson, LearningItem, Quiz, QuizQuestion, QuizOption
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Populate fake data for Kids Learning App models'

    def handle(self, *args, **kwargs):
        # Create Users (Parents)
        self.create_users()

        # Create Categories
        self.create_categories()

        # Create Lessons
        self.create_lessons()

        # Create Learning Items
        self.create_learning_items()

        # Create Quizzes and Quiz Questions
        self.create_quizzes()

        self.stdout.write(self.style.SUCCESS('Successfully populated fake data!'))

    def create_users(self):
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
                is_parent=True,
                phone_number=fake.phone_number()
            )
            user.is_active = True
            user.save()

    def create_categories(self):
        for _ in range(5):
            Category.objects.create(
                id=fake.slug(),
                name=fake.word().capitalize(),
                color=fake.color_name(),
                bg_color=fake.color_name(),
                icon="📚",
                is_premium=random.choice([True, False])
            )

    def create_lessons(self):
        categories = Category.objects.all()
        for _ in range(10):
            lesson = Lesson.objects.create(
                category=random.choice(categories),
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(),
                image=fake.image_url(),
                is_premium=random.choice([True, False])
            )

    def create_learning_items(self):
        lessons = Lesson.objects.all()
        for lesson in lessons:
            for _ in range(3):
                LearningItem.objects.create(
                    lesson=lesson,
                    image=fake.image_url(),
                    name_english=fake.word(),
                    name_malay=fake.word(),
                    name_arabic=fake.word()
                )

    def create_quizzes(self):
        lessons = Lesson.objects.all()
        for lesson in lessons:
            quiz = Quiz.objects.create(
                lesson=lesson,
                title=f"Quiz for {lesson.title}",
                description=fake.paragraph()
            )
            for _ in range(3):
                question = QuizQuestion.objects.create(
                    quiz=quiz,
                    question=fake.sentence(),
                    image=fake.image_url(),
                    correct_answer="A"
                )
                for opt in ['A', 'B', 'C', 'D']:
                    QuizOption.objects.create(
                        question=question,
                        option_text=fake.word()
                    )

