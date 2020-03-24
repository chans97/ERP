from django.urls import path
from . import views

app_name = "stockrack"

urlpatterns = [
    path("orderrackout/", views.orderrackout, name="orderrackout"),
    path(
        "orderrackoutregister/<int:pk>/",
        views.orderrackoutregister,
        name="orderrackoutregister",
    ),   
    path(
        "orderstockrackdelete/<int:pk>/",
        views.orderstockrackdelete,
        name="orderstockrackdelete",
    ),
    path(
        "orderstockrackedit/<int:pk>/",
        views.orderstockrackedit,
        name="orderstockrackedit",
    ),
    path(
        "ordersingledfrackinregister/<int:pk>/",
        views.ordersingledfrackinregister,
        name="ordersingledfrackinregister",
    ),
]
