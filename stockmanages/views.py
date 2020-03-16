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
from django.http import FileResponse
import math
from StandardInformation import models as SI_models
from stocksingle import models as SS_models
from stockrack import models as SR_models
from orders import models as OR_models
from django.utils import timezone
from qualitycontrols import models as QC_models
from afterservices import models as AS_models
from core import views as core_views
from StandardInformation import forms as SI_forms
from . import models
import urllib
from random import randint


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

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "MC" + num
            obj = QC_models.MaterialCheckRegister.objects.get_or_none(수입검사의뢰코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.materialcheckrequest(request.POST)
    code = give_number()
    form.initial = {
        "수입검사의뢰코드": code,
    }

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
    seletelist = [
        "출고유형",
    ]

    if form.is_valid():
        출고일 = form.cleaned_data.get("출고일")
        출고수량 = form.cleaned_data.get("출고수량")
        출고유형 = form.cleaned_data.get("출고유형")
        if 출고일 is None:
            출고일 = timezone.now().date()
        if 출고수량 > materialoutrequest.자재.자재재고.실수량:
            messages.error(request, "출고수량이 실수량보다 더 많습니다.")
            return render(
                request,
                "stockmanages/materialoutregister.html",
                {
                    "materialoutrequest": materialoutrequest,
                    "form": form,
                    "seletelist": seletelist,
                },
            )
        SM = models.StockOfMaterialOut.objects.create(
            자재출고요청=materialoutrequest, 출고자=request.user, 출고일=출고일, 출고수량=출고수량, 출고유형=출고유형,
        )
        messages.success(request, "자재출고가 완료되었습니다.")
        return redirect(reverse("stockmanages:materialoutlist"))

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


class singleinlist(core_views.onelist):
    templatename = "stockmanages/singleinlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SS_models.StockOfSingleProductIn.objects.filter(
                입고자=user
            ).order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                SS_models.StockOfSingleProductIn.objects.filter(입고자=user)
                .filter(
                    Q(단품입고요청__단품__모델명__contains=self.search)
                    | Q(입고자__first_name__contains=self.search)
                    | Q(단품입고요청__단품__모델코드__contains=self.search)
                    | Q(단품입고요청__입고요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


def singleindelete(request, pk):
    singlein = SS_models.StockOfSingleProductIn.objects.get_or_none(pk=pk)
    singlein.단품입고요청.단품.단품재고.실수량 -= singlein.입고수량
    차이 = singlein.단품입고요청.입고요청수량 - singlein.입고수량
    singlein.단품입고요청.단품.단품재고.입고요청포함수량 += 차이
    singlein.단품입고요청.단품.단품재고.출하요청제외수량 -= singlein.입고수량
    singlein.단품입고요청.단품.단품재고.save()
    singlein.delete()
    messages.success(request, "단품입고가 철회되었습니다.")
    return redirect(reverse("stockmanages:singleinlist"))


class singleinrequestlist(core_views.onelist):
    templatename = "stockmanages/singleinrequestlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = SS_models.StockOfSingleProductInRequest.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.단품입고등록
                except:
                    queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                SS_models.StockOfSingleProductInRequest.objects.all()
                .filter(
                    Q(단품__모델명__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(입고요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.단품입고등록
                except:
                    queryset.append(s)

        return queryset


def singleinregister(request, pk):
    singleinrequest = SS_models.StockOfSingleProductInRequest.objects.get_or_none(pk=pk)

    form = forms.singleinregisterForm(request.POST)
    now = timezone.now().date()
    form.initial = {"입고일": now}

    if form.is_valid():
        입고일 = form.cleaned_data.get("입고일")
        입고수량 = form.cleaned_data.get("입고수량")
        if 입고일 is None:
            입고일 = timezone.now().date()
        SM = SS_models.StockOfSingleProductIn.objects.create(
            단품입고요청=singleinrequest, 입고자=request.user, 입고일=입고일, 입고수량=입고수량,
        )
        messages.success(request, "단품입고가 완료되었습니다.")
        return redirect(reverse("stockmanages:singleinlist"))

    seletelist = [
        "입고유형",
    ]
    return render(
        request,
        "stockmanages/singleinregister.html",
        {
            "singleinrequest": singleinrequest,
            "form": form,
            "seletelist": seletelist,
            "now": now,
        },
    )


class singleoutlist(core_views.onelist):
    templatename = "stockmanages/singleoutlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SS_models.StockOfSingleProductOut.objects.filter(
                출하자=user
            ).order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                SS_models.StockOfSingleProductOut.objects.filter(출하자=user)
                .filter(
                    Q(단품출하요청__단품__모델명__contains=self.search)
                    | Q(출하자__first_name__contains=self.search)
                    | Q(단품출하요청__단품__모델코드__contains=self.search)
                    | Q(단품출하요청__출하요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


def dealdownload(request, pk):
    """파일 다운로드 유니코드화 패치"""
    partner = SS_models.StockOfSingleProductOut.objects.get_or_none(pk=pk)
    filepath = partner.거래명세서첨부.path
    title = partner.거래명세서첨부.path.__str__()
    title = urllib.parse.quote(title.encode("utf-8"))
    title = title.replace("C%3A%5Capps%5Cmysite%5Cuploads%5Cdeal%5C", "")

    with open(filepath, "rb") as f:
        response = HttpResponse(f, content_type="application/force-download")
        titling = 'attachment; filename="{}"'.format(title)
        response["Content-Disposition"] = titling
        return response


def singleoutdelete(request, pk):
    singleout = SS_models.StockOfSingleProductOut.objects.get_or_none(pk=pk)

    singleout.단품출하요청.단품.단품재고.실수량 += singleout.출하수량
    차이 = singleout.단품출하요청.출하요청수량 - singleout.출하수량
    singleout.단품출하요청.단품.단품재고.출하요청제외수량 -= 차이
    singleout.단품출하요청.단품.단품재고.입고요청포함수량 += singleout.출하수량
    singleout.단품출하요청.단품.단품재고.save()

    singleout.delete()
    messages.success(request, "단품출하가 철회되었습니다.")
    return redirect(reverse("stockmanages:singleoutlist"))


class singleoutrequestlist(core_views.onelist):
    templatename = "stockmanages/singleoutrequestlist.html"

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
                Q(단품__모델명__contains=self.search)
                | Q(단품__모델코드__contains=self.search)
                | Q(출하요청자__first_name__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.단품출하등록
                except:
                    queryset.append(s)

        return queryset


def singleoutregister(request, pk):
    singleoutrequest = SS_models.StockOfSingleProductOutRequest.objects.get_or_none(
        pk=pk
    )

    form = forms.singleoutregisterForm(request.POST)
    seletelist = [
        "출고유형",
    ]
    if form.is_valid():
        출하일 = form.cleaned_data.get("출하일")
        출하수량 = form.cleaned_data.get("출하수량")
        try:
            거래명세서첨부 = request.FILES["거래명세서첨부"]

        except Exception:
            거래명세서첨부 = None

        if 출하일 is None:
            출하일 = timezone.now().date()
        if 출하수량 > singleoutrequest.단품.단품재고.실수량:
            messages.error(request, "출하수량이 실수량보다 더 많습니다.")
            return render(
                request,
                "stockmanages/singleoutregister.html",
                {
                    "singleoutrequest": singleoutrequest,
                    "form": form,
                    "seletelist": seletelist,
                },
            )
        SM = SS_models.StockOfSingleProductOut.objects.create(
            단품출하요청=singleoutrequest,
            출하자=request.user,
            출하일=출하일,
            출하수량=출하수량,
            거래명세서첨부=거래명세서첨부,
        )
        messages.success(request, "단품출하가 완료되었습니다.")
        return redirect(reverse("stockmanages:singleoutlist"))

    return render(
        request,
        "stockmanages/singleoutregister.html",
        {"singleoutrequest": singleoutrequest, "form": form, "seletelist": seletelist,},
    )


class stockofsinglelist(core_views.onelist):
    templatename = "stockmanages/stockofsinglelist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SI_models.SingleProduct.objects.all().order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = SI_models.SingleProduct.objects.filter(
                Q(모델코드__contains=self.search)
                | Q(모델명__contains=self.search)
                | Q(규격__contains=self.search)
                | Q(단위__contains=self.search)
                | Q(단가__contains=self.search)
            ).order_by("-created")
        return queryset


def updatestockofsingle(request):
    search = request.GET.get("search")
    if search is None:
        single = SI_models.SingleProduct.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.SingleProduct.objects.filter(
            Q(모델코드__contains=search)
            | Q(모델명__contains=search)
            | Q(규격__contains=search)
            | Q(단위__contains=search)
            | Q(단가__contains=search)
        ).order_by("-created")
        single = qs

    form = forms.updatestockofsingle(request.POST)
    seletelist = [
        "불량분류",
    ]
    if form.is_valid():
        실수량 = form.cleaned_data.get("실수량")
        입고요청포함수량 = form.cleaned_data.get("입고요청포함수량")
        출하요청제외수량 = form.cleaned_data.get("출하요청제외수량")
        단품 = form.cleaned_data.get("단품")
        mpk = int(단품)
        단품 = SI_models.SingleProduct.objects.get(pk=mpk)
        try:
            stockofmatarial = 단품.단품재고
            stockofmatarial.실수량 = 실수량
            stockofmatarial.입고요청포함수량 = 입고요청포함수량
            stockofmatarial.출하요청제외수량 = 출하요청제외수량
            stockofmatarial.save()
        except:
            sm = SS_models.StockOfSingleProduct.objects.create(
                단품=단품, 실수량=실수량, 입고요청포함수량=입고요청포함수량, 출하요청제외수량=출하요청제외수량,
            )

        messages.success(request, "단품재고가 최신화되었습니다.")
        return redirect(reverse("stockmanages:stockofsinglelist"))

    pagediv = 5
    totalpage = int(math.ceil(len(single) / pagediv))
    paginator = Paginator(single, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    single = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "stockmanages/updatestockofsingle.html",
        {
            "form": form,
            "single": single,
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


class rackoutlist(core_views.onelist):
    templatename = "stockmanages/rackoutlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SR_models.StockOfRackProductOut.objects.filter(
                출하자=user
            ).order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                SR_models.StockOfRackProductOut.objects.filter(출하자=user)
                .filter(
                    Q(랙출하요청__랙__랙모델명__contains=self.search)
                    | Q(출하자__first_name__contains=self.search)
                    | Q(랙출하요청__랙__랙시리얼코드__contains=self.search)
                    | Q(랙출하요청__출하요청자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


def dealdownloadforrack(request, pk):
    """파일 다운로드 유니코드화 패치"""
    partner = SR_models.StockOfRackProductOut.objects.get_or_none(pk=pk)
    filepath = partner.거래명세서첨부.path
    title = partner.거래명세서첨부.path.__str__()
    title = urllib.parse.quote(title.encode("utf-8"))
    title = title.replace("C%3A%5Capps%5Cmysite%5Cuploads%5Cdeal%5C", "")

    with open(filepath, "rb") as f:
        response = HttpResponse(f, content_type="application/force-download")
        titling = 'attachment; filename="{}"'.format(title)
        response["Content-Disposition"] = titling
        return response


def rackoutdelete(request, pk):
    rackout = SR_models.StockOfRackProductOut.objects.get_or_none(pk=pk)
    try:
        for com in rackout.랙출하요청.랙.랙구성단품.all():
            if com.랙구성 == "자재":
                num = com.수량
                single = com.랙구성자재
                출하자재수량 = num * rackout.출하수량
                출하요청자재수량 = num * rackout.랙출하요청.출하요청수량
                single.자재재고.실수량 += 출하자재수량
                차이 = 출하요청자재수량 - 출하자재수량
                single.자재재고.출고요청제외수량 -= 차이
                single.자재재고.입고요청포함수량 += 출하자재수량
                single.자재재고.save()
            else:
                num = com.수량
                single = com.랙구성단품
                출하단품수량 = num * rackout.출하수량
                출하요청단품수량 = num * rackout.랙출하요청.출하요청수량
                single.단품재고.실수량 += 출하단품수량
                차이 = 출하요청단품수량 - 출하단품수량
                single.단품재고.출하요청제외수량 -= 차이
                single.단품재고.입고요청포함수량 += 출하단품수량
                single.단품재고.save()
    except:
        pass

    rackout.delete()
    messages.success(request, "랙출하가 철회되었습니다.")
    return redirect(reverse("stockmanages:rackoutlist"))


class rackoutrequestlist(core_views.onelist):
    templatename = "stockmanages/rackoutrequestlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = SR_models.StockOfRackProductOutRequest.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.랙출하등록
                except:
                    queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = SR_models.StockOfRackProductOutRequest.objects.filter(
                Q(랙__랙모델명__contains=self.search)
                | Q(랙__랙시리얼코드__contains=self.search)
                | Q(출하요청자__first_name__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.단품출하등록
                except:
                    queryset.append(s)

        return queryset


def rackoutregister(request, pk):
    rackoutrequest = SR_models.StockOfRackProductOutRequest.objects.get_or_none(pk=pk)

    form = forms.rackoutregisterForm(request.POST)
    seletelist = [
        "출고유형",
    ]
    if form.is_valid():
        출하일 = form.cleaned_data.get("출하일")
        출하수량 = form.cleaned_data.get("출하수량")
        try:
            거래명세서첨부 = request.FILES["거래명세서첨부"]

        except Exception:
            거래명세서첨부 = None

        if 출하일 is None:
            출하일 = timezone.now().date()
        if 출하수량 > rackoutrequest.rackstock():
            messages.error(request, "출하수량이 실수량보다 더 많습니다.")
            return render(
                request,
                "stockmanages/rackoutregister.html",
                {
                    "rackoutrequest": rackoutrequest,
                    "form": form,
                    "seletelist": seletelist,
                },
            )
        SM = SR_models.StockOfRackProductOut.objects.create(
            랙출하요청=rackoutrequest, 출하자=request.user, 출하일=출하일, 출하수량=출하수량, 거래명세서첨부=거래명세서첨부,
        )
        messages.success(request, "랙출하가 완료되었습니다.")
        return redirect(reverse("stockmanages:rackoutlist"))

    return render(
        request,
        "stockmanages/rackoutregister.html",
        {"rackoutrequest": rackoutrequest, "form": form, "seletelist": seletelist,},
    )


class stockofracklist(core_views.onelist):
    templatename = "stockmanages/stockofracklist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SI_models.RackProduct.objects.all().order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = SI_models.RackProduct.objects.filter(
                Q(랙시리얼코드__contains=self.search)
                | Q(랙모델명__contains=self.search)
                | Q(규격__contains=self.search)
                | Q(단위__contains=self.search)
                | Q(단가__contains=self.search)
            ).order_by("-created")
        return queryset


def informationforrack(request, pk):
    rack = SI_models.RackProduct.objects.get_or_none(pk=pk)
    single = rack.랙구성단품.filter(랙구성="단품")
    material = rack.랙구성단품.filter(랙구성="자재")

    user = request.user
    return render(
        request,
        "stockmanages/informationforrack.html",
        {"material": material, "rack": rack, "user": user, "single": single,},
    )


class singleStandarInformation(core_views.onelist):
    templatename = "stockmanages/singleStandarInformation.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SI_models.SingleProduct.objects.all().order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = SI_models.SingleProduct.objects.filter(
                Q(모델코드__contains=self.search)
                | Q(모델명__contains=self.search)
                | Q(규격__contains=self.search)
                | Q(단위__contains=self.search)
                | Q(작성자__first_name__contains=self.search)
            ).order_by("-created")
        return queryset


def singleregister(request):
    def give_number():
        while True:
            start_code = "SP"
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = start_code + num
            obj = SI_models.SingleProduct.objects.get_or_none(모델코드=code)
            if obj:
                pass
            else:
                return code

    form = SI_forms.UploadSingleForm(request.POST)
    code = give_number()
    form.initial = {
        "모델코드": code,
    }

    if form.is_valid():
        single = form.save()
        single.작성자 = request.user
        single.save()
        form.save_m2m()
        pk = single.pk

        messages.success(request, "해당 단품에 포함되는 자재를 추가해주세요.")
        return redirect(reverse("stockmanages:singlematerial", kwargs={"pk": pk}))
    return render(request, "stockmanages/singleregister.html", {"form": form,},)


def singlematerial(request, pk):
    single = SI_models.SingleProduct.objects.get(pk=pk)
    form = SI_forms.UploadSingleMaterialForm(request.POST)

    search = request.GET.get("search")
    if search is None:
        material = SI_models.Material.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = models.Material.objects.filter(
            Q(자재코드=search)
            | Q(자재품명__contains=search)
            | Q(품목__contains=search)
            | Q(자재공급업체__거래처명__contains=search)
        ).order_by("-created")
        material = qs

    if form.is_valid():
        단품구성자재 = form.cleaned_data.get("단품구성자재")
        수량 = form.cleaned_data.get("수량")
        SM = SI_models.SingleProductMaterial.objects.create(
            단품모델=single, 단품구성자재=단품구성자재, 수량=수량
        )

    pagediv = 7
    totalpage = int(math.ceil(len(material) / pagediv))
    paginator = Paginator(material, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    material = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    materialofsingle = single.단품구성자재.all()
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "stockmanages/singlematerial.html",
        {
            "single": single,
            "form": form,
            "material": material,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "materialofsingle": materialofsingle,
        },
    )


def donesingleregister(request):
    messages.success(request, "단품이 기준정보에 등록되었습니다.")

    return redirect(reverse("stockmanages:singleStandarInformation"))


class SingleDetialView(user_mixins.LoggedInOnlyView, DetailView):
    model = SI_models.SingleProduct

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        single = SI_models.SingleProduct.objects.get(pk=pk)

        material = single.단품구성자재.all()
        user = request.user
        return render(
            request,
            "stockmanages/singledetail.html",
            {"single": single, "user": user, "material": material},
        )


class singleedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = SI_models.SingleProduct
    fields = (
        "모델코드",
        "모델명",
        "규격",
        "단위",
        "단가",
    )
    template_name = "stockmanages/singleedit.html"

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse("stockmanages:singlematerial", kwargs={"pk": pk})


def singledeleteensure(request, pk):

    single = SI_models.SingleProduct.objects.get_or_none(pk=pk)
    return render(request, "stockmanages/singledeleteensure.html", {"single": single},)


def singledelete(request, pk):
    single = SI_models.SingleProduct.objects.get_or_none(pk=pk)
    single.delete()

    messages.success(request, "해당 단품이 삭제되었습니다.")

    return redirect(reverse("stockmanages:singleStandarInformation"))


def deletematerialofsingle(request, pk, m_pk):

    materialofsingle = SI_models.SingleProductMaterial.objects.get(pk=m_pk)
    materialofsingle.delete()
    return redirect(reverse("stockmanages:singlematerial", kwargs={"pk": pk}))


class materialStandarInformation(core_views.onelist):
    templatename = "stockmanages/materialStandarInformation.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SI_models.Material.objects.all().order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = SI_models.Material.objects.filter(
                Q(자재코드__contains=self.search)
                | Q(품목__contains=self.search)
                | Q(규격__contains=self.search)
                | Q(단위__contains=self.search)
                | Q(자재품명__contains=self.search)
                | Q(자재공급업체__거래처명__contains=self.search)
            ).order_by("-created")
        return queryset


def materialregister(request):
    def give_number():
        while True:
            start_code = "MT"
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = start_code + num
            obj = SI_models.Material.objects.get_or_none(자재코드=code)
            if obj:
                pass
            else:
                return code

    form = SI_forms.UploadmaterialForm(request.POST)
    code = give_number()
    form.initial = {
        "자재코드": code,
    }

    search = request.GET.get("search")
    if search is None:
        customer = SI_models.SupplyPartner.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.SupplyPartner.objects.filter(
            Q(공급처작성자__first_name=search)
            | Q(거래처구분=search)
            | Q(거래처코드=search)
            | Q(거래처명__contains=search)
            | Q(공급처담당자__first_name=search)
            | Q(사업장주소__contains=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        material = form.save()
        material.자재공급업체 = form.cleaned_data.get("자재공급업체")
        material.작성자 = request.user
        material.save()
        form.save_m2m()

        messages.success(request, "자재 기준정보가 등록되었습니다.")
        return redirect(reverse("stockmanages:materialStandarInformation"))
    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = ["단위", "품목"]
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"

    return render(
        request,
        "stockmanages/materialregister.html",
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


class MaterialDetialView(user_mixins.LoggedInOnlyView, DetailView):
    model = SI_models.Material

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        material = SI_models.Material.objects.get_or_none(pk=pk)
        user = request.user
        return render(
            request,
            "stockmanages/materialdetail.html",
            {"material": material, "user": user,},
        )


class materialedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = SI_models.Material
    fields = (
        "품목",
        "자재품명",
        "규격",
        "단위",
        "단가",
        "특이사항",
    )
    template_name = "stockmanages/materialedit.html"

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse("stockmanages:materialdetail", kwargs={"pk": pk})


def materialdeleteensure(request, pk):

    material = SI_models.Material.objects.get_or_none(pk=pk)
    return render(
        request, "stockmanages/materialdeleteensure.html", {"material": material},
    )


def materialdelete(request, pk):
    material = SI_models.Material.objects.get_or_none(pk=pk)
    material.delete()

    messages.success(request, "해당 자재가 삭제되었습니다.")

    return redirect(reverse("stockmanages:materialStandarInformation"))
