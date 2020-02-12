from django.urls import path
from . import views

app_name = "StandardInformation"

urlpatterns = [
    path("partner/", views.PartnerView.as_view(), name="partner"),
    path("partnerregister/", views.UploadPartnerView.as_view(), name="partnerregister"),
    path("partnersearch/", views.PartnerSearchView.as_view(), name="partnersearch"),
]
