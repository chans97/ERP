from django.urls import path
from . import views

app_name = "afterservices"

urlpatterns = [
    path(
        "afterserviceshome/",
        views.afterserviceshome.as_view(),
        name="afterserviceshome",
    ),
    path("ASregister/", views.ASregister, name="ASregister",),
    path(
        "afterservicesingle/<int:pk>/",
        views.afterservicesingle,
        name="afterservicesingle",
    ),
    path(
        "afterservicesrack/<int:pk>/",
        views.afterservicesrack,
        name="afterservicesrack",
    ),
    path(
        "ASvisitrequestslist/",
        views.ASvisitrequestslist.as_view(),
        name="ASvisitrequestslist",
    ),
    path("ASvisitrequests/<int:pk>/", views.ASvisitrequests, name="ASvisitrequests",),
    path("ASregisterall/", views.ASregisterall.as_view(), name="ASregisterall",),
    path(
        "ASrequestdetail/<int:pk>/",
        views.ASrequestdetail,
        name="ASrequestdetail",
    ),
    
]
