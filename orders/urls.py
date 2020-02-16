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
]
