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
from orders import models as OR_models


def ordersingleout(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="단품")
            .filter(작성자=user)
            .filter(출하구분="출하미완료")
            .order_by("-created")
        )

        s_bool = False
    else:
        s_bool = True
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="단품")
            .filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분__contains=search)
                | Q(제품구분__contains=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__랙모델명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

    pagediv = 7

    totalpage = int(math.ceil(len(order) / pagediv))
    paginator = Paginator(order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    order = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    nonpage = False
    if totalpage == 0:
        nonpage = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "stocksingle/ordersingleout.html",
        {
            "order": order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "nonpage": nonpage,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
            "None": None,
            "no": "",
        },
    )


def ordersingleoutregister(request, pk):
    form = forms.UploadSingleOutForm(request.POST)
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    user = request.user

    if form.is_valid():

        출하희망일 = form.cleaned_data.get("출하희망일")
        출하요청수량 = form.cleaned_data.get("출하요청수량")
        if order.singlestockincludeexception() < 출하요청수량:
            messages.error(request, "출하요청수량이 출하요청제외수량보다 더 많습니다.")
            return render(
                request,
                "stocksingle/ordersingleoutregister.html",
                {"form": form, "order": order, "list": order,},
            )
        elif order.needtoout() < 출하요청수량:
            messages.error(request, "출하요청수량이 남은남품수량보다 더 많습니다.")
            return render(
                request,
                "stocksingle/ordersingleoutregister.html",
                {"form": form, "order": order, "list": order,},
            )
        수주 = order
        단품 = order.단품모델
        고객사 = order.고객사명
        출하요청자 = user
        SM = models.StockOfSingleProductOutRequest.objects.create(
            출하희망일=출하희망일, 출하요청수량=출하요청수량, 수주=수주, 단품=단품, 고객사=고객사, 출하요청자=출하요청자,
        )
        messages.success(request, "출하요청 등록이 완료되었습니다.")
        return redirect(reverse("stocksingle:ordersingleout"))
    return render(
        request,
        "stocksingle/ordersingleoutregister.html",
        {"form": form, "order": order, "list": order,},
    )


def orderstocksingledelete(request, pk):
    orderstocksingle = models.StockOfSingleProductOutRequest.objects.get(pk=pk)
    order = orderstocksingle.수주
    pk = order.pk
    출하요청수량 = orderstocksingle.출하요청수량
    단품 = orderstocksingle.단품
    재고 = 단품.단품재고
    재고.출하요청제외수량 += 출하요청수량
    재고.save()

    messages.success(request, "출하요청이 철회되었습니다.")
    orderstocksingle.delete()
    return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))


def orderstocksingleedit(request, pk):
    form = forms.UploadSingleOutForm(request.POST)
    orderstocksingle = models.StockOfSingleProductOutRequest.objects.get(pk=pk)
    order = orderstocksingle.수주
    pk = order.pk
    user = request.user
    출하요청수량 = orderstocksingle.출하요청수량
    if orderstocksingle.출하희망일 is None:
        출하희망일 = ""
    else:
        출하희망일 = f"{orderstocksingle.출하희망일.year}-{orderstocksingle.출하희망일.month}-{orderstocksingle.출하희망일.day}"

    if form.is_valid():

        출하희망일f = form.cleaned_data.get("출하희망일")
        출하요청수량f = form.cleaned_data.get("출하요청수량")
        if (order.singlestockincludeexception() + 출하요청수량) < 출하요청수량f:
            messages.error(request, "출하요청수량이 출하요청제외수량보다 더 많습니다.")
            return render(
                request,
                "stocksingle/orderstocksingleedit.html",
                {
                    "form": form,
                    "order": order,
                    "list": order,
                    "single": orderstocksingle.단품,
                    "출하요청수량": 출하요청수량,
                    "출하희망일": 출하희망일,
                },
            )
        elif (order.needtoout() + 출하요청수량) < 출하요청수량f:
            messages.error(request, "출하요청수량이 남은남품수량보다 더 많습니다.")
            return render(
                request,
                "stocksingle/orderstocksingleedit.html",
                {
                    "form": form,
                    "order": order,
                    "list": order,
                    "single": orderstocksingle.단품,
                    "출하요청수량": 출하요청수량,
                    "출하희망일": 출하희망일,
                },
            )
        단품 = orderstocksingle.단품
        재고 = 단품.단품재고
        재고.출하요청제외수량 += 출하요청수량
        재고.save()

        orderstocksingle.출하희망일 = 출하희망일f
        orderstocksingle.출하요청수량 = 출하요청수량f
        orderstocksingle.save()

        messages.success(request, "출하요청 수정이 완료되었습니다.")
        return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))

    return render(
        request,
        "stocksingle/orderstocksingleedit.html",
        {
            "form": form,
            "order": order,
            "list": order,
            "single": orderstocksingle.단품,
            "출하요청수량": 출하요청수량,
            "출하희망일": 출하희망일,
        },
    )
