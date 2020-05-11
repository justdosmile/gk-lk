# coding=utf-8
from django.urls import path
from backend.news import views

urlpatterns = [
    path("add/", views.CreatePostView.as_view(), name="add_post"),
    path("update/<slug:slug>/", views.UpdatePostView.as_view(), name="update_post"),
    path("delete/<slug:slug>/", views.DeletePostView.as_view(), name="delete_post"),
    path("<slug:slug>/", views.SinglePostView.as_view(), name="single_post"),
    path("", views.PostListView.as_view(), name="news"),
]
