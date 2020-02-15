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
from django.http import HttpResponse
import math
from StandardInformation import models as SI_models


def orderregister(request):
    form = forms.UploadOrderForm(request.POST)

    search = request.GET.get("search")
    if search is None:
        customer = SI_models.CustomerPartner.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.CustomerPartner.objects.filter(
            Q(고객작성자__first_name=search)
            | Q(거래처구분=search)
            | Q(거래처코드=search)
            | Q(거래처명__contains=search)
            | Q(고객담당자__first_name=search)
            | Q(사업장주소__contains=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        수주코드 = form.cleaned_data.get("수주코드")
        영업구분 = form.cleaned_data.get("영업구분")
        사업장구분 = form.cleaned_data.get("사업장구분")
        수주일자 = form.cleaned_data.get("수주일자")
        거래처코드 = form.cleaned_data.get("거래처코드")
        현장명 = form.cleaned_data.get("현장명")
        납품요청일 = form.cleaned_data.get("납품요청일")
        특이사항 = form.cleaned_data.get("특이사항")
        제품구분 = form.cleaned_data.get("제품구분")
        SM = models.OrderRegister.objects.create(
            수주코드=수주코드,
            영업구분=영업구분,
            사업장구분=사업장구분,
            수주일자=수주일자,
            고객사명=거래처코드,
            현장명=현장명,
            납품요청일=납품요청일,
            특이사항=특이사항,
            제품구분=제품구분,
            납품수량=0,
        )

        pk = SM.pk
        if SM.제품구분 == "단품":
            return redirect(reverse("orders:ordersingle", kwargs={"pk": pk}))
        else:
            return redirect(reverse("orders:orderrack", kwargs={"pk": pk}))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = ["제품구분", "영업구분", "사업장구분"]
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "orders/orderregister.html",
        {
            "customer": customer,
            "form": form,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "seletelist": seletelist,
        },
    )


def ordersingle(request, pk):
    form = forms.OrderSingleForm(request.POST)

    search = request.GET.get("search")
    if search is None:
        customer = SI_models.SingleProduct.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.SingleProduct.objects.filter(
            Q(모델코드=search)
            | Q(모델명__contains=search)
            | Q(규격=search)
            | Q(단위=search)
            | Q(작성자__first_name=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        단품모델코드 = form.cleaned_data.get("단품모델코드")
        납품수량 = form.cleaned_data.get("납품수량")
        SM = models.OrderRegister.objects.get(pk=pk)
        SM.단품모델 = 단품모델코드
        SM.납품수량 = 납품수량
        SM.save()

        messages.success(request, "단품수주가 등록되었습니다.")

        return redirect(reverse("core:home"))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True

    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "orders/ordersingle.html",
        {
            "customer": customer,
            "form": form,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
        },
    )


def orderrack(request, pk):
    form = forms.OrderRackForm(request.POST)

    search = request.GET.get("search")
    if search is None:
        customer = SI_models.RackProduct.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.RackProduct.objects.filter(
            Q(랙시리얼코드=search)
            | Q(랙모델명__contains=search)
            | Q(규격=search)
            | Q(단위=search)
            | Q(작성자__first_name=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        랙시리얼코드 = form.cleaned_data.get("랙시리얼코드")
        납품수량 = form.cleaned_data.get("납품수량")
        SM = models.OrderRegister.objects.get(pk=pk)
        SM.랙모델 = 랙시리얼코드
        SM.납품수량 = 납품수량
        SM.save()

        messages.success(request, "랙수주가 등록되었습니다.")

        return redirect(reverse("core:home"))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "orders/orderrack.html",
        {
            "customer": customer,
            "form": form,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
        },
    )
