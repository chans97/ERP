import os
import requests, json
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib.messages.views import SuccessMessageMixin
import urllib.request


def firstindecide(request):
    user = request.user
    print(user.is_authenticated)

    return render(request, "users/login.html")
