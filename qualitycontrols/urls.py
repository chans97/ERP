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
]
