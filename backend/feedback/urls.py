# coding=utf-8
from django.urls import path
from backend.feedback import views

app_name = "feedback"
urlpatterns = [
    path("create/", views.FeedbackCreate.as_view(), name="create"),
    path("single_support/<int:pk>/", views.FeedbackDetail.as_view(), name="feedback_single"),
    path("all_support/", views.FeedbackAdminList.as_view(), name="feedback_admin"),
    path("search/", views.SearchFeedback.as_view(), name="feedback_search"),
    path("", views.FeedbackList.as_view(), name="feedback"),
]
