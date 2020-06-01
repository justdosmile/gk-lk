from django.forms import ModelForm

from backend.document.models import UserDocument


class UserDocumentForm(ModelForm):
    """Форма загрузки документов"""
    class Meta:
        model = UserDocument
        fields = ['user_document']