from django.contrib import admin
from .models import (
    User,
    Category,
    Lesson,
    LearningItem,
    Quiz,
    QuizQuestion,
    QuizOption,
    Progress,
    SubscriptionPlan,
    Subscription,
    Payment,
)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(LearningItem)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizOption)
admin.site.register(Progress)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Payment)
