from django.urls import path
from . import views

app_name = "StandardInformation"

urlpatterns = [
    path("partner/", views.PartnerView.as_view(), name="partner"),
    path("partnerregister/", views.UploadPartnerView, name="partnerregister"),
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
    path("singleregister/", views.UploadSingleView, name="singleregister"),
    path(
        "singledetail/<int:pk>/", views.SingleDetialView.as_view(), name="singledetail",
    ),
    path("singlematerial/<int:pk>/", views.singlematerial, name="singlematerial",),
    path(
        "deletematerialofsingle/<int:pk>/<int:m_pk>/",
        views.deletematerialofsingle,
        name="deletematerialofsingle",
    ),
    path(
        "singledeleteensure/<int:pk>/",
        views.singledeleteensure,
        name="singledeleteensure",
    ),
    path("singledelete/<int:pk>/", views.singledelete, name="singledelete",),
    path("singleedit/<int:pk>/", views.EditSingleView.as_view(), name="singleedit",),
    path("rack/", views.RackView.as_view(), name="rack"),
    path("rackdetail/<int:pk>/", views.RackDetialView.as_view(), name="rackdetail",),
    path("rackregister/", views.UploadRackView, name="rackregister"),
    path("racksingle/<int:pk>/", views.racksingle, name="racksingle",),
    path("rackmaterial/<int:pk>/", views.rackmaterial, name="rackmaterial",),
    path(
        "deletesingleofrack/<int:pk>/<int:m_pk>/",
        views.deletesingleofrack,
        name="deletesingleofrack",
    ),
    path(
        "deletematerialofrack/<int:pk>/<int:m_pk>/",
        views.deletematerialofrack,
        name="deletematerialofrack",
    ),
    path("rackedit/<int:pk>/", views.EditRackView.as_view(), name="rackedit",),
    path(
        "rackdeleteensure/<int:pk>/", views.rackdeleteensure, name="rackdeleteensure",
    ),
    path("rackdelete/<int:pk>/", views.rackdelete, name="rackdelete",),
    path("donesingleregister/", views.donesingleregister, name="donesingleregister"),
    path("donerackregister/", views.donerackregister, name="donerackregister"),
]
