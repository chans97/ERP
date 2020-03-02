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
    path("ASRegistersedit/<int:pk>/", views.ASRegistersedit.as_view(), name="ASRegistersedit",),
    path("ASRegisterdeleteensure/<int:pk>/", views.ASRegisterdeleteensure, name="ASRegisterdeleteensure",),
    path("ASRegisterdelete/<int:pk>/", views.ASRegisterdelete, name="ASRegisterdelete",),
    path("ASregisterdoneinsidelist/", views.ASregisterdoneinsidelist.as_view(), name="ASregisterdoneinsidelist",),
    path("ASdoneinside/<int:pk>/", views.ASdoneinside, name="ASdoneinside",),
    path("ASsuccessdeleteensure/<int:pk>/", views.ASsuccessdeleteensure, name="ASsuccessdeleteensure",),
    path("ASsuccessdelete/<int:pk>/", views.ASsuccessdelete, name="ASsuccessdelete",),
    
    
    
    
    
]
