from django.urls import path
from backend.document import views

urlpatterns = [
    path("verification/", views.VerificationDocView.as_view(), name="verification"),
    path("photo_verification/", views.PhotoVerificationDocView.as_view(), name="photo_verif"),
    path("documents/", views.DocView.as_view(), name="documents"),
    path("sample/", views.SampleDocView.as_view(), name="sample"),
    path("instructions/", views.InstructionView.as_view(), name="instructions"),

    path("add_document/", views.AddUserDocumentView.as_view(), name="add_doc"),
    ]