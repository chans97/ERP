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
        "produceplandeleteensure/<int:pk>/",
        views.produceplandeleteensure,
        name="produceplandeleteensure",
    ),
    path(
        "produceplandelete/<int:pk>/",
        views.produceplandelete,
        name="produceplandelete",
    ),
    path("rackmakelist/", views.rackmakelist, name="rackmakelist"),
    path("workorder/<int:pk>/", views.workorder, name="workorder",),
    path(
        "workorderupdate/<int:pk>/",
        views.workorderupdate.as_view(),
        name="workorderupdate",
    ),
    path(
        "workorderdeleteensure/<int:pk>/",
        views.workorderdeleteensure,
        name="workorderdeleteensure",
    ),
    path("workorderdelete/<int:pk>/", views.workorderdelete, name="workorderdelete",),
    path("producehome/", views.producehome, name="producehome"),
    path("worklist/", views.worklist, name="worklist"),
    path("workregister/<int:pk>/", views.workregister, name="workregister",),
    path("workdonelist/", views.workdonelist, name="workdonelist"),
    path("orderfinalcheck/<int:pk>/", views.orderfinalcheck, name="orderfinalcheck",),
    path(
        "orderdetailforwork/<int:pk>/",
        views.OrderDetailForWork.as_view(),
        name="orderdetailforwork",
    ),
    path(
        "orderfinaldelete/<int:pk>/", views.orderfinaldelete, name="orderfinaldelete",
    ),
    path(
        "workdeleteensure/<int:pk>/", views.workdeleteensure, name="workdeleteensure",
    ),
    path("workdelete/<int:pk>/", views.workdelete, name="workdelete",),
    path("workupdate/<int:pk>/", views.workupdate.as_view(), name="workupdate",),
    path("finalchecklist/", views.finalchecklist, name="finalchecklist"),
    path("repairregister/<int:pk>/", views.repairregister, name="repairregister",),
    path("repairupdate/<int:pk>/", views.repairupdate.as_view(), name="repairupdate",),
    path("repairlist/", views.repairlist, name="repairlist"),
    path("repairdetail/<int:pk>/", views.repairdetail, name="repairdetail",),
    path(
        "repairupdateindetail/<int:pk>/",
        views.repairupdateindetail.as_view(),
        name="repairupdateindetail",
    ),
    path(
        "repairdeleteensure/<int:pk>/",
        views.repairdeleteensure,
        name="repairdeleteensure",
    ),
    path("repairdelete/<int:pk>/", views.repairdelete, name="repairdelete",),
    path(
        "orderfinalcheckforrepair/<int:pk>/",
        views.orderfinalcheckforrepair,
        name="orderfinalcheckforrepair",
    ),
    path("checkdonelist/", views.checkdonelist, name="checkdonelist"),
    path(
        "finalcheckdetail/<int:pk>/", views.finalcheckdetail, name="finalcheckdetail",
    ),
    path("ASrequestlist/", views.ASrequestlist, name="ASrequestlist"),
    path(
        "repairregisterAS/<int:pk>/", views.repairregisterAS, name="repairregisterAS",
    ),
    path(
        "finalcheckrequestdelete/<int:pk>/",
        views.finalcheckrequestdelete,
        name="finalcheckrequestdelete",
    ),
    path(
        "repairupdateindetailAS/<int:pk>/",
        views.repairupdateindetailAS.as_view(),
        name="repairupdateindetailAS",
    ),
    path(
        "repairrequestdetail/<int:pk>/",
        views.repairrequestdetail,
        name="repairrequestdetail",
    ),
    path(
        "requestrackmakelist/",
        views.requestrackmakelist.as_view(),
        name="requestrackmakelist",
    ),
    path(
        "rackmakeregister/<int:pk>/", views.rackmakeregister, name="rackmakeregister",
    ),
    path("rackmakeedit/<int:pk>/", views.rackmakeedit.as_view(), name="rackmakeedit",),
    path(
        "rackmakedeleteensure/<int:pk>/",
        views.rackmakedeleteensure,
        name="rackmakedeleteensure",
    ),
    path("rackmakedelete/<int:pk>/", views.rackmakedelete, name="rackmakedelete",),
    path("monthlyplanlist/", views.monthlyplanlist.as_view(), name="monthlyplanlist",),
    path(
        "monthlyplandetail/<int:ypk>/<int:mpk>",
        views.monthlyplandetail,
        name="monthlyplandetail",
    ),
    path("monthlyplannewlist/", views.monthlyplannewlist.as_view(), name="monthlyplannewlist",),
    
]
