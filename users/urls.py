from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView, name="signup"),
    path("logout/", views.log_out, name="logout"),
    path("forgotemail/", views.forgotemail, name="forgotemail"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path("setpassword/<int:pk>/", views.setpassword, name="setpassword"),
]
