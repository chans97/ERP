from django.urls import path
from . import views

app_name = "producemanages"

urlpatterns = [
    path("producemanageshome/", views.producemanageshome, name="producemanageshome"),
    path("produceplanlist/", views.produceplanlist, name="produceplanlist"),
    path(
        "produceplanregister/<int:pk>/",
        views.produceplanregister,
        name="produceplanregister",
    ),
    path("orderdetail/<int:pk>/", views.OrderDetail.as_view(), name="orderdetail"),
    path(
        "produceplanupdate/<int:pk>/",
        views.produceplanupdate.as_view(),
        name="produceplanupdate",
    ),
    path(
        "produceplantotalupdate/<int:pk>/",
        views.produceplantotalupdate.as_view(),
        name="produceplantotalupdate",
    ),
    path(
        "produceplanupdeleteensure/<int:pk>/",
        views.produceplanupdeleteensure,
        name="produceplanupdeleteensure",
    ),
    path(
        "produceplanupdelete/<int:pk>/",
        views.produceplanupdelete,
        name="produceplanupdelete",
    ),
    path("workorderlist/", views.workorderlist, name="workorderlist"),
    path(
        "workorder/<int:pk>/",
        views.workorder,
        name="workorder",
    ),
]
