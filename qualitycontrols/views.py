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
            **response_kwargs
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
            **response_kwargs
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
