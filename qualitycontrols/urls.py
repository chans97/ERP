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
    path(
        "checkmeasurelist/", views.checkmeasurelist.as_view(), name="checkmeasurelist",
    ),
    path("measuredetail/<int:pk>/", views.measuredetail, name="measuredetail",),
    path("file_download/<int:pk>/", views.file_download, name="file_download",),
    path("measureedit/<int:pk>/", views.measureedit.as_view(), name="measureedit",),
    path(
        "measuredeleteensure/<int:pk>/",
        views.measuredeleteensure,
        name="measuredeleteensure",
    ),
    path("measuredelete/<int:pk>/", views.measuredelete, name="measuredelete",),
    path(
        "measurecheckdetail/<int:pk>/",
        views.measurecheckdetail,
        name="measurecheckdetail",
    ),
    path(
        "measurecheckedit/<int:pk>/",
        views.measurecheckedit.as_view(),
        name="measurecheckedit",
    ),
    path(
        "measurecheckdeleteensure/<int:pk>/",
        views.measurecheckdeleteensure,
        name="measurecheckdeleteensure",
    ),
    path(
        "measurecheckdelete/<int:pk>/",
        views.measurecheckdelete,
        name="measurecheckdelete",
    ),
    path(
        "measurecheckdetailregister/",
        views.measurecheckdetailregister,
        name="measurecheckdetailregister",
    ),
    path(
        "repairmeasurelist/",
        views.repairmeasurelist.as_view(),
        name="repairmeasurelist",
    ),
    path(
        "measurerepairdetail/<int:pk>/",
        views.measurerepairdetail,
        name="measurerepairdetail",
    ),
    path(
        "measurerepairedit/<int:pk>/",
        views.measurerepairedit.as_view(),
        name="measurerepairedit",
    ),
    path(
        "measurerepairdeleteensure/<int:pk>/",
        views.measurerepairdeleteensure,
        name="measurerepairdeleteensure",
    ),
    path(
        "measurerepairdelete/<int:pk>/",
        views.measurerepairdelete,
        name="measurerepairdelete",
    ),
    path(
        "file_downloadforrepair/<int:pk>/",
        views.file_downloadforrepair,
        name="file_downloadforrepair",
    ),
    path(
        "measurerepairdetailregister/",
        views.measurerepairdetailregister,
        name="measurerepairdetailregister",
    ),
    path("measurelist/", views.measurelist.as_view(), name="measurelist",),
    path(
        "measuredetailregister/",
        views.measuredetailregister,
        name="measuredetailregister",
    ),
    path(
        "specialregisterlist/",
        views.specialregisterlist.as_view(),
        name="specialregisterlist",
    ),
    path(
        "specialrequestlist/",
        views.specialrequestlist.as_view(),
        name="specialrequestlist",
    ),
    path("specialregister/<int:pk>/", views.specialregister, name="specialregister",),
    path("specialdetail/<int:pk>/", views.specialdetail, name="specialdetail",),
    path(
        "file_download_special/<int:pk>/",
        views.file_download_special,
        name="file_download_special",
    ),
    path(
        "specialconductdelete/<int:pk>/",
        views.specialconductdelete,
        name="specialconductdelete",
    ),
    path(
        "specialconductregister/<int:pk>/",
        views.specialconductregister,
        name="specialconductregister",
    ),
    path(
        "specialrejectdelete/<int:pk>/",
        views.specialrejectdelete,
        name="specialrejectdelete",
    ),
    path(
        "specialrejectregister/<int:pk>/",
        views.specialrejectregister,
        name="specialrejectregister",
    ),
    path(
        "specialconductlist/",
        views.specialconductlist.as_view(),
        name="specialconductlist",
    ),
    path(
        "finalcheckregisternotin/<int:pk>/",
        views.finalcheckregisternotin,
        name="finalcheckregisternotin",
    ),
    path("materialoutrequest/", views.materialoutrequest, name="materialoutrequest",),
    path(
        "managematerialoutrequest/",
        views.managematerialoutrequest.as_view(),
        name="managematerialoutrequest",
    ),
    path(
        "deletematerialoutrequest/<int:pk>/",
        views.deletematerialoutrequest,
        name="deletematerialoutrequest",
    ),
    path("ASrequestlist/", views.ASrequestlist, name="ASrequestlist",),
    path(
        "repairregisterAS/<int:pk>/", views.repairregisterAS, name="repairregisterAS",
    ),
    path(
        "repairrequestdetail/<int:pk>/",
        views.repairrequestdetail,
        name="repairrequestdetail",
    ),
    path("repairlist/", views.repairlist, name="repairlist",),
    path("AStotalregister/<int:pk>/", views.AStotalregister, name="AStotalregister",),
    path("AStotaledit/<int:pk>/", views.AStotaledit, name="AStotaledit",),
    path(
        "AStotaldeleteensure/<int:pk>/",
        views.AStotaldeleteensure,
        name="AStotaldeleteensure",
    ),
    path("AStotaldelete/<int:pk>/", views.AStotaldelete, name="AStotaldelete",),
    path(
        "file_download_forlow/<int:pk>/",
        views.file_download_forlow,
        name="file_download_forlow",
    ),
]
