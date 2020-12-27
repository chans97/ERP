from django.urls import path
from . import views
from django.conf.urls import handler400, handler404, handler500

app_name = "core"

handler400 = views.bad_request_page
handler404 = views.page_not_found_page
handler500 = views.server_error_page

urlpatterns = [
    path("", views.firstindecide, name="home"),
    path("parthome/<int:pk>/", views.parthome, name="parthome"),
    path("migrate", views.migrate, name="migrate"),
    path("partnermigrate", views.partnermigrate, name="partnermigrate"),
    path("materialmigrate", views.materialmigrate, name="materialmigrate"),
    path("measuremigrate", views.measuremigrate, name="measuremigrate"),
    path("singlemigrate", views.singlemigrate, name="singlemigrate"),
    path("makeCompanyPart", views.makeCompanyPart, name="makeCompanyPart"),
    path("managehome", views.managehome, name="managehome"),
    path("totalorder", views.totalorder, name="totalorder"),
    path("orderbar", views.orderbar, name="orderbar"),
    path("outcount", views.outcount, name="outcount"),
    path("productbar", views.productbar, name="productbar"),
    path("lastchecknum", views.lastchecknum, name="lastchecknum"),
    path("incheck", views.incheck, name="incheck"),
    path("asconduct", views.asconduct, name="asconduct"),
]
