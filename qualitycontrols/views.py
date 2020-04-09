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
from stockrack import models as SR_models
from stockmanages import models as SM_models
from orders import models as OR_models
from django.utils import timezone
from qualitycontrols import models as QC_models
from afterservices import models as AS_models
from core import views as core_views
from measures import models as MS_models
from random import randint
from specials import models as S_models


class qualitycontrolshome(core_views.threelist):
    pass


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
            SS = SR_models.StockOfRackProductOutRequest.objects.get_or_none(pk=pki)
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


class finalchecklist(core_views.threelist):
    templatename = "qualitycontrols/finalchecklist.html"


def finalcheckregister(request, pk):

    user = request.user
    finalcheck = QC_models.FinalCheck.objects.get_or_none(pk=pk)
    selectlist = [
        "포장검사",
        "동작검사",
        "내부검사",
        "외관검사",
        "내용물확인",
        "전원전압",
        "POWERTRANS",
        "FUSE_전_ULUSA",
        "LABEL_인쇄물",
        "내용물",
        "내압검사_DC",
        "내압검사_AC",
    ]

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "FC" + num
            obj = models.FinalCheckRegister.objects.get_or_none(최종검사코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.FinalCheckRegisterForm(request.POST or None)
    code = give_number()
    form.initial = {
        "치명적불량": 0,
        "중불량": 0.4,
        "경불량": 4.5,
        "샘플링방식": "랜덤샘플링방식",
        "검사수준": "보통검사",
        "최종검사코드": code,
        "내압검사_DC": "NO",
        "내압검사_AC": "OK",
    }

    if form.is_valid():
        최종검사코드 = form.cleaned_data.get("최종검사코드")
        검시일 = form.cleaned_data.get("검시일")
        치명적불량 = form.cleaned_data.get("치명적불량")
        중불량 = form.cleaned_data.get("중불량")
        경불량 = form.cleaned_data.get("경불량")
        검사수준 = form.cleaned_data.get("검사수준")
        샘플링방식 = form.cleaned_data.get("샘플링방식")
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
        내압검사_DC = form.cleaned_data.get("내압검사_DC")
        내압검사_AC = form.cleaned_data.get("내압검사_AC")
        내용물확인 = form.cleaned_data.get("내용물확인")
        가_감전압 = form.cleaned_data.get("가_감전압")
        HI_POT_내부검사 = form.cleaned_data.get("HI_POT_내부검사")
        특이사항 = form.cleaned_data.get("특이사항")
        부적합수량 = form.cleaned_data.get("부적합수량")
        적합수량 = form.cleaned_data.get("적합수량")
        if 검시일 is None:
            검시일 = timezone.now().date()

        SM = models.FinalCheckRegister.objects.create(
            최종검사의뢰=finalcheck,
            검시자=user,
            제품=finalcheck.제품,
            최종검사코드=최종검사코드,
            검시일=검시일,
            치명적불량=치명적불량,
            중불량=중불량,
            경불량=경불량,
            검사수준=검사수준,
            샘플링방식=샘플링방식,
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
            내압검사_DC=내압검사_DC,
            내압검사_AC=내압검사_AC,
            내용물확인=내용물확인,
            가_감전압=가_감전압,
            HI_POT_내부검사=HI_POT_내부검사,
            특이사항=특이사항,
            부적합수량=부적합수량,
            적합수량=적합수량,
        )
        SS_models.StockOfSingleProductInRequest.objects.create(
            단품=finalcheck.제품, 입고요청수량=적합수량, 입고요청자=user, 입고요청일=timezone.now().date(),
        )

        messages.success(request, "최종검사 등록이 완료되었습니다.(단품입고요청 자동완료)")

        return redirect(reverse("qualitycontrols:finalchecklist"))
    return render(
        request,
        "qualitycontrols/finalcheckregister.html",
        {"form": form, "finalcheck": finalcheck, "selectlist": selectlist},
    )


def finalcheckregisternotin(request, pk):

    user = request.user
    finalcheck = QC_models.FinalCheck.objects.get_or_none(pk=pk)
    selectlist = [
        "포장검사",
        "동작검사",
        "내부검사",
        "외관검사",
        "내용물확인",
        "전원전압",
        "POWERTRANS",
        "FUSE_전_ULUSA",
        "LABEL_인쇄물",
        "내용물",
        "내압검사_DC",
        "내압검사_AC",
    ]

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "FC" + num
            obj = models.FinalCheckRegister.objects.get_or_none(최종검사코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.FinalCheckRegisterForm(request.POST or None)
    code = give_number()
    form.initial = {
        "치명적불량": 0,
        "중불량": 0.4,
        "경불량": 4.5,
        "샘플링방식": "랜덤샘플링방식",
        "검사수준": "보통검사",
        "최종검사코드": code,
        "내압검사_DC": "NO",
        "내압검사_AC": "OK",
    }

    if form.is_valid():
        최종검사코드 = form.cleaned_data.get("최종검사코드")
        검시일 = form.cleaned_data.get("검시일")
        치명적불량 = form.cleaned_data.get("치명적불량")
        중불량 = form.cleaned_data.get("중불량")
        경불량 = form.cleaned_data.get("경불량")
        검사수준 = form.cleaned_data.get("검사수준")
        샘플링방식 = form.cleaned_data.get("샘플링방식")
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
        내압검사_DC = form.cleaned_data.get("내압검사_DC")
        내압검사_AC = form.cleaned_data.get("내압검사_AC")
        내용물확인 = form.cleaned_data.get("내용물확인")
        가_감전압 = form.cleaned_data.get("가_감전압")
        HI_POT_내부검사 = form.cleaned_data.get("HI_POT_내부검사")
        특이사항 = form.cleaned_data.get("특이사항")
        부적합수량 = form.cleaned_data.get("부적합수량")
        적합수량 = form.cleaned_data.get("적합수량")
        if 검시일 is None:
            검시일 = timezone.now().date()

        SM = models.FinalCheckRegister.objects.create(
            최종검사의뢰=finalcheck,
            검시자=user,
            제품=finalcheck.제품,
            최종검사코드=최종검사코드,
            검시일=검시일,
            치명적불량=치명적불량,
            중불량=중불량,
            경불량=경불량,
            검사수준=검사수준,
            샘플링방식=샘플링방식,
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
            내압검사_DC=내압검사_DC,
            내압검사_AC=내압검사_AC,
            내용물확인=내용물확인,
            가_감전압=가_감전압,
            HI_POT_내부검사=HI_POT_내부검사,
            특이사항=특이사항,
            부적합수량=부적합수량,
            적합수량=적합수량,
        )
        SS_models.StockOfSingleProductInRequest.objects.create(
            단품=finalcheck.제품, 입고요청수량=적합수량, 입고요청자=user, 입고요청일=timezone.now().date(),
        )

        messages.success(request, "최종검사 등록이 완료되었습니다.(단품입고요청 자동완료)")

        return redirect(reverse("qualitycontrols:finalchecklist"))

    return render(
        request,
        "qualitycontrols/finalcheckregister.html",
        {"form": form, "finalcheck": finalcheck, "selectlist": selectlist,},
    )


class finalcheckdonelist(core_views.threelist):
    templatename = "qualitycontrols/finalcheckdonelist.html"

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


class finalcheckedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = QC_models.FinalCheckRegister
    template_name = "qualitycontrols/finalcheckedit.html"
    form_class = forms.FinalCheckEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
        context["finalcheck"] = finalcheck
        context["selectlist"] = [
            "포장검사",
            "동작검사",
            "내부검사",
            "외관검사",
            "내용물확인",
            "전원전압",
            "POWERTRANS",
            "FUSE_전_ULUSA",
            "LABEL_인쇄물",
            "내용물",
            "내압검사_DC",
            "내압검사_AC",
        ]
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
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
        치명적불량 = form.cleaned_data.get("치명적불량")
        중불량 = form.cleaned_data.get("중불량")
        경불량 = form.cleaned_data.get("경불량")
        검사수준 = form.cleaned_data.get("검사수준")
        샘플링방식 = form.cleaned_data.get("샘플링방식")
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
        내압검사_AC = form.cleaned_data.get("내압검사_AC")
        내압검사_DC = form.cleaned_data.get("내압검사_DC")
        내용물확인 = form.cleaned_data.get("내용물확인")
        가_감전압 = form.cleaned_data.get("가_감전압")
        HI_POT_내부검사 = form.cleaned_data.get("HI_POT_내부검사")
        특이사항 = form.cleaned_data.get("특이사항")
        부적합수량 = form.cleaned_data.get("부적합수량")
        적합수량 = form.cleaned_data.get("적합수량")
        pk = self.kwargs.get("pk")
        finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
        finalcheck.최종검사코드 = 최종검사코드
        finalcheck.검시일 = 검시일
        finalcheck.치명적불량 = 치명적불량
        finalcheck.중불량 = 중불량
        finalcheck.경불량 = 경불량
        finalcheck.검사수준 = 검사수준
        finalcheck.샘플링방식 = 샘플링방식
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
        finalcheck.내압검사_AC = 내압검사_AC
        finalcheck.내압검사_C = 내압검사_C
        finalcheck.내용물확인 = 내용물확인
        finalcheck.가_감전압 = 가_감전압
        finalcheck.HI_POT_내부검사 = HI_POT_내부검사
        finalcheck.특이사항 = 특이사항
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


class materialchecklist(core_views.onelist):
    pass


def materialcheckregister(request, pk):
    user = request.user
    materialcheck = QC_models.MaterialCheckRegister.objects.get_or_none(pk=pk)

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "MR" + num
            obj = models.MaterialCheck.objects.get_or_none(수입검사코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.MaterialCheckRegisterForm(request.POST or None)
    code = give_number()
    form.initial = {
        "수입검사코드": code,
    }

    if form.is_valid():
        수입검사코드 = form.cleaned_data.get("수입검사코드")
        검사지침서번호 = form.cleaned_data.get("검사지침서번호")
        검사일자 = form.cleaned_data.get("검사일자")
        검사항목 = form.cleaned_data.get("검사항목")
        판정기준 = form.cleaned_data.get("판정기준")
        시료크기 = form.cleaned_data.get("시료크기")
        합격수량 = form.cleaned_data.get("합격수량")
        불합격수량 = form.cleaned_data.get("불합격수량")
        불합격내용 = form.cleaned_data.get("불합격내용")
        if 검사일자 is None:
            검사일자 = timezone.now().date()

        SM = models.MaterialCheck.objects.create(
            자재=materialcheck.자재,
            수입검사의뢰=materialcheck,
            검사자=user,
            수입검사코드=수입검사코드,
            검사지침서번호=검사지침서번호,
            검사일자=검사일자,
            검사항목=검사항목,
            판정기준=판정기준,
            시료크기=시료크기,
            합격수량=합격수량,
            불합격수량=불합격수량,
            불합격내용=불합격내용,
        )

        SM_models.StockOfMaterialInRequest.objects.create(
            자재=materialcheck.자재,
            입고요청수량=합격수량,
            입고요청자=user,
            입고요청일=timezone.now().date(),
            입고유형="일반",
        )

        messages.success(request, "수입검사 등록이 완료되었습니다.(자재입고요청 완료)")

        return redirect(reverse("qualitycontrols:materialchecklist"))
    return render(
        request,
        "qualitycontrols/materialcheckregister.html",
        {"form": form, "materialcheck": materialcheck,},
    )


class lowmateriallist(core_views.onelist):
    templatename = "qualitycontrols/materialcheckdonelist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            materialchecklist = QC_models.MaterialCheck.objects.exclude(
                불합격수량=0
            ).order_by("-created")
            queryset = []
            for s in materialchecklist:
                try:
                    s.자재부적합보고서
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            materialchecklist = (
                QC_models.MaterialCheck.objects.exclude(불합격수량=0)
                .filter(
                    Q(수입검사코드__contains=self.search)
                    | Q(검사지침서번호__contains=self.search)
                    | Q(판정기준__contains=self.search)
                    | Q(검사항목__contains=self.search)
                    | Q(검사자__first_name__contains=self.search)
                    | Q(자재__자재코드__contains=self.search)
                    | Q(자재__자재품명__contains=self.search)
                    | Q(불합격내용__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in materialchecklist:
                try:
                    s.자재부적합보고서
                except:
                    queryset.append(s)
        return queryset


def lowmaterialregister(request, pk):
    user = request.user
    materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "LR" + num
            obj = models.LowMetarial.objects.get_or_none(자재부적합코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.LowMetarialRegisterForm(request.POST or None)
    code = give_number()
    form.initial = {
        "자재부적합코드": code,
    }

    if form.is_valid():
        자재부적합코드 = form.cleaned_data.get("자재부적합코드")
        검토일 = form.cleaned_data.get("검토일")
        부적합자재의내용과검토방안 = form.cleaned_data.get("부적합자재의내용과검토방안")
        처리방안 = form.cleaned_data.get("처리방안")
        if 검토일 is None:
            검토일 = timezone.now().date()

        SM = models.LowMetarial.objects.create(
            자재부적합코드=자재부적합코드,
            수입검사=materialcheck,
            검토자=user,
            검토일=검토일,
            부적합자재의내용과검토방안=부적합자재의내용과검토방안,
            처리방안=처리방안,
            자재=materialcheck.자재,
        )

        messages.success(request, "자재부적합 보고서 등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:lowmateriallist"))
    return render(
        request,
        "qualitycontrols/lowmaterialregister.html",
        {"form": form, "materialcheck": materialcheck,},
    )


class materialcheckalllist(core_views.onelist):
    templatename = "qualitycontrols/materialcheckalllist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = QC_models.MaterialCheck.objects.all().order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = QC_models.MaterialCheck.objects.filter(
                Q(수입검사코드__contains=self.search)
                | Q(검사지침서번호__contains=self.search)
                | Q(판정기준__contains=self.search)
                | Q(검사항목__contains=self.search)
                | Q(검사자__first_name__contains=self.search)
                | Q(자재__자재코드__contains=self.search)
                | Q(자재__자재품명__contains=self.search)
                | Q(불합격내용__contains=self.search)
            ).order_by("-created")
        return queryset


def materialcheckdetail(request, pk):
    materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)
    user = request.user

    return render(
        request,
        "qualitycontrols/materialcheckdetail.html",
        {"materialcheck": materialcheck, "user": user},
    )


class lowmetarialedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = QC_models.LowMetarial
    template_name = "qualitycontrols/lowmaterialedit.html"
    form_class = forms.LowMetarialEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        lowmetarial = QC_models.LowMetarial.objects.get_or_none(pk=pk)
        context["lowmetarial"] = lowmetarial
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        lowmetarial = QC_models.LowMetarial.objects.get_or_none(pk=pk)
        matrialcheck = lowmetarial.수입검사
        pk = matrialcheck.pk
        return reverse("qualitycontrols:materialcheckdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        자재부적합코드 = form.cleaned_data.get("자재부적합코드")
        검토일 = form.cleaned_data.get("검토일")
        부적합자재의내용과검토방안 = form.cleaned_data.get("부적합자재의내용과검토방안")
        처리방안 = form.cleaned_data.get("처리방안")
        if 검토일 is None:
            검토일 = timezone.now().date()

        pk = self.kwargs.get("pk")
        lowmetarial = QC_models.LowMetarial.objects.get_or_none(pk=pk)
        lowmetarial.자재부적합코드 = 자재부적합코드
        lowmetarial.검토일 = 검토일
        lowmetarial.부적합자재의내용과검토방안 = 부적합자재의내용과검토방안
        lowmetarial.처리방안 = 처리방안

        lowmetarial.save()
        messages.success(self.request, "자재부적합보고서 수정이 완료되었습니다.")

        return super().form_valid(form)


def lowmetarialdeleteensure(request, pk):
    lowmetarial = QC_models.LowMetarial.objects.get_or_none(pk=pk)
    return render(
        request,
        "qualitycontrols/lowmetarialdeleteensure.html",
        {"lowmetarial": lowmetarial},
    )


def lowmetarialdelete(request, pk):
    lowmetarial = QC_models.LowMetarial.objects.get_or_none(pk=pk)
    materialcheck = lowmetarial.수입검사
    pk = materialcheck.pk
    lowmetarial.delete()
    messages.success(request, "자재부적합보고서 삭제가 완료되었습니다.")
    return redirect(reverse("qualitycontrols:materialcheckdetail", kwargs={"pk": pk}))


class materialcheckedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = QC_models.MaterialCheck
    template_name = "qualitycontrols/materialcheckedit.html"
    form_class = forms.MaterialCheckEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)
        context["materialcheck"] = materialcheck
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)
        pk = materialcheck.pk
        return reverse("qualitycontrols:materialcheckdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        수입검사코드 = form.cleaned_data.get("수입검사코드")
        검사지침서번호 = form.cleaned_data.get("검사지침서번호")
        검사일자 = form.cleaned_data.get("검사일자")
        검사항목 = form.cleaned_data.get("검사항목")
        판정기준 = form.cleaned_data.get("판정기준")
        시료크기 = form.cleaned_data.get("시료크기")
        합격수량 = form.cleaned_data.get("합격수량")
        불합격수량 = form.cleaned_data.get("불합격수량")
        불합격내용 = form.cleaned_data.get("불합격내용")
        if 검사일자 is None:
            검사일자 = timezone.now().date()
        pk = self.kwargs.get("pk")
        materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)
        materialcheck.수입검사코드 = form.cleaned_data.get("수입검사코드")
        materialcheck.검사지침서번호 = form.cleaned_data.get("검사지침서번호")
        materialcheck.검사일자 = form.cleaned_data.get("검사일자")
        materialcheck.검사항목 = form.cleaned_data.get("검사항목")
        materialcheck.판정기준 = form.cleaned_data.get("판정기준")
        materialcheck.시료크기 = form.cleaned_data.get("시료크기")
        materialcheck.합격수량 = form.cleaned_data.get("합격수량")
        materialcheck.불합격수량 = form.cleaned_data.get("불합격수량")
        materialcheck.불합격내용 = form.cleaned_data.get("불합격내용")
        materialcheck.save()
        messages.success(self.request, "수입검사결과 수정이 완료되었습니다.")
        return super().form_valid(form)


def materialcheckdeleteensure(request, pk):
    materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)
    return render(
        request,
        "qualitycontrols/materialcheckdeleteensure.html",
        {"materialcheck": materialcheck},
    )


def materialcheckdelete(request, pk):
    materialcheck = QC_models.MaterialCheck.objects.get_or_none(pk=pk)
    materialcheck.delete()
    messages.success(request, "수입검사결과 삭제가 완료되었습니다.")
    return redirect(reverse("qualitycontrols:qualitycontrolshome"))


class checkmeasurelist(core_views.onelist):
    templatename = "qualitycontrols/checkmeasurelist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = MS_models.MeasureCheckRegister.objects.all().order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = MS_models.MeasureCheckRegister.objects.filter(
                Q(계측기__계측기코드__contains=self.search)
                | Q(계측기__계측기명__contains=self.search)
                | Q(계측기__자산관리번호__contains=self.search)
                | Q(계측기__사용공정명__contains=self.search)
                | Q(계측기__설치장소__contains=self.search)
                | Q(점검내용__contains=self.search)
                | Q(점검자__first_name__contains=self.search)
            ).order_by("-created")
        return queryset


def measuredetail(request, pk):
    measure = SI_models.Measure.objects.get_or_none(pk=pk)
    user = request.user
    return render(
        request,
        "qualitycontrols/measuredetail.html",
        {"measure": measure, "user": user,},
    )


def file_download(request, pk):
    """파일 다운로드 유니코드화 패치"""
    measure = SI_models.Measure.objects.get_or_none(pk=pk)
    filepath = measure.file.path
    title = measure.file.__str__()
    title = urllib.parse.quote(title.encode("utf-8"))
    title = title.replace("images/", "")

    with open(filepath, "rb") as f:
        response = HttpResponse(f, content_type="application/force-download")
        titling = 'attachment; filename="{}"'.format(title)
        response["Content-Disposition"] = titling
        return response


class measureedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = SI_models.Measure
    template_name = "qualitycontrols/measureedit.html"
    form_class = forms.measureeditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        measure = SI_models.Measure.objects.get_or_none(pk=pk)
        context["measure"] = measure
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse("qualitycontrols:measuredetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        pk = self.kwargs.get("pk")
        measure = SI_models.Measure.objects.get_or_none(pk=pk)
        measure.계측기코드 = form.cleaned_data.get("계측기코드")
        measure.계측기명 = form.cleaned_data.get("계측기명")
        measure.자산관리번호 = form.cleaned_data.get("자산관리번호")
        measure.계측기규격 = form.cleaned_data.get("계측기규격")
        measure.설치년월일 = form.cleaned_data.get("설치년월일")
        measure.사용공정명 = form.cleaned_data.get("사용공정명")
        measure.설치장소 = form.cleaned_data.get("설치장소")
        measure.file = form.cleaned_data.get("file")
        measure.save()
        messages.success(self.request, "계측기 수정이 완료되었습니다.")
        return super().form_valid(form)


def measuredeleteensure(request, pk):
    measure = SI_models.Measure.objects.get_or_none(pk=pk)
    return render(
        request, "qualitycontrols/measuredeleteensure.html", {"measure": measure},
    )


def measuredelete(request, pk):
    measure = SI_models.Measure.objects.get_or_none(pk=pk)
    measure.delete()
    messages.success(request, "계측기 삭제가 완료되었습니다.")
    return redirect(reverse("qualitycontrols:qualitycontrolshome"))


def measurecheckdetail(request, pk):
    measurecheck = MS_models.MeasureCheckRegister.objects.get_or_none(pk=pk)
    user = request.user
    return render(
        request,
        "qualitycontrols/measurecheckdetail.html",
        {"measurecheck": measurecheck, "user": user,},
    )


class measurecheckedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = MS_models.MeasureCheckRegister
    template_name = "qualitycontrols/measurecheckedit.html"
    form_class = forms.measurecheckeditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        measurecheck = MS_models.MeasureCheckRegister.objects.get_or_none(pk=pk)
        context["measurecheck"] = measurecheck
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse("qualitycontrols:measurecheckdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()

        pk = self.kwargs.get("pk")
        measurecheck = MS_models.MeasureCheckRegister.objects.get_or_none(pk=pk)
        measurecheck.점검일 = form.cleaned_data.get("점검일")
        measurecheck.점검내용 = form.cleaned_data.get("점검내용")
        measurecheck.특이사항 = form.cleaned_data.get("특이사항")

        measurecheck.save()
        messages.success(self.request, "계측기점검 내용 수정이 완료되었습니다.")
        return super().form_valid(form)


def measurecheckdeleteensure(request, pk):
    measurecheck = MS_models.MeasureCheckRegister.objects.get_or_none(pk=pk)
    return render(
        request,
        "qualitycontrols/measurecheckdeleteensure.html",
        {"measurecheck": measurecheck},
    )


def measurecheckdelete(request, pk):
    measurecheck = MS_models.MeasureCheckRegister.objects.get_or_none(pk=pk)
    measurecheck.delete()
    messages.success(request, "계측기 삭제가 완료되었습니다.")
    return redirect(reverse("qualitycontrols:qualitycontrolshome"))


def measurecheckdetailregister(request):
    form = forms.measurecheckregisterForm(request.POST or None)
    search = request.GET.get("search")
    if search is None:
        customer = SI_models.Measure.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.Measure.objects.filter(
            Q(계측기코드__contains=search)
            | Q(계측기명__contains=search)
            | Q(자산관리번호__contains=search)
            | Q(계측기규격__contains=search)
            | Q(사용공정명__contains=search)
            | Q(설치장소__contains=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        계측기 = form.cleaned_data.get("계측기")
        점검일 = form.cleaned_data.get("점검일")
        점검내용 = form.cleaned_data.get("점검내용")
        특이사항 = form.cleaned_data.get("특이사항")

        SM = MS_models.MeasureCheckRegister.objects.create(
            점검자=request.user, 계측기=계측기, 점검일=점검일, 점검내용=점검내용, 특이사항=특이사항,
        )

        return redirect(reverse("qualitycontrols:checkmeasurelist"))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = [
        "제품구분",
    ]
    nonpage = False
    if totalpage == 0:
        nonpage = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "qualitycontrols/orderregister.html",
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
            "nonpage": nonpage,
        },
    )


class repairmeasurelist(core_views.onelist):
    templatename = "qualitycontrols/repairmeasurelist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = MS_models.MeasureRepairRegister.objects.all().order_by(
                "-created"
            )

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = MS_models.MeasureRepairRegister.objects.filter(
                Q(계측기__계측기코드__contains=self.search)
                | Q(계측기__계측기명__contains=self.search)
                | Q(계측기__자산관리번호__contains=self.search)
                | Q(계측기__사용공정명__contains=self.search)
                | Q(계측기__설치장소__contains=self.search)
                | Q(수리내용__contains=self.search)
                | Q(수리부문__contains=self.search)
                | Q(수리자__first_name__contains=self.search)
            ).order_by("-created")
        return queryset


def measurerepairdetail(request, pk):
    measurerepair = MS_models.MeasureRepairRegister.objects.get_or_none(pk=pk)
    user = request.user
    return render(
        request,
        "qualitycontrols/measurerepairdetail.html",
        {"measurerepair": measurerepair, "user": user,},
    )


class measurerepairedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = MS_models.MeasureRepairRegister
    template_name = "qualitycontrols/measurerepairedit.html"
    form_class = forms.measurerepaireditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        measurerepair = MS_models.MeasureRepairRegister.objects.get_or_none(pk=pk)
        context["measurerepair"] = measurerepair
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse("qualitycontrols:measurerepairdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()

        pk = self.kwargs.get("pk")
        measurerepair = MS_models.MeasureRepairRegister.objects.get_or_none(pk=pk)
        measurerepair.수리일 = form.cleaned_data.get("수리일")
        measurerepair.수리내용 = form.cleaned_data.get("수리내용")
        measurerepair.특이사항 = form.cleaned_data.get("특이사항")
        measurerepair.수리부문 = form.cleaned_data.get("수리부문")
        measurerepair.file = form.cleaned_data.get("file")

        measurerepair.save()
        messages.success(self.request, "계측기점검 내용 수정이 완료되었습니다.")
        return super().form_valid(form)


def measurerepairdeleteensure(request, pk):
    measurerepair = MS_models.MeasureRepairRegister.objects.get_or_none(pk=pk)
    return render(
        request,
        "qualitycontrols/measurerepairdeleteensure.html",
        {"measurerepair": measurerepair},
    )


def measurerepairdelete(request, pk):
    measurerepair = MS_models.MeasureRepairRegister.objects.get_or_none(pk=pk)
    measurerepair.delete()
    messages.success(request, "계측기 삭제가 완료되었습니다.")
    return redirect(reverse("qualitycontrols:qualitycontrolshome"))


def file_downloadforrepair(request, pk):
    """파일 다운로드 유니코드화 패치"""
    measure = MS_models.MeasureRepairRegister.objects.get_or_none(pk=pk)
    filepath = measure.file.path
    title = measure.file.__str__()
    title = urllib.parse.quote(title.encode("utf-8"))
    title = title.replace("images/", "")

    with open(filepath, "rb") as f:
        response = HttpResponse(f, content_type="application/force-download")
        titling = 'attachment; filename="{}"'.format(title)
        response["Content-Disposition"] = titling
        return response


def measurerepairdetailregister(request):
    form = forms.measurerepairregisterForm(request.POST or None)
    search = request.GET.get("search")
    if search is None:
        customer = SI_models.Measure.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.Measure.objects.filter(
            Q(계측기코드__contains=search)
            | Q(계측기명__contains=search)
            | Q(자산관리번호__contains=search)
            | Q(계측기규격__contains=search)
            | Q(사용공정명__contains=search)
            | Q(설치장소__contains=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        계측기 = form.cleaned_data.get("계측기")
        수리일 = form.cleaned_data.get("수리일")
        수리내용 = form.cleaned_data.get("수리내용")
        특이사항 = form.cleaned_data.get("특이사항")
        수리부문 = form.cleaned_data.get("수리부문")
        try:
            file = request.FILES["file"]

        except Exception:
            file = None

        SM = MS_models.MeasureRepairRegister.objects.create(
            계측기=계측기,
            수리자=request.user,
            수리일=수리일,
            수리부문=수리부문,
            수리내용=수리내용,
            file=file,
            특이사항=특이사항,
        )

        return redirect(reverse("qualitycontrols:repairmeasurelist"))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = [
        "제품구분",
    ]
    nonpage = False
    if totalpage == 0:
        nonpage = True
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "qualitycontrols/measurerepairdetailregister.html",
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
            "nonpage": nonpage,
        },
    )


class measurelist(core_views.onelist):
    templatename = "qualitycontrols/measurelist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SI_models.Measure.objects.all().order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = SI_models.Measure.objects.filter(
                Q(계측기코드__contains=self.search)
                | Q(계측기명__contains=self.search)
                | Q(자산관리번호__contains=self.search)
                | Q(사용공정명__contains=self.search)
                | Q(설치장소__contains=self.search)
                | Q(작성자__contains=self.search)
            ).order_by("-created")
        return queryset


def measuredetailregister(request):
    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "MS" + num
            obj = SI_models.Measure.objects.get_or_none(계측기코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.measureregisterForm(request.POST or None)
    code = give_number()
    form.initial = {
        "계측기코드": code,
    }

    if form.is_valid():
        계측기코드 = form.cleaned_data.get("계측기코드")
        계측기명 = form.cleaned_data.get("계측기명")
        자산관리번호 = form.cleaned_data.get("자산관리번호")
        계측기규격 = form.cleaned_data.get("계측기규격")
        설치년월일 = form.cleaned_data.get("설치년월일")
        사용공정명 = form.cleaned_data.get("사용공정명")
        설치장소 = form.cleaned_data.get("설치장소")
        try:
            file = request.FILES["file"]

        except Exception:
            file = None

        SM = SI_models.Measure.objects.create(
            계측기코드=계측기코드,
            계측기명=계측기명,
            자산관리번호=자산관리번호,
            계측기규격=계측기규격,
            설치년월일=설치년월일,
            사용공정명=사용공정명,
            설치장소=설치장소,
            file=file,
            작성자=request.user,
        )

        messages.success(request, "계측기 등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:measurelist"))
    return render(request, "qualitycontrols/measureregister.html", {"form": form,},)


class specialregisterlist(core_views.onelist):
    templatename = "qualitycontrols/specialregisterlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = S_models.SpecialRegister.objects.filter(
                특채등록자=request.user
            ).order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                S_models.SpecialRegister.objects.filter(특채등록자=request.user)
                .filter(
                    Q(특채신청등록__제품__모델명__contains=self.search)
                    | Q(특채신청등록__제품__모델코드__contains=self.search)
                    | Q(특채신청등록__고객사__거래처명__contains=self.search)
                    | Q(특채등록자__first_name__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


class specialrequestlist(core_views.onelist):
    templatename = "qualitycontrols/specialrequestlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            materialchecklist = S_models.SpecialApplyRegister.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in materialchecklist:
                try:
                    s.특채등록
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            materialchecklist = S_models.SpecialApplyRegister.objects.filter(
                Q(특채발행번호__contains=self.search)
                | Q(제품__모델코드__contains=self.search)
                | Q(제품__모델명__contains=self.search)
                | Q(수주__수주코드__contains=self.search)
                | Q(고객사__거래처명__contains=self.search)
                | Q(작성자__first_name__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in materialchecklist:
                try:
                    s.특채등록
                except:
                    queryset.append(s)
        return queryset


def specialregister(request, pk):
    user = request.user
    special = S_models.SpecialApplyRegister.objects.get_or_none(pk=pk)
    num = special.특채신청수량
    form = forms.SpecialRegisterForm(request.POST or None)
    form.initial = {
        "특채수량": num,
    }
    for field in form:
        if field.name == "특채수량":
            field.add_help_text = f"특채신청수량은 {num}입니다."

    if form.is_valid():
        특채등록일 = form.cleaned_data.get("특채등록일")
        특채수량 = form.cleaned_data.get("특채수량")
        if 특채등록일 is None:
            특채등록일 = timezone.now().date()

        SM = S_models.SpecialRegister.objects.create(
            특채신청등록=special, 특채등록자=user, 특채등록일=특채등록일, 특채수량=특채수량,
        )

        messages.success(request, "특채등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:specialregisterlist"))
    return render(
        request,
        "qualitycontrols/specialregister.html",
        {"form": form, "special": special,},
    )


def specialdetail(request, pk):
    specialdetail = S_models.SpecialApplyRegister.objects.get_or_none(pk=pk)
    user = request.user

    return render(
        request,
        "qualitycontrols/specialdetail.html",
        {"specialdetail": specialdetail, "user": user,},
    )


def file_download_special(request, pk):
    """파일 다운로드 유니코드화 패치"""
    measure = S_models.SpecialApplyRegister.objects.get_or_none(pk=pk)
    filepath = measure.특채관련회의록첨부.path
    title = measure.특채관련회의록첨부.__str__()
    title = urllib.parse.quote(title.encode("utf-8"))
    title = title.replace("images/", "")

    with open(filepath, "rb") as f:
        response = HttpResponse(f, content_type="application/force-download")
        titling = 'attachment; filename="{}"'.format(title)
        response["Content-Disposition"] = titling
        return response


def specialconductdelete(request, pk):
    conduct = S_models.SpecialConductRegister.objects.get_or_none(pk=pk)
    special = conduct.특채.특채신청등록
    pk = special.pk
    conduct.delete()
    messages.success(request, "특채처리가 삭제되었습니다.")
    return redirect(reverse("qualitycontrols:specialdetail", kwargs={"pk": pk}))


def specialconductregister(request, pk):
    user = request.user
    specialregister = S_models.SpecialRegister.objects.get_or_none(pk=pk)
    pk = specialregister.특채신청등록.pk
    num = specialregister.특채수량

    form = forms.specialconductregisterForm(request.POST or None)
    form.initial = {
        "특채수량중납품수량": num,
    }
    for field in form:
        if field.name == "특채수량중납품수량":
            field.add_help_text = f"특채수량은 {num}입니다."

    if form.is_valid():
        특채수량중납품수량 = form.cleaned_data.get("특채수량중납품수량")

        SM = S_models.SpecialConductRegister.objects.create(
            특채수량중납품수량=특채수량중납품수량, 특채=specialregister,
        )

        messages.success(request, "특채처리 등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:specialdetail", kwargs={"pk": pk}))
    return render(
        request,
        "qualitycontrols/specialconductregister.html",
        {"form": form, "specialregister": specialregister,},
    )


def specialrejectdelete(request, pk):
    conduct = S_models.SpecialRejectRegister.objects.get_or_none(pk=pk)
    special = conduct.특채처리.특채.특채신청등록
    pk = special.pk
    conduct.delete()
    messages.success(request, "특채반품이 삭제되었습니다.")
    return redirect(reverse("qualitycontrols:specialdetail", kwargs={"pk": pk}))


def specialrejectregister(request, pk):
    user = request.user
    specialconduct = S_models.SpecialConductRegister.objects.get_or_none(pk=pk)
    pk = specialconduct.특채.특채신청등록.pk
    specialregister = specialconduct.특채
    num = specialregister.특채수량 - specialconduct.특채수량중납품수량

    form = forms.specialrejectregisterForm(request.POST or None)
    form.initial = {
        "특채반품수량": num,
    }
    for field in form:
        if field.name == "특채반품수량":
            field.add_help_text = f"특채수량 중 납품불가수량은 {num}입니다."

    if form.is_valid():
        특채반품수량 = form.cleaned_data.get("특채반품수량")
        SM = S_models.SpecialRejectRegister.objects.create(
            특채반품수량=특채반품수량, 특채처리=specialconduct, 작성자=user,
        )

        messages.success(request, "특채반품 등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:specialdetail", kwargs={"pk": pk}))
    return render(
        request,
        "qualitycontrols/specialrejectregister.html",
        {"form": form, "specialconduct": specialconduct,},
    )


class specialconductlist(core_views.onelist):
    templatename = "qualitycontrols/specialconductlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            materialchecklist = S_models.SpecialConductRegister.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in materialchecklist:
                try:
                    s.특채반품
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            materialchecklist = S_models.SpecialConductRegister.objects.filter(
                Q(특채__특채신청등록__특채발행번호__contains=self.search)
                | Q(특채__특채신청등록__제품__모델코드__contains=self.search)
                | Q(특채__특채신청등록__제품__모델명__contains=self.search)
                | Q(특채__특채신청등록__수주__수주코드__contains=self.search)
                | Q(특채__특채신청등록__고객사__거래처명__contains=self.search)
                | Q(작성자__first_name__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in materialchecklist:
                try:
                    s.특채반품
                except:
                    queryset.append(s)
        return queryset


def materialoutrequest(request):
    form = forms.materialoutrequest(request.POST or None)

    search = request.GET.get("search")
    if search is None:
        customer = SI_models.Material.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.Material.objects.filter(
            Q(작성자__first_name__contains=search)
            | Q(자재코드__contains=search)
            | Q(품목__contains=search)
            | Q(자재품명__contains=search)
            | Q(규격__contains=search)
            | Q(단위__contains=search)
            | Q(자재공급업체__거래처명__contains=search)
            | Q(특이사항__contains=search)
        ).order_by("-created")
        customer = qs

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = ["출고유형"]
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"

    if form.is_valid():
        자재 = form.cleaned_data.get("자재")
        출고요청수량 = form.cleaned_data.get("출고요청수량")
        if 자재.자재재고.출고요청제외수량 < 출고요청수량:
            messages.error(request, "출고요청수량이 가용재고보다 더 많습니다.")
            return render(
                request,
                "qualitycontrols/materialoutrequest.html",
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
        material = form.save()
        material.자재 = 자재
        material.출고요청자 = request.user
        material.save()
        form.save_m2m()

        messages.success(request, "자재출고요청이 등록되었습니다.")
        return redirect(reverse("qualitycontrols:managematerialoutrequest"))

    return render(
        request,
        "qualitycontrols/materialoutrequest.html",
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


class managematerialoutrequest(core_views.onelist):
    templatename = "qualitycontrols/managematerialoutrequest.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = SM_models.StockOfMaterialOutRequest.objects.filter(
                출고요청자=request.user
            ).order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                SM_models.StockOfMaterialOutRequest.objects.filter(출고요청자=request.user)
                .filter(
                    Q(자재__자재품명__contains=self.search)
                    | Q(자재__자재코드__contains=self.search)
                    | Q(출고요청수량__contains=self.search)
                    | Q(출고요청일__contains=self.search)
                    | Q(출고유형__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


def deletematerialoutrequest(request, pk):
    materialoutrequest = SM_models.StockOfMaterialOutRequest.objects.get_or_none(pk=pk)
    materialoutrequest.자재.자재재고.출고요청제외수량 += materialoutrequest.출고요청수량
    materialoutrequest.자재.자재재고.save()
    materialoutrequest.delete()
    messages.success(request, "자재출고요청이 철회되었습니다.")
    return redirect(reverse("qualitycontrols:managematerialoutrequest"))


def ASrequestlist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        s_order = []
        order = AS_models.ASRepairRequest.objects.all().order_by("-created")
        for s in order:
            try:
                s.수리내역서
            except:
                s_order.append(s)

        s_bool = False
    else:
        s_bool = True
        order = AS_models.ASRepairRequest.objects.filter(
            Q(신청자__contains=search)
            | Q(신청품목__모델명__contains=search)
            | Q(신청품목__모델코드__contains=search)
            | Q(수리요청코드__contains=search)
        ).order_by("-created")
        s_order = []
        for s in order:
            try:
                s.수리내역서
            except:
                s_order.append(s)

    pagediv = 7

    totalpage = int(math.ceil(len(s_order) / pagediv))
    paginator = Paginator(s_order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    s_order = paginator.get_page(page)
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
        "qualitycontrols/ASrequestlist.html",
        {
            "s_order": s_order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "nonpage": nonpage,
        },
    )


def repairregisterAS(request, pk):
    user = request.user
    ASrequest = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)

    form = forms.UploadRepairForm(request.POST)

    if form.is_valid():
        불량위치및자재 = form.cleaned_data.get("불량위치및자재")
        수리내용 = form.cleaned_data.get("수리내용")
        실수리수량 = form.cleaned_data.get("실수리수량")
        폐기수량 = form.cleaned_data.get("폐기수량")
        특이사항 = form.cleaned_data.get("특이사항")

        SM = QC_models.RepairRegister.objects.create(
            AS수리의뢰=ASrequest,
            수리최종="AS",
            작성자=user,
            불량위치및자재=불량위치및자재,
            특이사항=특이사항,
            수리내용=수리내용,
            실수리수량=실수리수량,
            폐기수량=폐기수량,
            제품=ASrequest.신청품목,
        )
        rM = QC_models.FinalCheck.objects.create(수리내역서=SM, 제품=SM.제품)

        messages.success(request, "수리내역서 등록이 완료되었습니다.(최종검사의뢰 완료)")
        return redirect(reverse("qualitycontrols:qualitycontrolshome"))
    return render(
        request,
        "qualitycontrols/repairregisterAS.html",
        {"form": form, "ASrequest": ASrequest,},
    )


def repairrequestdetail(request, pk):
    user = request.user
    repair = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)
    return render(
        request,
        "qualitycontrols/repairrequestdetail.html",
        {"repair": repair, "user": user,},
    )


def repairlist(request):
    user = request.user
    search_m = request.GET.get("search_m")
    if search_m is None:
        s_order_m = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="AS")
            .order_by("-created")
        )
        s_bool_m = False
    else:
        s_bool_m = True

        s_order_m = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="AS")
            .filter(
                Q(AS수리의뢰__수리요청코드__contains=search_m)
                | Q(AS수리의뢰__신청품목__모델명__contains=search_m)
                | Q(AS수리의뢰__신청품목__모델코드__contains=search_m)
                | Q(작성자__first_name__contains=search_m)
                | Q(불량위치및자재__contains=search_m)
                | Q(수리내용__contains=search_m)
            )
            .order_by("-created")
        )

    pagediv = 7

    totalpage_m = int(math.ceil(len(s_order_m) / pagediv))
    paginator_m = Paginator(s_order_m, pagediv, orphans=0)
    page_m = request.GET.get("page_m", "1")
    s_order_m = paginator_m.get_page(page_m)
    nextpage_m = int(page_m) + 1
    previouspage_m = int(page_m) - 1
    nonpage_m = False
    notsamebool_m = True
    if totalpage_m == 0:
        nonpage_m = True
    if int(page_m) == totalpage_m:
        notsamebool_m = False
    if (search_m is None) or (search_m == ""):
        search_m = "search"

    return render(
        request,
        "qualitycontrols/repairlist.html",
        {
            "s_order_m": s_order_m,
            "search_m": search_m,
            "page_m": page_m,
            "totalpage_m": totalpage_m,
            "notsamebool_m": notsamebool_m,
            "nextpage_m": nextpage_m,
            "previouspage_m": previouspage_m,
            "s_bool_m": s_bool_m,
            "nonpage_m": nonpage_m,
        },
    )


def AStotalregister(request, pk):

    user = request.user
    ASrequest = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "FC" + num
            obj = models.FinalCheckRegister.objects.get_or_none(최종검사코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.AStotalRegisterForm(request.POST or None)
    code = give_number()

    if form.is_valid():
        최종검사코드 = form.cleaned_data.get("최종검사코드")
        동작이상유무 = form.cleaned_data.get("동작이상유무")
        외형이상유무 = form.cleaned_data.get("외형이상유무")
        수리내역 = form.cleaned_data.get("수리내역")
        특기사항 = form.cleaned_data.get("특기사항")
        수리비 = form.cleaned_data.get("수리비")
        기본요금 = form.cleaned_data.get("기본요금")
        부품비 = form.cleaned_data.get("부품비")
        택배 = form.cleaned_data.get("택배")
        화물 = form.cleaned_data.get("화물")
        발송날짜 = form.cleaned_data.get("발송날짜")
        입금확인 = form.cleaned_data.get("입금확인")
        비고 = form.cleaned_data.get("비고")
        검시일 = form.cleaned_data.get("검시일")
        발송자 = form.cleaned_data.get("발송자")
        검시자 = form.cleaned_data.get("검시자")
        수리자 = form.cleaned_data.get("수리자")
        try:
            problem = 발송자
            발송자 = user_models.User.objects.filter(first_name=발송자)[0]
            problem = 검시자
            검시자 = user_models.User.objects.filter(first_name=검시자)[0]
            problem = 수리자
            수리자 = user_models.User.objects.filter(first_name=수리자)[0]
        except:
            messages.error(request, f"{problem}(이)가 등록된 사용자가 아닙니다.")
            return render(
                request,
                "qualitycontrols/AStotalregister.html",
                {
                    "ASrequest": ASrequest,
                    "최종검사코드": 최종검사코드,
                    "동작이상유무": 동작이상유무,
                    "외형이상유무": 외형이상유무,
                    "수리내역": 수리내역,
                    "특기사항": 특기사항,
                    "수리비": 수리비,
                    "기본요금": 기본요금,
                    "부품비": 부품비,
                    "택배": 택배,
                    "화물": 화물,
                    "발송날짜": 발송날짜,
                    "입금확인": 입금확인,
                    "비고": 비고,
                    "검시일": 검시일,
                    "발송자": 발송자,
                    "검시자": 검시자,
                    "수리자": 수리자,
                },
            )

        SM = QC_models.RepairRegister.objects.create(
            AS수리의뢰=ASrequest,
            수리최종="AS",
            작성자=user,
            특이사항=특기사항,
            수리내용=수리내역,
            제품=ASrequest.신청품목,
        )
        rM = QC_models.FinalCheck.objects.create(수리내역서=SM, 제품=SM.제품)
        la = QC_models.FinalCheckRegister.objects.create(
            최종검사의뢰=rM,
            검시자=검시자,
            제품=rM.제품,
            최종검사코드=최종검사코드,
            검시일=검시일,
            동작이상유무=동작이상유무,
            외형이상유무=외형이상유무,
            수리내역=수리내역,
            특기사항=특기사항,
            수리비=수리비,
            기본요금=기본요금,
            부품비=부품비,
            택배=택배,
            화물=화물,
            발송날짜=발송날짜,
            입금확인=입금확인,
            비고=비고,
            발송자=발송자,
            수리자=수리자,
        )

        messages.success(request, "AS총괄장 등록이 완료되었습니다.")

        return redirect(reverse("qualitycontrols:finalcheckdonelist"))

    else:
        form.cleaned_data = {}
        최종검사코드 = form.cleaned_data.get("최종검사코드", code)
        동작이상유무 = form.cleaned_data.get("동작이상유무", "")
        외형이상유무 = form.cleaned_data.get("외형이상유무", "")
        수리내역 = form.cleaned_data.get("수리내역", "")
        특기사항 = form.cleaned_data.get("특기사항", "")
        수리비 = form.cleaned_data.get("수리비", "")
        기본요금 = form.cleaned_data.get("기본요금", "")
        부품비 = form.cleaned_data.get("부품비", "")
        택배 = form.cleaned_data.get("택배", "")
        화물 = form.cleaned_data.get("화물", "")
        발송날짜 = form.cleaned_data.get("발송날짜", "")
        입금확인 = form.cleaned_data.get("입금확인", "")
        비고 = form.cleaned_data.get("비고", "")
        검시일 = form.cleaned_data.get("검시일", "")
        발송자 = form.cleaned_data.get("발송자", "")
        검시자 = form.cleaned_data.get("검시자", "")
        수리자 = form.cleaned_data.get("수리자", "")

        messages.error(request, f"정확히 입력해주세요.")
        return render(
            request,
            "qualitycontrols/AStotalregister.html",
            {
                "ASrequest": ASrequest,
                "최종검사코드": 최종검사코드,
                "동작이상유무": 동작이상유무,
                "외형이상유무": 외형이상유무,
                "수리내역": 수리내역,
                "특기사항": 특기사항,
                "수리비": 수리비,
                "기본요금": 기본요금,
                "부품비": 부품비,
                "택배": 택배,
                "화물": 화물,
                "발송날짜": 발송날짜,
                "입금확인": 입금확인,
                "비고": 비고,
                "검시일": 검시일,
                "발송자": 발송자,
                "검시자": 검시자,
                "수리자": 수리자,
            },
        )

    return render(
        request,
        "qualitycontrols/AStotalregister.html",
        {"form": form, "ASrequest": ASrequest, "code": code, "검시자": ""},
    )


def AStotaledit(request, pk):
    user = request.user
    ASrequest = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    form = forms.AStotalEditForm(request.POST or None)
    code = ASrequest.최종검사코드

    if form.is_valid():
        최종검사코드 = form.cleaned_data.get("최종검사코드")
        동작이상유무 = form.cleaned_data.get("동작이상유무")
        외형이상유무 = form.cleaned_data.get("외형이상유무")
        수리내역 = form.cleaned_data.get("수리내역")
        특기사항 = form.cleaned_data.get("특기사항")
        수리비 = form.cleaned_data.get("수리비")
        기본요금 = form.cleaned_data.get("기본요금")
        부품비 = form.cleaned_data.get("부품비")
        택배 = form.cleaned_data.get("택배")
        화물 = form.cleaned_data.get("화물")
        발송날짜 = form.cleaned_data.get("발송날짜")
        입금확인 = form.cleaned_data.get("입금확인")
        비고 = form.cleaned_data.get("비고")
        검시일 = form.cleaned_data.get("검시일")
        발송자 = form.cleaned_data.get("발송자")
        검시자 = form.cleaned_data.get("검시자")
        수리자 = form.cleaned_data.get("수리자")
        try:
            problem = 발송자
            발송자 = user_models.User.objects.filter(first_name=발송자)[0]
            problem = 검시자
            검시자 = user_models.User.objects.filter(first_name=검시자)[0]
            problem = 수리자
            수리자 = user_models.User.objects.filter(first_name=수리자)[0]
        except:
            messages.error(request, f"{problem}(이)가 등록된 사용자가 아닙니다.")
            return render(
                request,
                "qualitycontrols/AStotalregister.html",
                {
                    "ASrequest": ASrequest.최종검사의뢰.수리내역서.AS수리의뢰,
                    "최종검사코드": 최종검사코드,
                    "동작이상유무": 동작이상유무,
                    "외형이상유무": 외형이상유무,
                    "수리내역": 수리내역,
                    "특기사항": 특기사항,
                    "수리비": 수리비,
                    "기본요금": 기본요금,
                    "부품비": 부품비,
                    "택배": 택배,
                    "화물": 화물,
                    "발송날짜": 발송날짜,
                    "입금확인": 입금확인,
                    "비고": 비고,
                    "검시일": 검시일,
                    "발송자": 발송자,
                    "검시자": 검시자,
                    "수리자": 수리자,
                },
            )
        SM = ASrequest.최종검사의뢰.수리내역서
        SM.특이사항 = 특기사항
        SM.수리내용 = 수리내역

        SM.save()

        ASrequest.검시자 = 검시자
        ASrequest.최종검사코드 = 최종검사코드
        ASrequest.검시일 = 검시일
        ASrequest.동작이상유무 = 동작이상유무
        ASrequest.외형이상유무 = 외형이상유무
        ASrequest.수리내역 = 수리내역
        ASrequest.특기사항 = 특기사항
        ASrequest.수리비 = 수리비
        ASrequest.기본요금 = 기본요금
        ASrequest.부품비 = 부품비
        ASrequest.택배 = 택배
        ASrequest.화물 = 화물
        ASrequest.발송날짜 = 발송날짜
        ASrequest.입금확인 = 입금확인
        ASrequest.비고 = 비고
        ASrequest.발송자 = 발송자
        ASrequest.수리자 = 수리자
        ASrequest.save()

        messages.success(request, "AS총괄장 수정이 완료되었습니다.")

        return redirect(
            reverse(
                "qualitycontrols:repairdetail",
                kwargs={"pk": ASrequest.최종검사의뢰.수리내역서.pk},
            )
        )

    else:
        form.cleaned_data = {}
        최종검사코드 = form.cleaned_data.get("최종검사코드", ASrequest.최종검사코드)
        동작이상유무 = form.cleaned_data.get("동작이상유무", ASrequest.동작이상유무)
        외형이상유무 = form.cleaned_data.get("외형이상유무", ASrequest.외형이상유무)
        수리내역 = form.cleaned_data.get("수리내역", ASrequest.수리내역)
        특기사항 = form.cleaned_data.get("특기사항", ASrequest.특기사항)
        수리비 = form.cleaned_data.get("수리비", ASrequest.수리비)
        기본요금 = form.cleaned_data.get("기본요금", ASrequest.기본요금)
        부품비 = form.cleaned_data.get("부품비", ASrequest.부품비)
        택배 = form.cleaned_data.get("택배", ASrequest.택배)
        화물 = form.cleaned_data.get("화물", ASrequest.화물)
        발송날짜 = form.cleaned_data.get("발송날짜", ASrequest.발송날짜)
        입금확인 = form.cleaned_data.get("입금확인", ASrequest.입금확인)
        비고 = form.cleaned_data.get("비고", ASrequest.비고)
        검시일 = form.cleaned_data.get("검시일", ASrequest.검시일)
        발송자 = form.cleaned_data.get("발송자", ASrequest.발송자)
        검시자 = form.cleaned_data.get("검시자", ASrequest.검시자)
        수리자 = form.cleaned_data.get("수리자", ASrequest.수리자)

        messages.error(request, "내용을 입력해주세요.")
        return render(
            request,
            "qualitycontrols/AStotalregister.html",
            {
                "ASrequest": ASrequest.최종검사의뢰.수리내역서.AS수리의뢰,
                "최종검사코드": 최종검사코드,
                "동작이상유무": 동작이상유무,
                "외형이상유무": 외형이상유무,
                "수리내역": 수리내역,
                "특기사항": 특기사항,
                "수리비": 수리비,
                "기본요금": 기본요금,
                "부품비": 부품비,
                "택배": 택배,
                "화물": 화물,
                "발송날짜": 발송날짜,
                "입금확인": 입금확인,
                "비고": 비고,
                "검시일": 검시일,
                "발송자": 발송자,
                "검시자": 검시자,
                "수리자": 수리자,
            },
        )

    최종검사코드 = ASrequest.최종검사코드
    동작이상유무 = ASrequest.동작이상유무
    외형이상유무 = ASrequest.외형이상유무
    수리내역 = ASrequest.수리내역
    특기사항 = ASrequest.특기사항
    수리비 = ASrequest.수리비
    기본요금 = ASrequest.기본요금
    부품비 = ASrequest.부품비
    택배 = ASrequest.택배
    화물 = ASrequest.화물
    발송날짜 = ASrequest.발송날짜
    입금확인 = ASrequest.입금확인
    비고 = ASrequest.비고
    검시일 = ASrequest.검시일
    발송자 = ASrequest.발송자
    검시자 = ASrequest.검시자
    수리자 = ASrequest.수리자

    return render(
        request,
        "qualitycontrols/AStotalregister.html",
        {
            "ASrequest": ASrequest.최종검사의뢰.수리내역서.AS수리의뢰,
            "최종검사코드": 최종검사코드,
            "동작이상유무": 동작이상유무,
            "외형이상유무": 외형이상유무,
            "수리내역": 수리내역,
            "특기사항": 특기사항,
            "수리비": 수리비,
            "기본요금": 기본요금,
            "부품비": 부품비,
            "택배": 택배,
            "화물": 화물,
            "발송날짜": 발송날짜,
            "입금확인": 입금확인,
            "비고": 비고,
            "검시일": 검시일,
            "발송자": 발송자,
            "검시자": 검시자,
            "수리자": 수리자,
        },
    )


def AStotaldeleteensure(request, pk):
    ASrequest = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    return render(
        request, "qualitycontrols/AStotaldeleteensure.html", {"ASrequest": ASrequest},
    )


def AStotaldelete(request, pk):
    ASrequest = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    ASrepair = ASrequest.최종검사의뢰.수리내역서
    AScheckrequest = ASrequest.최종검사의뢰

    ASrequest.delete()
    AScheckrequest.delete()
    ASrepair.delete()

    return redirect(reverse("qualitycontrols:finalchecklist"))
