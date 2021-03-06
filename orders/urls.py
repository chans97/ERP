from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("ordershome/", views.ordershome, name="ordershome"),
    path("orderregister/", views.orderregister, name="orderregister"),
    path("ordersingle/<int:pk>/", views.ordersingle, name="ordersingle"),
    path("orderrack/<int:pk>/", views.orderrack, name="orderrack"),
    path("orderdetail/<int:pk>/", views.OrderDetail.as_view(), name="orderdetail"),
    path("orderedit/<int:pk>/", views.orderedit, name="orderedit"),
    path("ordersingleedit/<int:pk>/", views.ordersingleedit, name="ordersingleedit"),
    path("orderrackedit/<int:pk>/", views.orderrackedit, name="orderrackedit"),
    path(
        "orderdeleteensure/<int:pk>/",
        views.orderdeleteensure,
        name="orderdeleteensure",
    ),
    path("orderdelete/<int:pk>/", views.orderdelete, name="orderdelete",),
    path("orderproduce/", views.orderproduce, name="orderproduce"),
    path(
        "orderproduceregister/<int:pk>/",
        views.orderproduceregister,
        name="orderproduceregister",
    ),
    path(
        "orderproduceedit/<int:pk>/", views.orderproduceedit, name="orderproduceedit",
    ),
    path(
        "orderproducedeleteensure/<int:pk>/",
        views.orderproducedeleteensure,
        name="orderproducedeleteensure",
    ),
    path(
        "orderproducedelete/<int:pk>/",
        views.orderproducedelete,
        name="orderproducedelete",
    ),
    path("endorder/", views.endorder, name="endorder"),
    path("endorderforout/<int:pk>/", views.endorderforout, name="endorderforout",),
    path(
        "endorderforoutforstock/<int:pk>/",
        views.endorderforoutforstock,
        name="endorderforoutforstock",
    ),
    path("endorderlist/", views.endorderlist, name="endorderlist"),
    path("endorderforin/<int:pk>/", views.endorderforin, name="endorderforin",),
    path(
        "orderproduceforrack/", views.orderproduceforrack, name="orderproduceforrack",
    ),
    path(
        "informationforrackproduce/<int:pk>/",
        views.informationforrackproduce,
        name="informationforrackproduce",
    ),
    path(
        "producesingleforrack/<int:pk>/<int:spk>/",
        views.producesingleforrack,
        name="producesingleforrack",
    ),
    path(
        "blueprintdownload/<int:pk>/",
        views.blueprintdownload,
        name="blueprintdownload",
    ),
    
]
