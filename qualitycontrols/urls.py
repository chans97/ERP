from django.urls import path
from . import views

app_name = "qualitycontrols"

urlpatterns = [
    path("qualitycontrolshome/", views.qualitycontrolshome, name="qualitycontrolshome"),
]
