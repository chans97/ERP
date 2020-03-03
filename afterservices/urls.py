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
    path("ASrequestdetail/<int:pk>/", views.ASrequestdetail, name="ASrequestdetail",),
    path(
        "ASRegistersedit/<int:pk>/",
        views.ASRegistersedit.as_view(),
        name="ASRegistersedit",
    ),
    path(
        "ASRegisterdeleteensure/<int:pk>/",
        views.ASRegisterdeleteensure,
        name="ASRegisterdeleteensure",
    ),
    path(
        "ASRegisterdelete/<int:pk>/", views.ASRegisterdelete, name="ASRegisterdelete",
    ),
    path(
        "ASregisterdoneinsidelist/",
        views.ASregisterdoneinsidelist.as_view(),
        name="ASregisterdoneinsidelist",
    ),
    path("ASdoneinside/<int:pk>/", views.ASdoneinside, name="ASdoneinside",),
    path(
        "ASsuccessdeleteensure/<int:pk>/",
        views.ASsuccessdeleteensure,
        name="ASsuccessdeleteensure",
    ),
    path("ASsuccessdelete/<int:pk>/", views.ASsuccessdelete, name="ASsuccessdelete",),
    path("ASvisitneedlist/", views.ASvisitneedlist.as_view(), name="ASvisitneedlist",),
    path("ASvisitregister/<int:pk>/", views.ASvisitregister, name="ASvisitregister",),
    path("ASvisitedit/<int:pk>/", views.ASvisitedit.as_view(), name="ASvisitedit",),
    path(
        "ASvisitdeleteensure/<int:pk>/",
        views.ASvisitdeleteensure,
        name="ASvisitdeleteensure",
    ),
    path("ASvisitdelete/<int:pk>/", views.ASvisitdelete, name="ASvisitdelete",),
    path(
        "ASrevisitneedlist/",
        views.ASrevisitneedlist.as_view(),
        name="ASrevisitneedlist",
    ),
    path(
        "ASrevisitregister/<int:pk>/",
        views.ASrevisitregister,
        name="ASrevisitregister",
    ),
    path(
        "ASrevisitedit/<int:pk>/", views.ASrevisitedit.as_view(), name="ASrevisitedit",
    ),
    path(
        "ASrevisitdeleteensure/<int:pk>/",
        views.ASrevisitdeleteensure,
        name="ASrevisitdeleteensure",
    ),
    path("ASrevisitdelete/<int:pk>/", views.ASrevisitdelete, name="ASrevisitdelete",),
    path("ASsuccesslist/", views.ASsuccesslist.as_view(), name="ASsuccesslist",),
    path("ASdonevisit/<int:pk>/", views.ASdonevisit, name="ASdonevisit",),
    path("ASdonerevisit/<int:pk>/", views.ASdonerevisit, name="ASdonerevisit",),
    path(
        "ASrepairorderalllist/",
        views.ASrepairorderalllist.as_view(),
        name="ASrepairorderalllist",
    ),
    path(
        "repairrequestdetail/<int:pk>/",
        views.repairrequestdetail,
        name="repairrequestdetail",
    ),
    path("ASexrepairlist/", views.ASexrepairlist.as_view(), name="ASexrepairlist",),
    path(
        "ASrepairrequestregister/<int:pk>/",
        views.ASrepairrequestregister,
        name="ASrepairrequestregister",
    ),
    path("rackdetail/<int:pk>/", views.RackDetialView.as_view(), name="rackdetail",),
    path(
        "singledetail/<int:pk>/", views.SingleDetialView.as_view(), name="singledetail",
    ),
    path(
        "ASrepairrequestregistersingle/<int:pk>/",
        views.ASrepairrequestregistersingle,
        name="ASrepairrequestregistersingle",
    ),
    path(
        "ASrepairrequestregisterrack/<int:pk>/",
        views.ASrepairrequestregisterrack,
        name="ASrepairrequestregisterrack",
    ),
    path(
        "repairrequestdeleteensure/<int:pk>/",
        views.repairrequestdeleteensure,
        name="repairrequestdeleteensure",
    ),
    path(
        "repairrequestdelete/<int:pk>/",
        views.repairrequestdelete,
        name="repairrequestdelete",
    ),
    path(
        "ASsingleoutalllist/",
        views.ASsingleoutalllist.as_view(),
        name="ASsingleoutalllist",
    ),
    path(
        "ASexsingleoutlist/",
        views.ASexsingleoutlist.as_view(),
        name="ASexsingleoutlist",
    ),
    path(
        "orderstocksingledelete/<int:pk>/",
        views.orderstocksingledelete,
        name="orderstocksingledelete",
    ),
    path(
        "ASsingleoutrequestregister/<int:pk>/",
        views.ASsingleoutrequestregister,
        name="ASsingleoutrequestregister",
    ),
    path(
        "ASsingleoutrequestregistersingle/<int:pk>/",
        views.ASsingleoutrequestregistersingle,
        name="ASsingleoutrequestregistersingle",
    ),
    path(
        "ASsingleoutrequestregisterrack/<int:pk>/",
        views.ASsingleoutrequestregisterrack,
        name="ASsingleoutrequestregisterrack",
    ),
]
