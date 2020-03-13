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


class finalchecklist(core_views.threelist):
    templatename = "qualitycontrols/finalchecklist.html"


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
        if 검시일 is None:
            검시일 = timezone.now().date()

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


class materialchecklist(core_views.onelist):
    pass


def materialcheckregister(request, pk):
    user = request.user
    materialcheck = QC_models.MaterialCheckRegister.objects.get_or_none(pk=pk)

    form = forms.MaterialCheckRegisterForm(request.POST)

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

        messages.success(request, "수입검사 등록이 완료되었습니다.")

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
    form = forms.LowMetarialRegisterForm(request.POST)

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
    form = forms.measurecheckregisterForm(request.POST)
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
    form = forms.measurerepairregisterForm(request.POST)
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

    form = forms.measureregisterForm(request.POST)
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
    form = forms.SpecialRegisterForm(request.POST)
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

    form = forms.specialconductregisterForm(request.POST)
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
