# coding=utf-8
from django.urls import path
from backend.news import views

urlpatterns = [
    path("add/", views.CreatePostView.as_view(), name="add-post"),
    path("<slug:slug>/", views.SinglePost.as_view(), name="single_post"),
    path("", views.PostList.as_view(), name="news"),
]
