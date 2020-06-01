from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View

from backend.document.forms import UserDocumentForm
from backend.document.models import Document, UserDocument
from backend.profile.permissions import CandidateShareholderPermissionsMixin


class VerificationDocView(CandidateShareholderPermissionsMixin, ListView):
    """Документы"""
    # model = Document
    queryset = Document.objects.filter(document="templates_and_samples")
    template_name = "documents/documents-verif.html"


class PhotoVerificationDocView(CandidateShareholderPermissionsMixin, ListView):
    """Фотоверификация"""
    model = Document
    queryset = Document.objects.filter(document="photo_verification")
    template_name = "documents/documents-photo.html"

    def get_context_data(self, **kwargs):
        context = super(PhotoVerificationDocView, self).get_context_data()
        context["form"] = UserDocumentForm()
        # context["document"] = UserDocument.objects.values('user_document')
        # print(context['document'])
        return context


class AddUserDocumentView(View):
    """Загрузка документов пользователем"""
    def post(self, request):
        form = UserDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("doc", None):
                form.document_id = int(request.POST.get('doc'))
            form.user = request.user
            form.save()
            messages.success(request, f'Изменения сохранены')
        return redirect(request.META.get('HTTP_REFERER'))


class DocView(CandidateShareholderPermissionsMixin, ListView):
    """Документы"""
    # model = Document
    queryset = Document.objects.filter(document="document")
    template_name = "documents/documents-docs.html"


class SampleDocView(CandidateShareholderPermissionsMixin, ListView):
    """Шаблоны и образцы"""
    # model = Document
    queryset = Document.objects.filter(document="templates_and_samples")
    template_name = "documents/documents-shablon.html"


class InstructionView(CandidateShareholderPermissionsMixin, ListView):
    """Инструкции"""
    # model = Document
    queryset = Document.objects.filter(document="instructions")
    template_name = "documents/documents-instructions.html"
