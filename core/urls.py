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
]
