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
from stocksingle import models as SS_models


@login_required
def orderrackout(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="랙")
            .filter(작성자=user)
            .filter(출하구분="출하미완료")
            .order_by("-created")
        )

        s_bool = False
    else:
        s_bool = True
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="랙")
            .filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분__contains=search)
                | Q(제품구분__contains=search)
                | Q(사업장구분__contains=search)
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
        "stockrack/orderrackout.html",
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


@login_required
def orderrackoutregister(request, pk):
    form = forms.UploadRackOutForm(request.POST)
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    user = request.user

    if form.is_valid():

        출하희망일 = form.cleaned_data.get("출하희망일")
        출하요청수량 = form.cleaned_data.get("출하요청수량")
        수취인 = form.cleaned_data.get("수취인")
        수취인주소 = form.cleaned_data.get("수취인주소")
        연락처 = form.cleaned_data.get("연락처")
        try:
            랙조립도면 = request.FILES["랙조립도면"]
        except Exception:
            랙조립도면 = None

        if order.rackstockincludeexception() < 출하요청수량:
            messages.error(request, "출하요청수량이 출하예정제외랙추정수량보다 더 많습니다.")
            return render(
                request,
                "stockrack/orderrackoutregister.html",
                {"form": form, "order": order, "list": order,},
            )
        elif order.needtooutrack() < 출하요청수량:
            messages.error(request, "출하요청수량이 남은납품수량보다 더 많습니다.")
            return render(
                request,
                "stockrack/orderrackoutregister.html",
                {"form": form, "order": order, "list": order,},
            )
        수주 = order
        랙 = order.랙모델
        고객사 = order.고객사명
        출하요청자 = user
        수주.랙조립도면 = 랙조립도면

        SM = models.StockOfRackProductOutRequest.objects.create(
            출하희망일=출하희망일,
            출하요청수량=출하요청수량,
            수주=수주,
            랙=랙,
            고객사=고객사,
            출하요청자=출하요청자,
            수취인=수취인,
            수취인주소=수취인주소,
            연락처=연락처,
        )
        messages.success(request, "출하요청 등록이 완료되었습니다.")
        return redirect(reverse("stockrack:orderrackout"))
    return render(
        request,
        "stockrack/orderrackoutregister.html",
        {"form": form, "order": order, "list": order,},
    )


@login_required
def orderstockrackdelete(request, pk):
    orderstockrack = models.StockOfRackProductOutRequest.objects.get(pk=pk)
    order = orderstockrack.수주
    pk = order.pk
    출하요청수량 = orderstockrack.출하요청수량
    for com in orderstockrack.랙.랙구성단품.all():
        if com.랙구성 == "자재":
            num = com.수량
            material = com.랙구성자재
            realnum = 출하요청수량 * num
            material.자재재고.출고요청제외수량 += realnum
            material.자재재고.save()
        else:
            num = com.수량
            single = com.랙구성단품
            realnum = 출하요청수량 * num
            single.단품재고.출하요청제외수량 += realnum
            single.단품재고.save()
    orderstockrack.delete()
    messages.success(request, "출하요청이 철회되었습니다.")

    return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))


@login_required
def orderstockrackedit(request, pk):

    form = forms.UploadRackOutForm(request.POST)
    orderstockrack = models.StockOfRackProductOutRequest.objects.get(pk=pk)
    order = orderstockrack.수주
    pk = order.pk
    user = request.user
    출하요청수량 = orderstockrack.출하요청수량
    수취인 = orderstockrack.수취인
    수취인주소 = orderstockrack.수취인주소
    연락처 = orderstockrack.연락처
    if orderstockrack.출하희망일 is None:
        출하희망일 = ""
    else:
        출하희망일 = f"{orderstockrack.출하희망일.year}-{orderstockrack.출하희망일.month}-{orderstockrack.출하희망일.day}"

    if form.is_valid():

        출하희망일f = form.cleaned_data.get("출하희망일")
        출하요청수량f = form.cleaned_data.get("출하요청수량")
        수취인f = form.cleaned_data.get("수취인")
        수취인주소f = form.cleaned_data.get("수취인주소")
        연락처f = form.cleaned_data.get("연락처")

        if (order.rackstockincludeexception() + 출하요청수량) < 출하요청수량f:
            messages.error(request, "출하요청수량이 출하예정제외랙추정수량보다 더 많습니다.")
            return render(
                request,
                "stockrack/orderstockrackedit.html",
                {
                    "form": form,
                    "order": order,
                    "list": order,
                    "출하요청수량": 출하요청수량,
                    "출하희망일": 출하희망일,
                    "수취인": 수취인,
                    "수취인주소": 수취인주소,
                    "연락처": 연락처,
                    "rack": orderstockrack.랙,
                },
            )

        elif (order.needtooutrack() + 출하요청수량) < 출하요청수량f:
            messages.error(request, "출하요청수량이 남은남품수량보다 더 많습니다.")
            return render(
                request,
                "stockrack/orderstockrackedit.html",
                {
                    "form": form,
                    "order": order,
                    "list": order,
                    "출하요청수량": 출하요청수량,
                    "출하희망일": 출하희망일,
                    "수취인": 수취인,
                    "수취인주소": 수취인주소,
                    "연락처": 연락처,
                    "rack": orderstockrack.랙,
                },
            )
        for com in orderstockrack.랙.랙구성단품.all():
            if com.랙구성 == "자재":
                num = com.수량
                material = com.랙구성자재
                realnum = (출하요청수량 - 출하요청수량f) * num
                material.자재재고.출고요청제외수량 += realnum
                material.자재재고.save()
            else:
                num = com.수량
                single = com.랙구성단품
                realnum = (출하요청수량 - 출하요청수량f) * num
                single.단품재고.출하요청제외수량 += realnum
                single.단품재고.save()

        orderstockrack.출하희망일 = 출하희망일f
        orderstockrack.출하요청수량 = 출하요청수량f
        orderstockrack.수취인 = 수취인f
        orderstockrack.수취인주소 = 수취인주소f
        orderstockrack.연락처 = 연락처f
        orderstockrack.save()

        messages.success(request, "출하요청 수정이 완료되었습니다.")
        return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))

    return render(
        request,
        "stockrack/orderstockrackedit.html",
        {
            "form": form,
            "order": order,
            "list": order,
            "출하요청수량": 출하요청수량,
            "출하희망일": 출하희망일,
            "rack": orderstockrack.랙,
            "수취인": 수취인,
            "수취인주소": 수취인주소,
            "연락처": 연락처,
        },
    )


@login_required
def ordersingledfrackinregister(request, pk):
    form = forms.UploadSingleInForm(request.POST)
    outrequest = models.StockOfRackProductOutRequest.objects.get_or_none(pk=pk)
    order = outrequest.수주
    user = request.user
    rack = order.랙모델

    singleofrack = []
    for com in rack.랙구성단품.all():
        if com.랙구성 == "자재":
            pass
        else:
            num = com.수량
            single = com.랙구성단품
            singleofrack.append(single)

    if form.is_valid():

        입고요청수량 = form.cleaned_data.get("입고요청수량")
        입고요청일 = form.cleaned_data.get("입고요청일")
        단품 = form.cleaned_data.get("단품")

        수주 = order
        고객사 = order.고객사명
        출하요청자 = user
        SM = SS_models.StockOfSingleProductInRequest.objects.create(
            수주=수주, 랙출하요청=outrequest, 단품=단품, 입고요청수량=입고요청수량, 입고요청자=user, 입고요청일=입고요청일
        )
        messages.success(request, "반품요청 등록이 완료되었습니다.")
        pk = 수주.pk
        return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))
    return render(
        request,
        "stockrack/ordersingledfrackinregister.html",
        {
            "form": form,
            "order": order,
            "list": order,
            "outrequest": outrequest,
            "singleofrack": singleofrack,
        },
    )
