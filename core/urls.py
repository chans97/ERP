from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.firstindecide, name="home"),
    path("parthome/<int:pk>/", views.parthome, name="parthome"),
    path("migrate", views.migrate, name="migrate"),
    path("partnermigrate", views.partnermigrate, name="partnermigrate"),
    path("materialmigrate", views.materialmigrate, name="materialmigrate"),
    path("measuremigrate", views.measuremigrate, name="measuremigrate"),
    path("managehome", views.managehome, name="managehome"),
    path("totalorder", views.totalorder, name="totalorder"),
    path("orderbar", views.orderbar, name="orderbar"),
    path("outcount", views.outcount, name="outcount"),
    path("productbar", views.productbar, name="productbar"),
    path("lastchecknum", views.lastchecknum, name="lastchecknum"),
    path("incheck", views.incheck, name="incheck"),
    path("asconduct", views.asconduct, name="asconduct"),
]
