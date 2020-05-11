# coding=utf-8
from django.urls import path
from backend.news import views

urlpatterns = [
    path("add/", views.CreatePostView.as_view(), name="add_post"),
    path("<slug:slug>/", views.SinglePostView.as_view(), name="single_post"),
    path("", views.PostListView.as_view(), name="news"),
]
