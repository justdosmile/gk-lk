from django.contrib import admin

from backend.feedback.models import Feedback, Answer


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Обратная связь"""
    list_display = ('title', 'user', 'date', "processing", "id")
    list_filter = ("title", "date")
    search_fields = ("title",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback', 'data')
    list_filter = ('data',)
    search_fields = ('user', 'text')

