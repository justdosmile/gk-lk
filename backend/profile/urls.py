# coding=utf-8
from django.urls import path
from backend.profile import views

urlpatterns = [
    path("turn/", views.MembersCollectiveView.as_view(), name="members_list"),
    path("partner/", views.PartnerCollectiveView.as_view(), name="partner_list"),
    path("queue/", views.TurnView.as_view(), name="turn_list"),
    path("deal/", views.DealView.as_view(), name="deal_list"),
    path("calculated/", views.CalculatedView.as_view(), name="calculated_list"),
    path("debtor/", views.DebtorView.as_view(), name="debtor_list"),

    path("entrance_fee/", views.EntranceFeeView.as_view(), name="entrance_fee"),
    path("share_premium/", views.SharePremiumView.as_view(), name="share_premium"),
    path("confirm_payment/", views.ConfirmPaymentView.as_view(), name="confirm_payment"),
    path("history_payment/", views.HistoryPaymentView.as_view(), name="history_payment"),

    path("verification/", views.VerificationDocView.as_view(), name="verification"),
    path("photo_verification/", views.PhotoVerificationDocView.as_view(), name="photo_verif"),
    path("documents/", views.DocView.as_view(), name="documents"),
    path("sample/", views.SampleDocView.as_view(), name="sample"),
    path("instructions/", views.InstructionView.as_view(), name="instructions"),


    path("create/", views.CreateAddressView.as_view(), name="create"),
    # path("create2/", views.CreateAddress.as_view(), name="create2"),
    # path("", views.edit, name="profile"),

    path("hierarchy/", views.HierarchyView.as_view(), name="hierarchy"),
    path("invitation/", views.LinkInvitationView.as_view(), name="invitation"),

    path("support/", views.SupportView.as_view(), name="support"),

    path("all_user/", views.AdminAllUserView.as_view(), name="all_user"),
    path("all_verification/", views.AdminAllVerificationView.as_view(), name="all_verification"),
    path("all_payment/", views.AdminAllPaymentView.as_view(), name="all_payment"),
    # path("all_support/", views.AdminAllSupportView.as_view(), name="all_support"),
    path("", views.ProfileView.as_view(), name="profile"),
]
