from django.shortcuts import render
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
from . import models, forms
from django.contrib.messages.views import SuccessMessageMixin
import urllib.request


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.info(
                self.request, f"안녕하세요. {self.request.user.first_name} 님. 로그인 되었습니다."
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:home")

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if self.request.user.__str__() != "AnonymousUser":
            return redirect(reverse("core:home"))

        return self.render_to_response(self.get_context_data())


def SignUpView(request):

    if request.user.__str__() != "AnonymousUser":
        return redirect(reverse("core:home"))

    form = forms.SignUpForm(request.POST or None)

    if form.is_valid():

        pw = request.POST.get("pw")
        confirm = models.Passward.objects.all()[0]
        if pw != confirm.pw:
            messages.error(request, "회사승인코드를 확인해주세요.")
            return render(request, "users/signup.html", {"form": form,},)

        form.save()
        form.save_m2m()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            name = user.first_name

            messages.success(request, f"가입되었습니다. 환영합니다. {name}님.")
        return redirect(reverse("core:home"))

    return render(request, "users/signup.html", {"form": form,},)


def log_out(request):
    logout(request)
    messages.info(request, "정상적으로 로그아웃 되었습니다.")
    return redirect(reverse("core:home"))
