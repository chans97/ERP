from django.shortcuts import render
from django.core.paginator import Paginator
import os
import requests, json
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    CreateView,
    FormView,
)

from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models, forms
from django.contrib.messages.views import SuccessMessageMixin
import urllib.request
from django.db.models import Q
from users import mixins as user_mixins
from users import models as user_models


class PartnerView(ListView):
    """HomeView Def"""

    model = models.Partner
    paginate_by = 6
    paginate_orphans = 2
    ordering = "-created"
    context_object_name = "lists"
    template_name = "Standardinformation/partner.html"


class UploadPartnerView(user_mixins.LoggedInOnlyView, FormView):
    model = models.Partner
    fields = (
        "거래처구분",
        "거래처코드",
        "거래처명",
        "사업자등록번호",
        "담당자",
        "연락처",
        "이메일",
        "사업장주소",
        "사업자등록증첨부",
        "특이사항",
        "사용여부",
    )
    template_name = "Standardinformation/partnerregister.html"
    form_class = forms.UploadRoomForm

    def form_valid(self, form):
        partner = form.save()
        user = self.request.user
        request = self.request
        print(self)
        print(user)

        partner.작성자 = user
        partner.save()
        form.save_m2m()

        messages.success(request, "거래처가 등록되었습니다.")
        return redirect(reverse("StandardInformation:partner"))

    def get(self, request, *args, **kwargs):
        user = self.request.user
        lists = models.Partner.objects.filter(작성자=user)
        form = forms.UploadRoomForm

        return render(
            request,
            "Standardinformation/partnerregister.html",
            {"lists": lists, "form": form},
        )


class PartnerSearchView(ListView):

    model = models.Partner
    paginate_by = 6
    paginate_orphans = 2
    ordering = "created"
    context_object_name = "lists"
    template_name = "Standardinformation/partnersearch.html"

    def get_queryset(self):
        r = self.request.GET.get("search")

        qs = models.Partner.objects.filter(
            Q(거래처코드=r)
            | Q(거래처구분=r)
            | Q(거래처명__contains=r)
            | Q(담당자__first_name=r)
            | Q(사업장주소__contains=r)
            | Q(작성자__first_name=r)
        )

        qs.order_by("-created")
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {"class_name": self.__class__.__name__,}
                )
        context = self.get_context_data()
        context["ss"] = request.GET.get("search")
        print(context)
        return self.render_to_response(context)

