from django.urls import path
from . import views

app_name = "qualitycontrols"

urlpatterns = [
    path(
        "qualitycontrolshome/",
        views.qualitycontrolshome.as_view(),
        name="qualitycontrolshome",
    ),
    path("orderdetail/<int:pk>/", views.OrderDetail.as_view(), name="orderdetail",),
    path(
        "finalcheckdetail/<int:pk>/", views.finalcheckdetail, name="finalcheckdetail",
    ),
    path("repairdetail/<int:pk>/", views.repairdetail, name="repairdetail",),
    path("finalchecklist/", views.finalchecklist.as_view(), name="finalchecklist",),
    path(
        "finalcheckregister/<int:pk>/",
        views.finalcheckregister,
        name="finalcheckregister",
    ),
    path(
        "finalcheckdonelist/",
        views.finalcheckdonelist.as_view(),
        name="finalcheckdonelist",
    ),
    path(
        "finalcheckedit/<int:pk>/",
        views.finalcheckedit.as_view(),
        name="finalcheckedit",
    ),
    path(
        "finalcheckdeleteensure/<int:pk>/",
        views.finalcheckdeleteensure,
        name="finalcheckdeleteensure",
    ),
    path(
        "finalcheckdelete/<int:pk>/", views.finalcheckdelete, name="finalcheckdelete",
    ),
    path(
        "materialchecklist/",
        views.materialchecklist.as_view(),
        name="materialchecklist",
    ),
    path(
        "materialcheckregister/<int:pk>/",
        views.materialcheckregister,
        name="materialcheckregister",
    ),
    path("lowmateriallist/", views.lowmateriallist.as_view(), name="lowmateriallist",),
    path(
        "lowmaterialregister/<int:pk>/",
        views.lowmaterialregister,
        name="lowmaterialregister",
    ),
    path(
        "materialcheckalllist/",
        views.materialcheckalllist.as_view(),
        name="materialcheckalllist",
    ),
    path(
        "materialcheckdetail/<int:pk>/",
        views.materialcheckdetail,
        name="materialcheckdetail",
    ),
    path(
        "lowmetarialedit/<int:pk>/",
        views.lowmetarialedit.as_view(),
        name="lowmetarialedit",
    ),
    path(
        "lowmetarialdeleteensure/<int:pk>/",
        views.lowmetarialdeleteensure,
        name="lowmetarialdeleteensure",
    ),
    path(
        "lowmetarialdelete/<int:pk>/",
        views.lowmetarialdelete,
        name="lowmetarialdelete",
    ),
    path(
        "materialcheckedit/<int:pk>/",
        views.materialcheckedit.as_view(),
        name="materialcheckedit",
    ),
    path(
        "materialcheckdeleteensure/<int:pk>/",
        views.materialcheckdeleteensure,
        name="materialcheckdeleteensure",
    ),
    path(
        "materialcheckdelete/<int:pk>/",
        views.materialcheckdelete,
        name="materialcheckdelete",
    ),
]
