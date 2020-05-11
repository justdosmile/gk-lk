# coding=utf-8
from django.urls import path
from backend.feedback import views

app_name = "feedback"
urlpatterns = [
    path("create/", views.FeedbackCreateView.as_view(), name="create"),
    path("single_support/<int:pk>/", views.FeedbackDetailView.as_view(), name="feedback_single"),
    path("all_support/", views.FeedbackAdminListView.as_view(), name="feedback_admin"),
    path("", views.FeedbackListView.as_view(), name="feedback"),
]
