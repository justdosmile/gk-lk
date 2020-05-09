from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, DetailView

from .models import Feedback
from .forms import FeedbackForm


class FeedbackList(LoginRequiredMixin, ListView):
    """Список обратных связей"""
    paginate_by = 6
    template_name = "feedback/feedback_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user)


class FeedbackAdminList(LoginRequiredMixin, ListView):
    """Список обратных связей в адменистрированнии"""
    paginate_by = 6
    template_name = "administrirovanie/admin-support.html"

    def get_queryset(self):
        return Feedback.objects.all()


class FeedbackDetail(LoginRequiredMixin, DetailView):
    """Детально о запросе"""
    model = Feedback
    context_object_name = 'single_support'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Feedback, id=self.kwargs.get('pk'))
        return obj


class SearchFeedback(LoginRequiredMixin, ListView):
    """Поиск пользователей по ФИО"""
    paginate_by = 5
    template_name = "administrirovanie/admin-support.html"

    def get_queryset(self):
        return Feedback.objects.filter(user__username=self.request.GET.get('qus'))


class FeedbackCreate(LoginRequiredMixin, CreateView):
    """Добавление обратной связи"""
    model = Feedback
    form_class = FeedbackForm
    # template_name = 'feedback/feedback_list.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # self.success_url = form.instance.get_absolute_url()
        # form.save()
        message = 'Отправлено в службу поддержки.'
        messages.success(self.request, message)
        return super(FeedbackCreate, self).form_valid(form)
