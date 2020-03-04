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
from stocksingle import models as SS_models
from stockrack import models as SR_models
from orders import models as OR_models
from django.utils import timezone
from qualitycontrols import models as QC_models
from afterservices import models as AS_models
from core import views as core_views
from . import models


class stockmanageshome(core_views.twolist):
    templatename = "stockmanages/stockmanageshome.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = SS_models.StockOfSingleProductOutRequest.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.단품출하등록
                except:
                    queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = SS_models.StockOfSingleProductOutRequest.objects.filter(
                Q(출하요청자__first_name__contains=self.search)
                | Q(수주__수주코드__contains=self.search)
                | Q(수주AS__contains=self.search)
                | Q(고객사__거래처명__contains=self.search)
                | Q(단품__모델명__contains=self.search)
                | Q(단품__모델코드__contains=self.search)
                | Q(AS__AS현장방문요청__AS접수__접수번호__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.단품출하등록
                except:
                    queryset.append(s)
        return queryset

    def get_second_queryset(self, request):
        self.search2 = request.GET.get("search2")
        if self.search2 is None:
            order = SR_models.StockOfRackProductOutRequest.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.랙출하등록
                except:
                    queryset.append(s)
            self.s_bool2 = False
        else:
            self.s_bool2 = True
            order = SR_models.StockOfRackProductOutRequest.objects.filter(
                Q(출하요청자__first_name__contains=self.search2)
                | Q(고객사__거래처명__contains=self.search2)
                | Q(수주__수주코드__contains=self.search2)
                | Q(랙__랙모델명__contains=self.search2)
                | Q(랙__랙시리얼코드__contains=self.search2)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.랙출하등록
                except:
                    queryset.append(s)
        return queryset


class materialchecklist(core_views.onelist):
    templatename = "stockmanages/materialchecklist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = QC_models.MaterialCheckRegister.objects.filter(
                의뢰자=user
            ).order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                QC_models.MaterialCheckRegister.objects.filter(의뢰자=user)
                .filter(
                    Q(의뢰자__first_name__contains=self.search)
                    | Q(수입검사의뢰코드__contains=self.search)
                    | Q(자재__contains=self.search)
                    | Q(수량__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


def materialcheckdetail(request, pk):
    user = request.user
    materialcheck = QC_models.MaterialCheckRegister.objects.get_or_none(pk=pk)
    return render(
        request,
        "stockmanages/materialcheckdetail.html",
        {"materialcheck": materialcheck, "user": user,},
    )


def materialcheckrequest(request):
    search = request.GET.get("search")
    if search is None:
        material = SI_models.Material.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.Material.objects.filter(
            Q(자재코드=search)
            | Q(자재품명__contains=search)
            | Q(품목__contains=search)
            | Q(자재공급업체__거래처명__contains=search)
        ).order_by("-created")
        material = qs

    form = forms.materialcheckrequest(request.POST)
    seletelist = [
        "불량분류",
    ]
    if form.is_valid():
        수입검사의뢰코드 = form.cleaned_data.get("수입검사의뢰코드")
        수량 = form.cleaned_data.get("수량")
        자재 = form.cleaned_data.get("자재")
        mpk = int(자재)
        자재 = SI_models.Material.objects.get(pk=mpk)

        SM = QC_models.MaterialCheckRegister.objects.create(
            수입검사의뢰코드=수입검사의뢰코드, 의뢰자=request.user, 자재=자재, 수량=수량,
        )
        messages.success(request, "수입검사요청이 등록되었습니다.")
        return redirect(reverse("stockmanages:materialchecklist"))

    pagediv = 5
    totalpage = int(math.ceil(len(material) / pagediv))
    paginator = Paginator(material, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    material = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "stockmanages/materialcheckrequest.html",
        {
            "form": form,
            "material": material,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "seletelist": ["1",],
        },
    )


def materialcheckrequestdelete(request, pk):
    materialcheck = QC_models.MaterialCheckRegister.objects.get_or_none(pk=pk)
    materialcheck.delete()
    messages.success(request, "수입검사의뢰가 삭제되었습니다.")
    return redirect(reverse("stockmanages:materialchecklist"))


class materialinlist(core_views.onelist):
    templatename = "stockmanages/materialinlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = models.StockOfMaterialIn.objects.filter(입고자=user).order_by(
                "-created"
            )

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                models.StockOfMaterialIn.objects.filter(입고자=user)
                .filter(
                    Q(자재입고요청__자재__자재품명__contains=self.search)
                    | Q(입고자__first_name__contains=self.search)
                    | Q(입고유형__contains=self.search)
                    | Q(자재입고요청__자재__자재코드__contains=self.search)
                    | Q(자재입고요청__입고요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


class materialinrequestlist(core_views.onelist):
    templatename = "stockmanages/materialinrequestlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = models.StockOfMaterialInRequest.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.자재입고등록
                except:
                    queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                models.StockOfMaterialInRequest.objects.all()
                .filter(
                    Q(자재__자재품명__contains=self.search)
                    | Q(자재__자재코드__contains=self.search)
                    | Q(입고요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.자재입고등록
                except:
                    queryset.append(s)

        return queryset


def materialinregister(request, pk):
    materialinrequest = models.StockOfMaterialInRequest.objects.get_or_none(pk=pk)

    form = forms.materialinregisterForm(request.POST)

    if form.is_valid():
        입고일 = form.cleaned_data.get("입고일")
        입고수량 = form.cleaned_data.get("입고수량")
        입고유형 = form.cleaned_data.get("입고유형")
        if 입고일 is None:
            입고일 = timezone.now().date()
        SM = models.StockOfMaterialIn.objects.create(
            자재입고요청=materialinrequest, 입고자=request.user, 입고일=입고일, 입고수량=입고수량, 입고유형=입고유형,
        )
        messages.success(request, "자재입고가 완료되었습니다.")
        return redirect(reverse("stockmanages:materialinlist"))

    seletelist = [
        "입고유형",
    ]
    return render(
        request,
        "stockmanages/materialinregister.html",
        {
            "materialinrequest": materialinrequest,
            "form": form,
            "seletelist": seletelist,
        },
    )


def materialindelete(request, pk):
    materialin = models.StockOfMaterialIn.objects.get_or_none(pk=pk)
    materialin.자재입고요청.자재.자재재고.실수량 -= materialin.입고수량
    차이 = materialin.자재입고요청.입고요청수량 - materialin.입고수량
    materialin.자재입고요청.자재.자재재고.입고요청포함수량 += 차이
    materialin.자재입고요청.자재.자재재고.출고요청제외수량 -= materialin.입고수량
    materialin.자재입고요청.자재.자재재고.save()
    materialin.delete()
    messages.success(request, "자재입고가 철회되었습니다.")
    return redirect(reverse("stockmanages:materialinlist"))


class materialoutlist(core_views.onelist):
    templatename = "stockmanages/materialoutlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = models.StockOfMaterialOut.objects.filter(출고자=user).order_by(
                "-created"
            )
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                models.StockOfMaterialOut.objects.filter(출고자=user)
                .filter(
                    Q(자재출고요청__자재__자재품명__contains=self.search)
                    | Q(출고자__first_name__contains=self.search)
                    | Q(출고유형__contains=self.search)
                    | Q(자재출고요청__자재__자재코드__contains=self.search)
                    | Q(자재출고요청__출고요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


class materialoutrequestlist(core_views.onelist):
    templatename = "stockmanages/materialoutrequestlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = models.StockOfMaterialOutRequest.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.자재출고등록
                except:
                    queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = models.StockOfMaterialOutRequest.objects.filter(
                Q(자재__자재품명__contains=self.search)
                | Q(자재__자재코드__contains=self.search)
                | Q(출고요청자__first_name__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.자재출고등록
                except:
                    queryset.append(s)

        return queryset


def materialoutregister(request, pk):
    materialoutrequest = models.StockOfMaterialOutRequest.objects.get_or_none(pk=pk)

    form = forms.materialoutregisterForm(request.POST)

    if form.is_valid():
        출고일 = form.cleaned_data.get("출고일")
        출고수량 = form.cleaned_data.get("출고수량")
        출고유형 = form.cleaned_data.get("출고유형")
        if 출고일 is None:
            출고일 = timezone.now().date()
        SM = models.StockOfMaterialOut.objects.create(
            자재출고요청=materialoutrequest, 출고자=request.user, 출고일=출고일, 출고수량=출고수량, 출고유형=출고유형,
        )
        messages.success(request, "자재출고가 완료되었습니다.")
        return redirect(reverse("stockmanages:materialoutlist"))

    seletelist = [
        "출고유형",
    ]
    return render(
        request,
        "stockmanages/materialoutregister.html",
        {
            "materialoutrequest": materialoutrequest,
            "form": form,
            "seletelist": seletelist,
        },
    )


def materialoutdelete(request, pk):
    materialout = models.StockOfMaterialOut.objects.get_or_none(pk=pk)

    materialout.자재출고요청.자재.자재재고.실수량 += materialout.출고수량
    차이 = materialout.자재출고요청.출고요청수량 - materialout.출고수량
    materialout.자재출고요청.자재.자재재고.출고요청제외수량 -= 차이
    materialout.자재출고요청.자재.자재재고.입고요청포함수량 += materialout.출고수량
    materialout.자재출고요청.자재.자재재고.save()

    materialout.delete()
    messages.success(request, "자재출고가 철회되었습니다.")
    return redirect(reverse("stockmanages:materialoutlist"))


class stockofmateriallist(core_views.onelist):
    templatename = "stockmanages/stockofmateriallist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SI_models.Material.objects.all().order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = SI_models.Material.objects.filter(
                Q(자재품명__contains=self.search)
                | Q(자재코드__contains=self.search)
                | Q(단위__contains=self.search)
                | Q(규격__contains=self.search)
                | Q(자재공급업체__거래처명__contains=self.search)
            ).order_by("-created")
        return queryset


def updatestockofmaterial(request):
    search = request.GET.get("search")
    if search is None:
        material = SI_models.Material.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.Material.objects.filter(
            Q(자재코드=search)
            | Q(자재품명__contains=search)
            | Q(품목__contains=search)
            | Q(자재공급업체__거래처명__contains=search)
        ).order_by("-created")
        material = qs

    form = forms.updatestockofmaterial(request.POST)
    seletelist = [
        "불량분류",
    ]
    if form.is_valid():
        실수량 = form.cleaned_data.get("실수량")
        입고요청포함수량 = form.cleaned_data.get("입고요청포함수량")
        출고요청제외수량 = form.cleaned_data.get("출고요청제외수량")
        자재 = form.cleaned_data.get("자재")
        mpk = int(자재)
        자재 = SI_models.Material.objects.get(pk=mpk)
        try:
            stockofmatarial = 자재.자재재고
            stockofmatarial.실수량 = 실수량
            stockofmatarial.입고요청포함수량 = 입고요청포함수량
            stockofmatarial.출고요청제외수량 = 출고요청제외수량
            stockofmatarial.save()
        except:
            sm = models.StockOfMaterial.objects.create(
                자재=자재, 실수량=실수량, 입고요청포함수량=입고요청포함수량, 출고요청제외수량=출고요청제외수량,
            )

        messages.success(request, "자재재고가 최신화되었습니다.")
        return redirect(reverse("stockmanages:stockofmateriallist"))

    pagediv = 5
    totalpage = int(math.ceil(len(material) / pagediv))
    paginator = Paginator(material, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    material = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "stockmanages/updatestockofmaterial.html",
        {
            "form": form,
            "material": material,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "seletelist": ["1",],
        },
    )
