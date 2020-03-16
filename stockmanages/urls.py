from django.urls import path
from . import views

app_name = "stockmanages"

urlpatterns = [
    path(
        "stockmanageshome/", views.stockmanageshome.as_view(), name="stockmanageshome",
    ),
    path(
        "materialchecklist/",
        views.materialchecklist.as_view(),
        name="materialchecklist",
    ),
    path(
        "materialcheckdetail/<int:pk>/",
        views.materialcheckdetail,
        name="materialcheckdetail",
    ),
    path(
        "materialcheckrequest/",
        views.materialcheckrequest,
        name="materialcheckrequest",
    ),
    path(
        "materialcheckrequestdelete/<int:pk>/",
        views.materialcheckrequestdelete,
        name="materialcheckrequestdelete",
    ),
    path("materialinlist/", views.materialinlist.as_view(), name="materialinlist",),
    path(
        "materialinrequestlist/",
        views.materialinrequestlist.as_view(),
        name="materialinrequestlist",
    ),
    path(
        "materialinregister/<int:pk>/",
        views.materialinregister,
        name="materialinregister",
    ),
    path(
        "materialindelete/<int:pk>/", views.materialindelete, name="materialindelete",
    ),
    path("materialoutlist/", views.materialoutlist.as_view(), name="materialoutlist",),
    path(
        "materialoutrequestlist/",
        views.materialoutrequestlist.as_view(),
        name="materialoutrequestlist",
    ),
    path(
        "materialoutregister/<int:pk>/",
        views.materialoutregister,
        name="materialoutregister",
    ),
    path(
        "materialoutdelete/<int:pk>/",
        views.materialoutdelete,
        name="materialoutdelete",
    ),
    path(
        "stockofmateriallist/",
        views.stockofmateriallist.as_view(),
        name="stockofmateriallist",
    ),
    path(
        "updatestockofmaterial/",
        views.updatestockofmaterial,
        name="updatestockofmaterial",
    ),
    path("singleinlist/", views.singleinlist.as_view(), name="singleinlist",),
    path("singleindelete/<int:pk>/", views.singleindelete, name="singleindelete",),
    path(
        "singleinrequestlist/",
        views.singleinrequestlist.as_view(),
        name="singleinrequestlist",
    ),
    path(
        "singleinregister/<int:pk>/", views.singleinregister, name="singleinregister",
    ),
    path("singleoutlist/", views.singleoutlist.as_view(), name="singleoutlist",),
    path("dealdownload/<int:pk>/", views.dealdownload, name="dealdownload",),
    path("singleoutdelete/<int:pk>/", views.singleoutdelete, name="singleoutdelete",),
    path(
        "singleoutrequestlist/",
        views.singleoutrequestlist.as_view(),
        name="singleoutrequestlist",
    ),
    path(
        "singleoutregister/<int:pk>/",
        views.singleoutregister,
        name="singleoutregister",
    ),
    path(
        "stockofsinglelist/",
        views.stockofsinglelist.as_view(),
        name="stockofsinglelist",
    ),
    path(
        "updatestockofsingle/", views.updatestockofsingle, name="updatestockofsingle",
    ),
    path("rackoutlist/", views.rackoutlist.as_view(), name="rackoutlist",),
    path(
        "dealdownloadforrack/<int:pk>/",
        views.dealdownloadforrack,
        name="dealdownloadforrack",
    ),
    path("rackoutdelete/<int:pk>/", views.rackoutdelete, name="rackoutdelete",),
    path(
        "rackoutrequestlist/",
        views.rackoutrequestlist.as_view(),
        name="rackoutrequestlist",
    ),
    path("rackoutregister/<int:pk>/", views.rackoutregister, name="rackoutregister",),
    path("stockofracklist/", views.stockofracklist.as_view(), name="stockofracklist",),
    path(
        "informationforrack/<int:pk>/",
        views.informationforrack,
        name="informationforrack",
    ),
    path(
        "singleStandarInformation/",
        views.singleStandarInformation.as_view(),
        name="singleStandarInformation",
    ),
    path("singleregister/", views.singleregister, name="singleregister",),
    path("singlematerial/<int:pk>/", views.singlematerial, name="singlematerial",),
    path("donesingleregister/", views.donesingleregister, name="donesingleregister",),
    path(
        "singledetail/<int:pk>/", views.SingleDetialView.as_view(), name="singledetail",
    ),
    path("singleedit/<int:pk>/", views.singleedit.as_view(), name="singleedit",),
    path(
        "singledeleteensure/<int:pk>/",
        views.singledeleteensure,
        name="singledeleteensure",
    ),
    path("singledelete/<int:pk>/", views.singledelete, name="singledelete",),
    path(
        "deletematerialofsingle/<int:pk>/<int:m_pk>/",
        views.deletematerialofsingle,
        name="deletematerialofsingle",
    ),
    path(
        "materialStandarInformation/",
        views.materialStandarInformation.as_view(),
        name="materialStandarInformation",
    ),
    path("materialregister/", views.materialregister, name="materialregister",),
    path(
        "materialdetail/<int:pk>/", views.MaterialDetialView.as_view(), name="materialdetail",
    ),
    path("materialedit/<int:pk>/", views.materialedit.as_view(), name="materialedit",),
    path(
        "materialdeleteensure/<int:pk>/",
        views.materialdeleteensure,
        name="materialdeleteensure",
    ),
    path("materialdelete/<int:pk>/", views.materialdelete, name="materialdelete",),
]
