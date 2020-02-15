from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("orderregister/", views.orderregister, name="orderregister"),
    path("ordersingle/<int:pk>/", views.ordersingle, name="ordersingle"),
    path("orderrack/<int:pk>/", views.orderrack, name="orderrack"),
]
