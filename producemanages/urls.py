from django.urls import path
from . import views

app_name = "producemanages"

urlpatterns = [
    path("producemanageshome/", views.producemanageshome, name="producemanageshome"),
]
