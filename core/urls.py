from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.firstindecide, name="home"),
    path("parthome/<int:pk>/", views.parthome, name="parthome"),
    
]
