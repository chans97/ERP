from django.urls import path
from . import views

app_name = "StandardInformation"

urlpatterns = [
    path("partner/", views.PartnerView.as_view(), name="partner"),
    path("partnerregister/", views.UploadPartnerView.as_view(), name="partnerregister"),
    path("partnersearch/", views.PartnerSearchView.as_view(), name="partnersearch"),
    path(
        "partnerdetail/<int:pk>/",
        views.PartnerDetialView.as_view(),
        name="partnerdetail",
    ),
    path("partnerdownload/<int:pk>/", views.file_download, name="partnerdownload",),
    path(
        "partnerdeleteensure/<int:pk>/",
        views.partnerdeleteensure,
        name="partnerdeleteensure",
    ),
    path("partnerdelete/<int:pk>/", views.partnerdelete, name="partnerdelete",),
    path("partneredit/<int:pk>/", views.EditPartnerView.as_view(), name="partneredit",),
    path("single/", views.SingleView.as_view(), name="single"),
    path("singlesearch/", views.SingleSearchView.as_view(), name="singlesearch"),
    path("singleregister/", views.UploadSingleView.as_view(), name="singleregister"),
    path(
        "singledetail/<int:pk>/", views.SingleDetialView.as_view(), name="singledetail",
    ),
    path("singlematerial/<int:pk>/", views.singlematerial, name="singlematerial",),
]
