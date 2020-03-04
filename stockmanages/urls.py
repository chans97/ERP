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
]
