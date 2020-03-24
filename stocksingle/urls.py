from django.urls import path
from . import views

app_name = "stocksingle"

urlpatterns = [
    path("ordersingleout/", views.ordersingleout, name="ordersingleout"),
    path(
        "ordersingleoutregister/<int:pk>/",
        views.ordersingleoutregister,
        name="ordersingleoutregister",
    ),
    path(
        "orderstocksingledelete/<int:pk>/",
        views.orderstocksingledelete,
        name="orderstocksingledelete",
    ),
    path(
        "orderstocksingleedit/<int:pk>/",
        views.orderstocksingleedit,
        name="orderstocksingleedit",
    ),
    path(
        "ordersingleinregister/<int:pk>/",
        views.ordersingleinregister,
        name="ordersingleinregister",
    ),
    path(
        "orderstocksinglebackdelete/<int:pk>/",
        views.orderstocksinglebackdelete,
        name="orderstocksinglebackdelete",
    ),
    
]
