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
from stocksingle import models as SS_models
from stockrack import models as SM_models
from orders import models as OR_models
from django.utils import timezone
from qualitycontrols import models as QC_models
from afterservices import models as AS_models


class qualitycontrolshome(View):
    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = OR_models.OrderRegister.objects.filter(제품구분="단품").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                    try:
                        s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록
                    except:
                        queryset.append(s)
                except:
                    pass
            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                OR_models.OrderRegister.objects.filter(제품구분="단품")
                .filter(
                    Q(수주코드__contains=self.search)
                    | Q(영업구분=self.search)
                    | Q(제품구분=self.search)
                    | Q(사업장구분=self.search)
                    | Q(고객사명__거래처명__contains=self.search)
                    | Q(단품모델__모델명__contains=self.search)
                    | Q(단품모델__모델코드__contains=self.search)
                    | Q(랙모델__랙모델명__contains=self.search)
                    | Q(랙모델__랙시리얼코드__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                    try:
                        s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록
                    except:
                        queryset.append(s)
                except:
                    pass
        return queryset

    def get_second_queryset(self, request):
        self.search2 = request.GET.get("search2")
        if self.search2 is None:
            order = QC_models.RepairRegister.objects.filter(수리최종="최종검사결과").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                    except:
                        queryset.append(s)
                except:
                    pass
            self.s_bool2 = False
        else:
            self.s_bool2 = True
            order = (
                QC_models.RepairRegister.objects.filter(수리최종="최종검사결과")
                .filter(
                    Q(최종검사결과__최종검사코드__contains=self.search2)
                    | Q(최종검사결과__제품__모델명__contains=self.search2)
                    | Q(최종검사결과__제품__모델코드__contains=self.search2)
                    | Q(작성자__first_name__contains=self.search2)
                    | Q(불량위치및자재__contains=self.search2)
                    | Q(수리내용__contains=self.search2)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                    except:
                        queryset.append(s)
                except:
                    pass
        return queryset

    def get_third_queryset(self, request):
        self.search3 = request.GET.get("search3")
        if self.search3 is None:
            order = QC_models.RepairRegister.objects.filter(수리최종="AS").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                    except:
                        queryset.append(s)
                except:
                    pass
            self.s_bool3 = False
        else:
            self.s_bool3 = True
            order = (
                QC_models.RepairRegister.objects.filter(수리최종="AS")
                .filter(
                    Q(AS수리의뢰__수리요청코드__contains=self.search3)
                    | Q(AS수리의뢰__신청품목__모델명__contains=self.search3)
                    | Q(AS수리의뢰__신청품목__모델코드__contains=self.search3)
                    | Q(작성자__first_name__contains=self.search3)
                    | Q(불량위치및자재__contains=self.search3)
                    | Q(수리내용__contains=self.search3)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                    except:
                        queryset.append(s)
                except:
                    pass
        return queryset

    def get_page(self):
        self.queryset = self.get_first_queryset(self.request)
        self.pagediv = 7
        self.totalpage = int(math.ceil(len(self.queryset) / self.pagediv))
        self.paginator = Paginator(self.queryset, self.pagediv, orphans=3)
        self.page = self.request.GET.get("page", "1")
        self.queryset = self.paginator.get_page(self.page)
        self.nextpage = int(self.page) + 1
        self.previouspage = int(self.page) - 1
        self.notsamebool = True
        self.nonpage = False
        if self.totalpage == 0:
            self.nonpage = True
        if int(self.page) == self.totalpage:
            self.notsamebool = False
        if (self.search is None) or (self.search == ""):
            self.search = "search"

    def get_page2(self):
        self.queryset2 = self.get_second_queryset(self.request)
        self.pagediv2 = 7
        self.totalpage2 = int(math.ceil(len(self.queryset2) / self.pagediv2))
        self.paginator2 = Paginator(self.queryset2, self.pagediv2, orphans=3)
        self.page2 = self.request.GET.get("page2", "1")
        self.queryset2 = self.paginator2.get_page(self.page2)
        self.nextpage2 = int(self.page2) + 1
        self.previouspage2 = int(self.page2) - 1
        self.notsamebool2 = True
        self.nonpage2 = False
        if self.totalpage2 == 0:
            self.nonpage2 = True
        if int(self.page2) == self.totalpage2:
            self.notsamebool2 = False
        if (self.search2 is None) or (self.search2 == ""):
            self.search2 = "search"

    def get_page3(self):
        self.queryset3 = self.get_third_queryset(self.request)
        self.pagediv3 = 7
        self.totalpage3 = int(math.ceil(len(self.queryset3) / self.pagediv3))
        self.paginator3 = Paginator(self.queryset3, self.pagediv3, orphans=3)
        self.page3 = self.request.GET.get("page3", "1")
        self.queryset3 = self.paginator3.get_page(self.page3)
        self.nextpage3 = int(self.page3) + 1
        self.previouspage3 = int(self.page3) - 1
        self.notsamebool3 = True
        self.nonpage3 = False
        if self.totalpage3 == 0:
            self.nonpage3 = True
        if int(self.page3) == self.totalpage3:
            self.notsamebool3 = False
        if (self.search3 is None) or (self.search3 == ""):
            self.search3 = "search"

    def get(self, request):
        self.get_page()
        self.get_page2()
        self.get_page3()
        return render(
            request,
            "qualitycontrols/qualitycontrolshome.html",
            {
                "queryset": self.queryset,
                "page": self.page,
                "totalpage": self.totalpage,
                "notsamebool": self.notsamebool,
                "nextpage": self.nextpage,
                "previouspage": self.previouspage,
                "nonpage": self.nonpage,
                "search": self.search,
                "s_bool": self.s_bool,
                "queryset2": self.queryset2,
                "page2": self.page2,
                "totalpage2": self.totalpage2,
                "notsamebool2": self.notsamebool2,
                "nextpage2": self.nextpage2,
                "previouspage2": self.previouspage2,
                "nonpage2": self.nonpage2,
                "search2": self.search2,
                "s_bool2": self.s_bool2,
                "queryset3": self.queryset3,
                "page3": self.page3,
                "totalpage3": self.totalpage3,
                "notsamebool3": self.notsamebool3,
                "nextpage3": self.nextpage3,
                "previouspage3": self.previouspage3,
                "nonpage3": self.nonpage3,
                "search3": self.search3,
                "s_bool3": self.s_bool3,
            },
        )


class OrderDetailForWork(user_mixins.LoggedInOnlyView, DetailView):
    model = OR_models.OrderRegister

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        order = OR_models.OrderRegister.objects.get(pk=pk)
        user = request.user
        final = False
        inproduce = False
        orderproduce = False
        st = order.process()
        obj_user = order.작성자

        if st == "생산의뢰완료":
            orderproduce = True
        elif "생산중" in st or "최종검사의뢰완료" in st:
            inproduce = True
            orderproduce = True
        elif st == "최종검사완료":
            final = True
            inproduce = True
            orderproduce = True
        else:
            pass

        ordersingle = order.단품출하요청.all()
        pklist = []
        for orderi in ordersingle:
            pklist.append(orderi.pk)
        ordersingle = []
        for pki in pklist:
            SS = SS_models.StockOfSingleProductOutRequest.objects.get_or_none(pk=pki)
            ordersingle.append(SS)

        orderrack = order.랙출하요청.all()
        rpk = []
        for orderr in orderrack:
            rpk.append(orderr.pk)
        orderrack = []
        for pki in rpk:
            SS = SM_models.StockOfRackProductOutRequest.objects.get_or_none(pk=pki)
            orderrack.append(SS)
        try:
            order.생산요청.생산계획.작업지시서
            workboolean = True
        except:
            workboolean = False
        try:
            order.생산요청.생산계획.작업지시서.작업지시서등록
            workdoneboolean = True
        except:
            workdoneboolean = False
        try:
            order.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
            orderfinalboolean = True
        except:
            orderfinalboolean = False
        try:
            order.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록.수리내역서
            repairboolean = True
        except:
            repairboolean = False

        return render(
            request,
            "producemanages/orderdetailforwork.html",
            {
                "order": order,
                "user": user,
                "final": final,
                "inproduce": inproduce,
                "orderproduce": orderproduce,
                "obj_user": obj_user,
                "출하완료": "출하완료",
                "ordersingle": ordersingle,
                "no": 0,
                "orderrack": orderrack,
                "workboolean": workboolean,
                "workdoneboolean": workdoneboolean,
                "orderfinalboolean": orderfinalboolean,
                "repairboolean": repairboolean,
            },
        )


class OrderDetail(user_mixins.LoggedInOnlyView, DetailView):
    model = OR_models.OrderRegister

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        order = OR_models.OrderRegister.objects.get(pk=pk)
        user = request.user
        final = False
        inproduce = False
        orderproduce = False
        st = order.process()
        obj_user = order.작성자

        if st == "생산의뢰완료":
            orderproduce = True
        elif "생산중" in st or "최종검사의뢰완료" in st:
            inproduce = True
            orderproduce = True
        elif st == "최종검사완료":
            final = True
            inproduce = True
            orderproduce = True
        else:
            pass

        ordersingle = order.단품출하요청.all()
        pklist = []
        for orderi in ordersingle:
            pklist.append(orderi.pk)
        ordersingle = []
        for pki in pklist:
            SS = SS_models.StockOfSingleProductOutRequest.objects.get_or_none(pk=pki)
            ordersingle.append(SS)

        orderrack = order.랙출하요청.all()
        rpk = []
        for orderr in orderrack:
            rpk.append(orderr.pk)
        orderrack = []
        for pki in rpk:
            SS = SM_models.StockOfRackProductOutRequest.objects.get_or_none(pk=pki)
            orderrack.append(SS)
        try:
            order.생산요청.생산계획.작업지시서
            workboolean = True
        except:
            workboolean = False
        try:
            order.생산요청.생산계획.작업지시서.작업지시서등록
            workdoneboolean = True
        except:
            workdoneboolean = False
        try:
            order.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
            orderfinalboolean = True
        except:
            orderfinalboolean = False
        try:
            order.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록.수리내역서
            repairboolean = True
        except:
            repairboolean = False

        return render(
            request,
            "qualitycontrols/orderdetail.html",
            {
                "order": order,
                "user": user,
                "final": final,
                "inproduce": inproduce,
                "orderproduce": orderproduce,
                "obj_user": obj_user,
                "출하완료": "출하완료",
                "ordersingle": ordersingle,
                "no": 0,
                "orderrack": orderrack,
                "workboolean": workboolean,
                "workdoneboolean": workdoneboolean,
                "orderfinalboolean": orderfinalboolean,
                "repairboolean": repairboolean,
            },
        )


def finalcheckdetail(request, pk):
    finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    user = request.user
    try:
        finalcheck.수리내역서
        repairbool = True
    except:
        repairbool = False

    return render(
        request,
        "qualitycontrols/finalcheckdetail.html",
        {"finalcheck": finalcheck, "user": user, "repairbool": repairbool},
    )


def repairdetail(request, pk):
    user = request.user
    repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
    try:
        repair.최종검사
        finalcheckboolean = False
    except:
        finalcheckboolean = True
    return render(
        request,
        "qualitycontrols/repairdetail.html",
        {"repair": repair, "finalcheckboolean": finalcheckboolean, "user": user,},
    )


class finalchecklist(qualitycontrolshome):
    def get(self, request):
        self.get_page()
        self.get_page2()
        self.get_page3()
        return render(
            request,
            "qualitycontrols/finalchecklist.html",
            {
                "queryset": self.queryset,
                "page": self.page,
                "totalpage": self.totalpage,
                "notsamebool": self.notsamebool,
                "nextpage": self.nextpage,
                "previouspage": self.previouspage,
                "nonpage": self.nonpage,
                "search": self.search,
                "s_bool": self.s_bool,
                "queryset2": self.queryset2,
                "page2": self.page2,
                "totalpage2": self.totalpage2,
                "notsamebool2": self.notsamebool2,
                "nextpage2": self.nextpage2,
                "previouspage2": self.previouspage2,
                "nonpage2": self.nonpage2,
                "search2": self.search2,
                "s_bool2": self.s_bool2,
                "queryset3": self.queryset3,
                "page3": self.page3,
                "totalpage3": self.totalpage3,
                "notsamebool3": self.notsamebool3,
                "nextpage3": self.nextpage3,
                "previouspage3": self.previouspage3,
                "nonpage3": self.nonpage3,
                "search3": self.search3,
                "s_bool3": self.s_bool3,
            },
        )


def finalcheckregister(request, pk):

    user = request.user
    finalcheck = QC_models.FinalCheck.objects.get_or_none(pk=pk)

    form = forms.FinalCheckRegisterForm(request.POST)

    if form.is_valid():
        최종검사코드 = form.cleaned_data.get("최종검사코드")
        검시일 = form.cleaned_data.get("검시일")
        CR = form.cleaned_data.get("CR")
        MA = form.cleaned_data.get("MA")
        MI = form.cleaned_data.get("MI")
        검사수준 = form.cleaned_data.get("검사수준")
        Sample방식 = form.cleaned_data.get("Sample방식")
        결점수 = form.cleaned_data.get("결점수")
        전원전압 = form.cleaned_data.get("전원전압")
        POWERTRANS = form.cleaned_data.get("POWERTRANS")
        FUSE_전_ULUSA = form.cleaned_data.get("FUSE_전_ULUSA")
        LABEL_인쇄물 = form.cleaned_data.get("LABEL_인쇄물")
        기타출하위치 = form.cleaned_data.get("기타출하위치")
        내용물 = form.cleaned_data.get("내용물")
        포장검사 = form.cleaned_data.get("포장검사")
        동작검사 = form.cleaned_data.get("동작검사")
        내부검사 = form.cleaned_data.get("내부검사")
        외관검사 = form.cleaned_data.get("외관검사")
        내압검사 = form.cleaned_data.get("내압검사")
        내용물확인 = form.cleaned_data.get("내용물확인")
        가_감전압 = form.cleaned_data.get("가_감전압")
        HI_POT_내부검사 = form.cleaned_data.get("HI_POT_내부검사")
        REMARK = form.cleaned_data.get("REMARK")
        부적합수량 = form.cleaned_data.get("부적합수량")
        적합수량 = form.cleaned_data.get("적합수량")

        SM = models.FinalCheckRegister.objects.create(
            최종검사의뢰=finalcheck,
            검시자=user,
            제품=finalcheck.제품,
            최종검사코드=최종검사코드,
            검시일=검시일,
            CR=CR,
            MA=MA,
            MI=MI,
            검사수준=검사수준,
            Sample방식=Sample방식,
            결점수=결점수,
            전원전압=전원전압,
            POWERTRANS=POWERTRANS,
            FUSE_전_ULUSA=FUSE_전_ULUSA,
            LABEL_인쇄물=LABEL_인쇄물,
            기타출하위치=기타출하위치,
            내용물=내용물,
            포장검사=포장검사,
            동작검사=동작검사,
            내부검사=내부검사,
            외관검사=외관검사,
            내압검사=내압검사,
            내용물확인=내용물확인,
            가_감전압=가_감전압,
            HI_POT_내부검사=HI_POT_내부검사,
            REMARK=REMARK,
            부적합수량=부적합수량,
            적합수량=적합수량,
        )

        messages.success(request, "최종검사 등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:finalchecklist"))
    return render(
        request,
        "qualitycontrols/finalcheckregister.html",
        {"form": form, "finalcheck": finalcheck,},
    )


class finalcheckdonelist(qualitycontrolshome):
    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = OR_models.OrderRegister.objects.filter(제품구분="단품").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                    try:
                        s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록
                        queryset.append(s)
                    except:
                        pass
                except:
                    pass
            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                OR_models.OrderRegister.objects.filter(제품구분="단품")
                .filter(
                    Q(수주코드__contains=self.search)
                    | Q(영업구분=self.search)
                    | Q(제품구분=self.search)
                    | Q(사업장구분=self.search)
                    | Q(고객사명__거래처명__contains=self.search)
                    | Q(단품모델__모델명__contains=self.search)
                    | Q(단품모델__모델코드__contains=self.search)
                    | Q(랙모델__랙모델명__contains=self.search)
                    | Q(랙모델__랙시리얼코드__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                    try:
                        s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록
                        queryset.append(s)
                    except:
                        pass
                except:
                    pass
        return queryset

    def get_second_queryset(self, request):
        self.search2 = request.GET.get("search2")
        if self.search2 is None:
            order = QC_models.RepairRegister.objects.filter(수리최종="최종검사결과").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                        queryset.append(s)
                    except:
                        pass
                except:
                    pass
            self.s_bool2 = False
        else:
            self.s_bool2 = True
            order = (
                QC_models.RepairRegister.objects.filter(수리최종="최종검사결과")
                .filter(
                    Q(최종검사결과__최종검사코드__contains=self.search2)
                    | Q(최종검사결과__제품__모델명__contains=self.search2)
                    | Q(최종검사결과__제품__모델코드__contains=self.search2)
                    | Q(작성자__first_name__contains=self.search2)
                    | Q(불량위치및자재__contains=self.search2)
                    | Q(수리내용__contains=self.search2)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                        queryset.append(s)
                    except:
                        pass
                except:
                    pass
        return queryset

    def get_third_queryset(self, request):
        self.search3 = request.GET.get("search3")
        if self.search3 is None:
            order = QC_models.RepairRegister.objects.filter(수리최종="AS").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                        queryset.append(s)
                    except:
                        pass
                except:
                    pass
            self.s_bool3 = False
        else:
            self.s_bool3 = True
            order = (
                QC_models.RepairRegister.objects.filter(수리최종="AS")
                .filter(
                    Q(AS수리의뢰__수리요청코드__contains=self.search3)
                    | Q(AS수리의뢰__신청품목__모델명__contains=self.search3)
                    | Q(AS수리의뢰__신청품목__모델코드__contains=self.search3)
                    | Q(작성자__first_name__contains=self.search3)
                    | Q(불량위치및자재__contains=self.search3)
                    | Q(수리내용__contains=self.search3)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.최종검사
                    try:
                        s.최종검사.최종검사등록
                        queryset.append(s)
                    except:
                        pass
                except:
                    pass
        return queryset

    def get(self, request):
        self.get_page()
        self.get_page2()
        self.get_page3()
        return render(
            request,
            "qualitycontrols/finalcheckdonelist.html",
            {
                "queryset": self.queryset,
                "page": self.page,
                "totalpage": self.totalpage,
                "notsamebool": self.notsamebool,
                "nextpage": self.nextpage,
                "previouspage": self.previouspage,
                "nonpage": self.nonpage,
                "search": self.search,
                "s_bool": self.s_bool,
                "queryset2": self.queryset2,
                "page2": self.page2,
                "totalpage2": self.totalpage2,
                "notsamebool2": self.notsamebool2,
                "nextpage2": self.nextpage2,
                "previouspage2": self.previouspage2,
                "nonpage2": self.nonpage2,
                "search2": self.search2,
                "s_bool2": self.s_bool2,
                "queryset3": self.queryset3,
                "page3": self.page3,
                "totalpage3": self.totalpage3,
                "notsamebool3": self.notsamebool3,
                "nextpage3": self.nextpage3,
                "previouspage3": self.previouspage3,
                "nonpage3": self.nonpage3,
                "search3": self.search3,
                "s_bool3": self.s_bool3,
            },
        )


class finalcheckedit(UpdateView):
    model = QC_models.FinalCheckRegister
    template_name = "qualitycontrols/finalcheckedit.html"
    form_class = forms.FinalCheckEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
        context["finalcheck"] = finalcheck
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
        pk = finalcheck.pk
        return reverse("qualitycontrols:finalcheckdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        최종검사코드 = form.cleaned_data.get("최종검사코드")
        검시일 = form.cleaned_data.get("검시일")
        CR = form.cleaned_data.get("CR")
        MA = form.cleaned_data.get("MA")
        MI = form.cleaned_data.get("MI")
        검사수준 = form.cleaned_data.get("검사수준")
        Sample방식 = form.cleaned_data.get("Sample방식")
        결점수 = form.cleaned_data.get("결점수")
        전원전압 = form.cleaned_data.get("전원전압")
        POWERTRANS = form.cleaned_data.get("POWERTRANS")
        FUSE_전_ULUSA = form.cleaned_data.get("FUSE_전_ULUSA")
        LABEL_인쇄물 = form.cleaned_data.get("LABEL_인쇄물")
        기타출하위치 = form.cleaned_data.get("기타출하위치")
        내용물 = form.cleaned_data.get("내용물")
        포장검사 = form.cleaned_data.get("포장검사")
        동작검사 = form.cleaned_data.get("동작검사")
        내부검사 = form.cleaned_data.get("내부검사")
        외관검사 = form.cleaned_data.get("외관검사")
        내압검사 = form.cleaned_data.get("내압검사")
        내용물확인 = form.cleaned_data.get("내용물확인")
        가_감전압 = form.cleaned_data.get("가_감전압")
        HI_POT_내부검사 = form.cleaned_data.get("HI_POT_내부검사")
        REMARK = form.cleaned_data.get("REMARK")
        부적합수량 = form.cleaned_data.get("부적합수량")
        적합수량 = form.cleaned_data.get("적합수량")
        pk = self.kwargs.get("pk")
        finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
        finalcheck.최종검사코드 = 최종검사코드
        finalcheck.검시일 = 검시일
        finalcheck.CR = CR
        finalcheck.MA = MA
        finalcheck.MI = MI
        finalcheck.검사수준 = 검사수준
        finalcheck.Sample방식 = Sample방식
        finalcheck.결점수 = 결점수
        finalcheck.전원전압 = 전원전압
        finalcheck.POWERTRANS = POWERTRANS
        finalcheck.FUSE_전_ULUSA = FUSE_전_ULUSA
        finalcheck.LABEL_인쇄물 = LABEL_인쇄물
        finalcheck.기타출하위치 = 기타출하위치
        finalcheck.내용물 = 내용물
        finalcheck.포장검사 = 포장검사
        finalcheck.동작검사 = 동작검사
        finalcheck.내부검사 = 내부검사
        finalcheck.외관검사 = 외관검사
        finalcheck.내압검사 = 내압검사
        finalcheck.내용물확인 = 내용물확인
        finalcheck.가_감전압 = 가_감전압
        finalcheck.HI_POT_내부검사 = HI_POT_내부검사
        finalcheck.REMARK = REMARK
        finalcheck.부적합수량 = 부적합수량
        finalcheck.적합수량 = 적합수량

        finalcheck.save()
        messages.success(self.request, "최종검사 수정이 완료되었습니다.")

        return super().form_valid(form)


def finalcheckdeleteensure(request, pk):
    finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    return render(
        request,
        "qualitycontrols/finalcheckdeleteensure.html",
        {"finalcheck": finalcheck},
    )


def finalcheckdelete(request, pk):
    finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    finalcheck.delete()
    messages.success(request, "최종검사 삭제가 완료되었습니다.")
    return redirect(reverse("qualitycontrols:qualitycontrolshome"))

