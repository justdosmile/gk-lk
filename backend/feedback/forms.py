from django import forms
from .models import Feedback, Answer


class FeedbackForm(forms.ModelForm):
    """Форма обратной связи"""

    class Meta:
        model = Feedback
        fields = ("title", "text", "image")


class AnswerForm(forms.ModelForm):
    """Ответ на вопрос"""

    class Meta:
        model = Answer
        fields = ("title", "text", "image")