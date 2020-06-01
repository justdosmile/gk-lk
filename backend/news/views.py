from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from ..profile.permissions import AdminPermissionsMixin


class PostListView(LoginRequiredMixin, ListView):
    """Список всех новостей """
    paginate_by = 6
    template_name = "news/news-all.html"

    def get_queryset(self):
        return Post.objects.filter(published=True)


class SinglePostView(LoginRequiredMixin, DetailView):
    """Полная новость"""
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        query = Post.objects.filter(slug=self.kwargs.get("slug"))
        for a in query:
            a.viewed += 1
            a.save()
        return query


class CreatePostView(AdminPermissionsMixin, CreateView):
    """Создание новости в шаблоне"""
    model = Post
    fields = ['title', 'image', 'mini_text', 'text', 'published_date', 'published']

    def form_valid(self, form):
        form.instance.user = self.request.user
        # messages.success(self.request, f'Ваша статья готовится к публикации!')
        return super().form_valid(form)


class UpdatePostView(AdminPermissionsMixin, UpdateView):
    """Обновляем новости в шаблоне"""
    model = Post
    slug_field = 'slug'
    fields = ['title', 'image', 'mini_text', 'text', 'published_date', 'published']

    def form_valid(self, form):
        form.instance.author = self.request.user  # --?????
        # messages.success(self.request, f'Ваша статья готовится к публикации!')
        return super().form_valid(form)


class DeletePostView(AdminPermissionsMixin, DeleteView):
    """Удаляем новости в шаблоне"""
    model = Post
    slug_field = 'slug'
    success_url = '/'


