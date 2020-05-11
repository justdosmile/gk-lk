from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, DetailView

from .models import Feedback
from .forms import FeedbackForm


class FeedbackListView(LoginRequiredMixin, ListView):
    """Список обратных связей"""
    paginate_by = 6
    template_name = "feedback/feedback_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user)


class FeedbackAdminListView(PermissionRequiredMixin, ListView):
    """Список обратных связей в адменистрированнии"""
    paginate_by = 6
    template_name = "administrirovanie/admin-support.html"

    def get_queryset(self):
        return Feedback.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


class FeedbackDetailView(PermissionRequiredMixin, DetailView):
    """Детально о запросе в адменистрированнии"""
    model = Feedback
    context_object_name = 'single_support'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Feedback, id=self.kwargs.get('pk'))
        return obj

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


class SearchFeedbackView(PermissionRequiredMixin, ListView):
    """Поиск пользователей по ФИО в адменистрированнии"""
    paginate_by = 5
    template_name = "administrirovanie/admin-support.html"

    def get_queryset(self):
        return Feedback.objects.filter(user__username__icontains=self.request.GET.get('qus'))

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    """Добавление обратной связи"""
    model = Feedback
    form_class = FeedbackForm
    # template_name = 'feedback/feedback_list.html'
    success_url = '/feedback/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # self.success_url = form.instance.get_absolute_url()
        # form.save()
        message = 'Отправлено в службу поддержки.'
        messages.success(self.request, message)
        return super(FeedbackCreateView, self).form_valid(form)
