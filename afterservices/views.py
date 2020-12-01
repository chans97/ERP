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
from random import randint


class afterserviceshome(core_views.onelist):
    templatename = "afterservices/afterserviceshome.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = AS_models.ASRegisters.objects.order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = AS_models.ASRegisters.objects.filter(
                Q(접수번호__contains=self.search)
                | Q(접수일__contains=self.search)
                | Q(설치연도__contains=self.search)
                | Q(접수내용__contains=self.search)
                | Q(현장명__contains=self.search)
                | Q(주소__contains=self.search)
                | Q(의뢰자전화번호__contains=self.search)
                | Q(비용__contains=self.search)
                | Q(비고__contains=self.search)
                | Q(처리방법__contains=self.search)
            ).order_by("-created")
        return queryset


def ASregister(request):
    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "AR" + num
            obj = AS_models.ASRegisters.objects.get_or_none(접수번호=code)
            if obj:
                pass
            else:
                return code

    form = forms.ASRegisterForm(request.POST or None)
    code = give_number()
    form.initial = {
        "접수번호": code,
    }

    if form.is_valid():
        접수번호 = form.cleaned_data.get("접수번호")
        접수일 = form.cleaned_data.get("접수일")
        접수내용 = form.cleaned_data.get("접수내용")
        처리방법 = form.cleaned_data.get("처리방법")
        의뢰자전화번호 = form.cleaned_data.get("의뢰자전화번호")
        현장명 = form.cleaned_data.get("현장명")
        비용 = form.cleaned_data.get("비용")
        비고 = form.cleaned_data.get("비고")
        try:
            첨부파일 = request.FILES["첨부파일"]
        except:
            첨부파일 = None

        주소 = form.cleaned_data.get("주소")
        설치연도 = form.cleaned_data.get("설치연도")
        if 접수일 is None:
            접수일 = timezone.now().date()
        SM = AS_models.ASRegisters.objects.create(
            접수번호=접수번호,
            접수일=접수일,
            접수자=request.user,
            접수내용=접수내용,
            처리방법=처리방법,
            의뢰자전화번호=의뢰자전화번호,
            현장명=현장명,
            비용=비용,
            설치연도=설치연도,
            비고=비고,
            첨부파일=첨부파일,
            주소=주소,
        )
        messages.success(request, "AS접수가 등록되었습니다.")
        return redirect(reverse("afterservices:afterserviceshome"))

    notsamebool = True
    seletelist = [
        "처리방법",
        "비용",
    ]
    return render(
        request,
        "afterservices/ASregister.html",
        {"form": form, "seletelist": seletelist},
    )


class ASregisterall(core_views.onelist):
    templatename = "afterservices/ASregisterall.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = AS_models.ASRegisters.objects.order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = AS_models.ASRegisters.objects.filter(
                Q(접수번호__contains=self.search)
                | Q(접수내용__contains=self.search)
                | Q(처리방법__contains=self.search)
                | Q(접수자__first_name__contains=self.search)
                | Q(단품__모델코드__contains=self.search)
                | Q(단품__모델명__contains=self.search)
                | Q(랙__랙시리얼코드__contains=self.search)
                | Q(랙__랙모델명__contains=self.search)
                | Q(의뢰처__거래처명__contains=self.search)
            ).order_by("-created")
        return queryset


def ASrequestdetail(request, pk):
    asregister = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    post = request.POST
    if post:
        try:
            견적서 = request.FILES["견적서"]
        except:
            견적서 = None

        asregister.AS현장방문.견적서 = 견적서
        asregister.AS현장방문.save()

    return render(
        request, "afterservices/ASrequestdetail.html", {"asregister": asregister,}
    )


def costdelete(request, pk):
    asvisit = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    asvisit.AS현장방문.견적서 = None
    asvisit.AS현장방문.save()
    return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))


class ASRegistersedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = AS_models.ASRegisters
    template_name = "afterservices/ASregisteredit.html"
    form_class = forms.ASRegisterEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
        seletelist = [
            "처리방법",
            "비용",
        ]
        context["asregisters"] = asregisters
        context["seletelist"] = seletelist

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
        pk = asregisters.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))

    def form_valid(self, form):
        self.object = form.save()
        접수일 = form.cleaned_data.get("접수일")
        접수내용 = form.cleaned_data.get("접수내용")
        의뢰자전화번호 = form.cleaned_data.get("의뢰자전화번호")
        비용 = form.cleaned_data.get("비용")
        처리방법 = form.cleaned_data.get("처리방법")
        if 접수일 is None:
            접수일 = timezone.now().date()

        pk = self.kwargs.get("pk")
        asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
        asregisters.접수일 = 접수일
        asregisters.접수내용 = 접수내용
        asregisters.의뢰자전화번호 = 의뢰자전화번호
        asregisters.비용 = 비용
        asregisters.처리방법 = 처리방법
        asregisters.save()
        messages.success(self.request, "수정이 완료되었습니다.")
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))


def ASRegisterdeleteensure(request, pk):
    asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    return render(
        request,
        "afterservices/ASRegisterdeleteensure.html",
        {"asregisters": asregisters},
    )


def ASRegisterdelete(request, pk):
    asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    asregisters.delete()
    messages.success(request, "AS접수가 삭제되었습니다.")
    return redirect(reverse("afterservices:afterserviceshome"))


class ASregisterdoneinsidelist(core_views.onelist):
    templatename = "afterservices/ASregisterdoneinsidelist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            requestslist = AS_models.ASRegisters.objects.filter(처리방법="내부처리").order_by(
                "-created"
            )
            queryset = []
            for s in requestslist:
                try:
                    s
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            requestslist = (
                AS_models.ASRegisters.objects.filter(처리방법="내부처리")
                .filter(
                    Q(접수번호__contains=self.search)
                    | Q(접수내용__contains=self.search)
                    | Q(처리방법__contains=self.search)
                    | Q(접수자__first_name__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(랙__랙시리얼코드__contains=self.search)
                    | Q(랙__랙모델명__contains=self.search)
                    | Q(의뢰처__거래처명__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in requestslist:
                try:
                    s
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)
        return queryset


def ASdoneinside(request, pk):
    asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    form = forms.ASdoneinsideForm(request.POST or None)

    if form.is_valid():
        처리내용 = form.cleaned_data.get("처리내용")

        AS_models.ASResults.objects.create(
            내부처리=asregisters,
            완료확인자=request.user,
            완료날짜=timezone.now().date(),
            완료유형="내부처리",
            처리내용=처리내용,
        )
        messages.success(request, "해당 AS가 완료 처리되었습니다.")
        return redirect(reverse("afterservices:afterserviceshome"))

    seletelist = [
        "AS방법",
    ]
    return render(
        request,
        "afterservices/ASdoneinside.html",
        {"asregisters": asregisters, "form": form, "seletelist": seletelist,},
    )


def ASsuccessdeleteensure(request, pk):
    assuccess = AS_models.ASResults.objects.get_or_none(pk=pk)
    return render(
        request, "afterservices/ASsuccessdeleteensure.html", {"assuccess": assuccess},
    )


def ASsuccessdelete(request, pk):
    assuccess = AS_models.ASResults.objects.get_or_none(pk=pk)
    if assuccess.완료유형 == "내부처리":
        pk = assuccess.내부처리.pk
    elif assuccess.완료유형 == "방문":
        pk = assuccess.방문.AS접수.pk
    else:
        pk = assuccess.재방문.전AS현장방문.AS접수.pk

    assuccess.delete()
    messages.success(request, "AS완료가 철회되었습니다.")
    return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk,}))


class ASvisitneedlist(core_views.onelist):
    templatename = "afterservices/ASvisitneedlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASRegisters.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                except:
                    if s.처리방법 == "현장방문":
                        queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = AS_models.ASRegisters.objects.filter(
                Q(접수번호__contains=self.search)
                | Q(접수일__contains=self.search)
                | Q(설치연도__contains=self.search)
                | Q(접수내용__contains=self.search)
                | Q(현장명__contains=self.search)
                | Q(주소__contains=self.search)
                | Q(의뢰자전화번호__contains=self.search)
                | Q(비용__contains=self.search)
                | Q(비고__contains=self.search)
                | Q(처리방법__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                except:
                    if s.처리방법 == "현장방문":
                        queryset.append(s)
        return queryset


class ASpostlist(core_views.onelist):
    templatename = "afterservices/ASpostlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASRegisters.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                except:
                    if s.처리방법 == "택배수령":
                        queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = AS_models.ASRegisters.objects.filter(
                Q(접수번호__contains=self.search)
                | Q(접수일__contains=self.search)
                | Q(설치연도__contains=self.search)
                | Q(접수내용__contains=self.search)
                | Q(현장명__contains=self.search)
                | Q(주소__contains=self.search)
                | Q(의뢰자전화번호__contains=self.search)
                | Q(비용__contains=self.search)
                | Q(비고__contains=self.search)
                | Q(처리방법__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                except:
                    if s.처리방법 == "현장방문":
                        queryset.append(s)
        return queryset


def ASvisitregister(request, pk):
    ASrequest = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    form = forms.ASvisitRegisterForm(request.POST or None)

    if form.is_valid():
        AS날짜 = form.cleaned_data.get("AS날짜")
        AS방법 = form.cleaned_data.get("AS방법")
        처리방법 = form.cleaned_data.get("처리방법")
        처리기사 = form.cleaned_data.get("처리기사")
        견적진행여부 = form.cleaned_data.get("견적진행여부")
        견적서첨부 = form.cleaned_data.get("견적서첨부")
        특이사항 = form.cleaned_data.get("특이사항")
        try:
            첨부파일 = request.FILES["첨부파일"]
        except:
            첨부파일 = None
        try:
            견적서첨부 = request.FILES["견적서첨부"]
        except:
            견적서첨부 = None

        if AS날짜 is None:
            AS날짜 = timezone.now().date()
        SM = AS_models.ASVisitContents.objects.create(
            AS날짜=AS날짜,
            AS방법=AS방법,
            처리방법=처리방법,
            견적진행여부=견적진행여부,
            견적서첨부=견적서첨부,
            AS접수=ASrequest,
            입력자=request.user,
            특이사항=특이사항,
            첨부파일=첨부파일,
        )
        messages.success(request, "AS현장방문이 등록되었습니다.")
        if ASrequest.처리방법 == "현장방문":
            return redirect(reverse("afterservices:ASvisitneedlist"))
        else:
            return redirect(reverse("afterservices:ASpostlist"))

    seletelist = [
        "AS방법",
        "AS방법",
        "처리방법",
        "견적진행여부",
    ]
    return render(
        request,
        "afterservices/ASvisitregister.html",
        {"ASrequest": ASrequest, "form": form, "seletelist": seletelist,},
    )


class ASvisitedit(UpdateView):
    model = AS_models.ASVisitContents
    template_name = "afterservices/ASvisitregister.html"
    form_class = forms.ASvisitEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        ASrequest = visitRegister
        seletelist = [
            "AS방법",
            "처리방법",
            "견적진행여부",
        ]
        context["ASrequest"] = ASrequest.AS접수
        context["seletelist"] = seletelist

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        pk = visitRegister.AS접수.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))

    def form_valid(self, form):
        self.object = form.save()
        AS날짜 = form.cleaned_data.get("AS날짜")
        AS방법 = form.cleaned_data.get("AS방법")
        처리방법 = form.cleaned_data.get("처리방법")
        처리기사 = form.cleaned_data.get("처리기사")
        견적진행여부 = form.cleaned_data.get("견적진행여부")
        특이사항 = form.cleaned_data.get("특이사항")
        if AS날짜 is None:
            AS날짜 = timezone.now().date()

        pk = self.kwargs.get("pk")
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        visitRegister.AS날짜 = AS날짜
        visitRegister.AS방법 = AS방법
        visitRegister.처리방법 = 처리방법
        visitRegister.처리기사 = 처리기사
        visitRegister.견적진행여부 = 견적진행여부
        visitRegister.특이사항 = 특이사항
        visitRegister.save()
        messages.success(self.request, "수정이 완료되었습니다.")
        pk = visitRegister.AS접수.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))


def ASvisitdeleteensure(request, pk):
    visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    return render(
        request,
        "afterservices/ASvisitdeleteensure.html",
        {"visitRegister": visitRegister},
    )


def ASvisitdelete(request, pk):
    visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    visitRegister.delete()
    messages.success(request, "AS현장방문이 삭제되었습니다.")
    return redirect(reverse("afterservices:afterserviceshome"))


class ASrevisitneedlist(core_views.onelist):
    templatename = "afterservices/ASrevisitneedlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASVisitContents.objects.filter(재방문여부="재방문").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                AS_models.ASVisitContents.objects.filter(재방문여부="재방문")
                .filter(
                    Q(AS방법__contains=self.search)
                    | Q(고객이름__contains=self.search)
                    | Q(AS처리내역__contains=self.search)
                    | Q(특이사항__contains=self.search)
                    | Q(AS현장방문요청__AS접수__접수번호__contains=self.search)
                    | Q(AS현장방문요청__AS접수__의뢰처__거래처명__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(랙__랙모델명__contains=self.search)
                    | Q(랙__랙시리얼코드__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    queryset.append(s)
        return queryset


def ASrevisitregister(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    form = forms.ASrevisitRegisterForm(request.POST or None)

    if form.is_valid():
        AS날짜 = form.cleaned_data.get("AS날짜")
        AS방법 = form.cleaned_data.get("AS방법")
        고객이름 = form.cleaned_data.get("고객이름")
        AS처리내역 = form.cleaned_data.get("AS처리내역")
        특이사항 = form.cleaned_data.get("특이사항")
        if AS날짜 is None:
            AS날짜 = timezone.now().date()
        SM = AS_models.ASReVisitContents.objects.create(
            AS날짜=AS날짜,
            AS방법=AS방법,
            고객이름=고객이름,
            AS처리내역=AS처리내역,
            특이사항=특이사항,
            전AS현장방문=ASvisit,
            수리기사=request.user,
            단품=ASvisit.단품,
            랙=ASvisit.랙,
        )
        messages.success(request, "AS현장재방문이 등록되었습니다.")
        return redirect(reverse("afterservices:ASrevisitneedlist"))

    seletelist = [
        "AS방법",
    ]
    return render(
        request,
        "afterservices/ASrevisitregister.html",
        {"ASvisit": ASvisit, "form": form, "seletelist": seletelist,},
    )


class ASrevisitedit(UpdateView):
    model = AS_models.ASReVisitContents
    template_name = "afterservices/ASrevisitregister.html"
    form_class = forms.ASrevisitRegisterForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        visitRegister = AS_models.ASReVisitContents.objects.get_or_none(pk=pk)
        ASvisit = visitRegister.전AS현장방문
        seletelist = [
            "AS방법",
        ]
        context["ASvisit"] = ASvisit
        context["seletelist"] = seletelist

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        pk = visitRegister.전AS현장방문.AS접수.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))

    def form_valid(self, form):
        self.object = form.save()
        AS날짜 = form.cleaned_data.get("AS날짜")
        AS방법 = form.cleaned_data.get("AS방법")
        고객이름 = form.cleaned_data.get("고객이름")
        AS처리내역 = form.cleaned_data.get("AS처리내역")
        특이사항 = form.cleaned_data.get("특이사항")
        if AS날짜 is None:
            AS날짜 = timezone.now().date()

        pk = self.kwargs.get("pk")
        visitRegister = AS_models.ASReVisitContents.objects.get_or_none(pk=pk)
        visitRegister.AS날짜 = AS날짜
        visitRegister.AS방법 = AS방법
        visitRegister.고객이름 = 고객이름
        visitRegister.AS처리내역 = AS처리내역
        visitRegister.특이사항 = 특이사항
        visitRegister.save()
        messages.success(self.request, "수정이 완료되었습니다.")
        pk = visitRegister.전AS현장방문.AS접수.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))


def ASrevisitdeleteensure(request, pk):
    revisitRegister = AS_models.ASReVisitContents.objects.get_or_none(pk=pk)
    return render(
        request,
        "afterservices/ASrevisitdeleteensure.html",
        {"revisitRegister": revisitRegister},
    )


def ASrevisitdelete(request, pk):
    revisitRegister = AS_models.ASReVisitContents.objects.get_or_none(pk=pk)
    revisitRegister.delete()
    messages.success(request, "AS현장재방문이 삭제되었습니다.")
    return redirect(reverse("afterservices:afterserviceshome"))


class ASsuccesslist(core_views.threelist):
    templatename = "afterservices/ASsuccesslist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASRegisters.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS완료
                except:
                    if s.처리방법 == "내부처리":
                        queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = AS_models.ASRegisters.objects.filter(
                Q(접수번호__contains=self.search)
                | Q(접수일__contains=self.search)
                | Q(설치연도__contains=self.search)
                | Q(접수내용__contains=self.search)
                | Q(현장명__contains=self.search)
                | Q(주소__contains=self.search)
                | Q(의뢰자전화번호__contains=self.search)
                | Q(비용__contains=self.search)
                | Q(비고__contains=self.search)
                | Q(처리방법__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS완료
                except:
                    if s.처리방법 == "내부처리":
                        queryset.append(s)
        return queryset

    def get_second_queryset(self, request):
        self.search2 = request.GET.get("search2")
        if self.search2 is None:
            order = AS_models.ASRegisters.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                    if s.AS현장방문.재방문여부 == "완료":
                        try:
                            s.AS현장방문.AS완료
                        except:
                            queryset.append(s)

                except:
                    pass

            self.s_bool2 = False
        else:
            # here
            self.s_bool2 = True
            order = AS_models.ASRegisters.objects.filter(
                Q(접수번호__contains=self.search2)
                | Q(접수일__contains=self.search2)
                | Q(설치연도__contains=self.search2)
                | Q(접수내용__contains=self.search2)
                | Q(현장명__contains=self.search2)
                | Q(주소__contains=self.search2)
                | Q(의뢰자전화번호__contains=self.search2)
                | Q(비용__contains=self.search2)
                | Q(비고__contains=self.search2)
                | Q(처리방법__contains=self.search2)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                    if s.AS현장방문.재방문여부 == "완료":
                        try:
                            s.AS현장방문.AS완료
                        except:
                            queryset.append(s)

                except:
                    pass

        return queryset

    def get_third_queryset(self, request):
        self.search3 = request.GET.get("search3")
        if self.search3 is None:
            order = AS_models.ASVisitContents.objects.filter(재방문여부="재방문").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                    try:
                        s.AS재방문.AS완료
                    except:
                        queryset.append(s)
                except:
                    pass

            self.s_bool3 = False
        else:
            self.s_bool3 = True
            order = (
                AS_models.ASVisitContents.objects.filter(재방문여부="재방문")
                .filter(
                    Q(AS방법__contains=self.search3)
                    | Q(고객이름__contains=self.search3)
                    | Q(AS처리내역__contains=self.search3)
                    | Q(특이사항__contains=self.search3)
                    | Q(AS현장방문요청__AS접수__접수번호__contains=self.search3)
                    | Q(AS현장방문요청__AS접수__의뢰처__거래처명__contains=self.search3)
                    | Q(단품__모델명__contains=self.search3)
                    | Q(단품__모델코드__contains=self.search3)
                    | Q(랙__랙모델명__contains=self.search3)
                    | Q(랙__랙시리얼코드__contains=self.search3)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                    try:
                        s.AS재방문.AS완료
                    except:
                        queryset.append(s)
                except:
                    pass

        return queryset


def ASdonevisit(request, pk):
    asvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    AS_models.ASResults.objects.create(
        방문=asvisit, 완료확인자=request.user, 완료날짜=timezone.now().date(), 완료유형="방문",
    )
    messages.success(request, "해당 AS가 완료 처리되었습니다.")
    return redirect(reverse("afterservices:ASsuccesslist"))


def ASdonerevisit(request, pk):
    asrevisit = AS_models.ASReVisitContents.objects.get_or_none(pk=pk)
    AS_models.ASResults.objects.create(
        재방문=asrevisit, 완료확인자=request.user, 완료날짜=timezone.now().date(), 완료유형="재방문",
    )
    messages.success(request, "해당 AS가 완료 처리되었습니다.")
    return redirect(reverse("afterservices:ASsuccesslist"))


class ASrepairorderalllist(core_views.onelist):
    templatename = "afterservices/ASrepairorderalllist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = AS_models.ASRepairRequest.objects.filter(
                신청자=self.request.user
            ).order_by("-created")
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                AS_models.ASRepairRequest.objects.filter(신청자=self.request.user)
                .filter(
                    Q(수리요청코드__contains=self.search)
                    | Q(신청자__first_name__contains=self.search)
                    | Q(신청품목__모델코드__contains=self.search)
                    | Q(신청품목__모델명__contains=self.search)
                    | Q(AS현장방문__AS현장방문요청__AS접수__접수번호__contains=self.search)
                )
                .order_by("-created")
            )

        return queryset


def repairrequestdetail(request, pk):
    user = request.user
    repair = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)
    return render(
        request,
        "afterservices/repairrequestdetail.html",
        {"repair": repair, "user": user,},
    )


class ASexrepairlist(core_views.onelist):
    templatename = "afterservices/ASexrepairlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = (
                AS_models.ASVisitContents.objects.filter(입력자=self.request.user)
                .filter(AS방법="제품수리")
                .filter(재방문여부="재방문")
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                AS_models.ASVisitContents.objects.filter(입력자=self.request.user)
                .filter(AS방법="제품수리")
                .filter(재방문여부="재방문")
                .filter(
                    Q(AS방법__contains=self.search)
                    | Q(고객이름__contains=self.search)
                    | Q(AS처리내역__contains=self.search)
                    | Q(특이사항__contains=self.search)
                    | Q(AS현장방문요청__AS접수__접수번호__contains=self.search)
                    | Q(AS현장방문요청__AS접수__의뢰처__거래처명__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(랙__랙모델명__contains=self.search)
                    | Q(랙__랙시리얼코드__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)

        return queryset


def ASrepairrequestregister(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    if ASvisit.접수제품분류 == "단품":
        return redirect(
            reverse("afterservices:ASrepairrequestregistersingle", kwargs={"pk": pk,})
        )
    else:
        return redirect(
            reverse("afterservices:ASrepairrequestregisterrack", kwargs={"pk": pk,})
        )


def ASrepairrequestregistersingle(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "RR" + num
            obj = AS_models.ASRepairRequest.objects.get_or_none(수리요청코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.ASrepairrequestregisterForm(request.POST or None)
    code = give_number()
    single = ASvisit.단품
    form.initial = {"수리요청코드": code, "신청품목": single.모델코드}
    for field in form:
        if field.name == "신청품목":
            field.help_text_add = f"*기본값은 <{single.모델명}>의 모델코드입니다."

    if form.is_valid():
        신청품목 = form.cleaned_data.get("신청품목")
        수리요청코드 = form.cleaned_data.get("수리요청코드")
        신청수량 = form.cleaned_data.get("신청수량")
        고객성명 = form.cleaned_data.get("고객성명")
        고객주소 = form.cleaned_data.get("고객주소")
        고객전화 = form.cleaned_data.get("고객전화")
        고객팩스 = form.cleaned_data.get("고객팩스")
        시리얼번호 = form.cleaned_data.get("시리얼번호")
        사용자액세서리 = form.cleaned_data.get("사용자액세서리")
        AS의뢰내용 = form.cleaned_data.get("AS의뢰내용")
        택배관련 = form.cleaned_data.get("택배관련")
        SM = AS_models.ASRepairRequest.objects.create(
            신청품목=신청품목,
            수리요청코드=수리요청코드,
            신청수량=신청수량,
            AS현장방문=ASvisit,
            신청자=request.user,
            고객성명=고객성명,
            고객주소=고객주소,
            고객전화=고객전화,
            고객팩스=고객팩스,
            시리얼번호=시리얼번호,
            사용자액세서리=사용자액세서리,
            택배관련=택배관련,
            AS의뢰내용=AS의뢰내용,
        )
        messages.success(request, "AS수리의뢰가 등록되었습니다.")
        return redirect(reverse("afterservices:ASrepairorderalllist"))

    seletelist = [
        "택배관련",
    ]
    return render(
        request,
        "afterservices/ASrepairrequestregistersingle.html",
        {"ASvisit": ASvisit, "form": form, "seletelist": seletelist,},
    )


def ASrepairrequestregisterrack(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    rack = ASvisit.랙
    singlelist = []
    for single in rack.랙구성단품.all():
        if single.랙구성 == "단품":
            sipk = single.랙구성단품_id
            sin = SI_models.SingleProduct.objects.get(pk=sipk)
            singlelist.append(sin)

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "RR" + num
            obj = AS_models.ASRepairRequest.objects.get_or_none(수리요청코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.ASrepairrequestregisterRackForm(request.POST or None)
    code = give_number()
    form.initial = {
        "수리요청코드": code,
    }

    if form.is_valid():
        신청품목 = form.cleaned_data.get("신청품목")
        수리요청코드 = form.cleaned_data.get("수리요청코드")
        신청수량 = form.cleaned_data.get("신청수량")
        고객성명 = form.cleaned_data.get("고객성명")
        고객주소 = form.cleaned_data.get("고객주소")
        고객전화 = form.cleaned_data.get("고객전화")
        고객팩스 = form.cleaned_data.get("고객팩스")
        시리얼번호 = form.cleaned_data.get("시리얼번호")
        사용자액세서리 = form.cleaned_data.get("사용자액세서리")
        AS의뢰내용 = form.cleaned_data.get("AS의뢰내용")
        택배관련 = form.cleaned_data.get("택배관련")
        spk = int(신청품목)
        신청품목 = SI_models.SingleProduct.objects.get(pk=spk)

        SM = AS_models.ASRepairRequest.objects.create(
            신청품목=신청품목,
            수리요청코드=수리요청코드,
            신청수량=신청수량,
            AS현장방문=ASvisit,
            신청자=request.user,
            고객성명=고객성명,
            고객주소=고객주소,
            고객전화=고객전화,
            고객팩스=고객팩스,
            시리얼번호=시리얼번호,
            사용자액세서리=사용자액세서리,
            택배관련=택배관련,
            AS의뢰내용=AS의뢰내용,
        )
        messages.success(request, "AS수리의뢰가 등록되었습니다.")
        return redirect(reverse("afterservices:ASrepairorderalllist"))
    seletelist = [
        "택배관련",
    ]

    return render(
        request,
        "afterservices/ASrepairrequestregisterrack.html",
        {
            "ASvisit": ASvisit,
            "form": form,
            "singlelist": singlelist,
            "seletelist": seletelist,
        },
    )


class RackDetialView(user_mixins.LoggedInOnlyView, DetailView):
    model = SI_models.RackProduct

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        rack = SI_models.RackProduct.objects.get(pk=pk)

        single = rack.랙구성단품.filter(랙구성="단품")
        material = rack.랙구성단품.filter(랙구성="자재")
        user = request.user
        return render(
            request,
            "afterservices/rackdetail.html",
            {"rack": rack, "user": user, "material": material, "single": single},
        )


class SingleDetialView(user_mixins.LoggedInOnlyView, DetailView):
    model = SI_models.SingleProduct

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        single = SI_models.SingleProduct.objects.get(pk=pk)

        material = single.단품구성자재.all()
        user = request.user
        return render(
            request,
            "afterservices/singledetail.html",
            {"single": single, "user": user, "material": material},
        )


def repairrequestdeleteensure(request, pk):
    repairrequest = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)
    return render(
        request,
        "afterservices/repairrequestdeleteensure.html",
        {"repairrequest": repairrequest},
    )


def repairrequestdelete(request, pk):
    repairrequest = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)
    repairrequest.delete()
    messages.success(request, "AS수리요청이 삭제되었습니다.")
    return redirect(reverse("afterservices:ASrepairorderalllist"))


class ASsingleoutalllist(core_views.onelist):
    templatename = "afterservices/ASsingleoutalllist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = (
                SS_models.StockOfSingleProductOutRequest.objects.filter(수주AS="AS")
                .filter(출하요청자=self.request.user)
                .order_by("-created")
            )
            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                SS_models.StockOfSingleProductOutRequest.objects.filter(수주AS="AS")
                .filter(출하요청자=self.request.user)
                .filter(
                    Q(AS__AS현장방문요청__AS접수__접수번호__contains=self.search)
                    | Q(출하요청자__first_name__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(고객사__거래처명__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


class ASexsingleoutlist(core_views.onelist):
    templatename = "afterservices/ASexsingleoutlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = (
                AS_models.ASVisitContents.objects.filter(입력자=self.request.user)
                .filter(AS방법="제품교체")
                .filter(재방문여부="재방문")
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                AS_models.ASVisitContents.objects.filter(입력자=self.request.user)
                .filter(AS방법="제품교체")
                .filter(재방문여부="재방문")
                .filter(
                    Q(AS방법__contains=self.search)
                    | Q(고객이름__contains=self.search)
                    | Q(AS처리내역__contains=self.search)
                    | Q(특이사항__contains=self.search)
                    | Q(AS현장방문요청__AS접수__접수번호__contains=self.search)
                    | Q(AS현장방문요청__AS접수__의뢰처__거래처명__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(랙__랙모델명__contains=self.search)
                    | Q(랙__랙시리얼코드__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)

        return queryset


def orderstocksingledelete(request, pk):
    orderstocksingle = SS_models.StockOfSingleProductOutRequest.objects.get(pk=pk)
    출하요청수량 = orderstocksingle.출하요청수량
    단품 = orderstocksingle.단품
    재고 = 단품.단품재고
    재고.출하요청제외수량 += 출하요청수량
    재고.save()

    messages.success(request, "출하요청이 철회되었습니다.")
    orderstocksingle.delete()
    return redirect(reverse("afterservices:ASsingleoutalllist"))


def ASsingleoutrequestregister(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    if ASvisit.접수제품분류 == "단품":
        return redirect(
            reverse(
                "afterservices:ASsingleoutrequestregistersingle", kwargs={"pk": pk,}
            )
        )
    else:
        return redirect(
            reverse("afterservices:ASsingleoutrequestregisterrack", kwargs={"pk": pk,})
        )


def ASsingleoutrequestregistersingle(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    form = forms.ASsingleoutrequestregistersingleForm(request.POST or None)
    if form.is_valid():
        출하희망일 = form.cleaned_data.get("출하희망일")
        출하요청수량 = form.cleaned_data.get("출하요청수량")
        if ASvisit.단품.단품재고.출하요청제외수량 < 출하요청수량:
            messages.error(request, "출하요청수량이 출하요청제외수량보다 더 많습니다.")
            return render(
                request,
                "afterservices/ASsingleoutrequestregistersingle.html",
                {"ASvisit": ASvisit, "form": form,},
            )
        SM = SS_models.StockOfSingleProductOutRequest.objects.create(
            수주AS="AS",
            단품=ASvisit.단품,
            AS=ASvisit,
            고객사=ASvisit.AS접수.의뢰처,
            출하요청수량=출하요청수량,
            출하요청자=request.user,
            출하희망일=출하희망일,
        )
        messages.success(request, "단품출하요청이 등록되었습니다.")
        return redirect(reverse("afterservices:ASsingleoutalllist"))

    return render(
        request,
        "afterservices/ASsingleoutrequestregistersingle.html",
        {"ASvisit": ASvisit, "form": form,},
    )


def ASsingleoutrequestregisterrack(request, pk):
    ASvisit = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
    rack = ASvisit.랙
    singlelist = []
    for single in rack.랙구성단품.all():
        if single.랙구성 == "단품":
            sipk = single.랙구성단품_id
            sin = SI_models.SingleProduct.objects.get(pk=sipk)
            singlelist.append(sin)
    form = forms.ASsingleoutrequestregisterrackForm(request.POST or None)
    seletelist = []
    if form.is_valid():
        출하희망일 = form.cleaned_data.get("출하희망일")
        출하요청수량 = form.cleaned_data.get("출하요청수량")
        신청품목 = form.cleaned_data.get("신청품목")
        spk = int(신청품목)
        신청품목 = SI_models.SingleProduct.objects.get(pk=spk)

        if 신청품목.단품재고.출하요청제외수량 < 출하요청수량:
            messages.error(request, "출하요청수량이 출하요청제외수량보다 더 많습니다.")
            return render(
                request,
                "afterservices/ASsingleoutrequestregisterrack.html",
                {
                    "ASvisit": ASvisit,
                    "form": form,
                    "singlelist": singlelist,
                    "seletelist": seletelist,
                },
            )

        SM = SS_models.StockOfSingleProductOutRequest.objects.create(
            수주AS="AS",
            단품=신청품목,
            AS=ASvisit,
            고객사=ASvisit.AS접수.의뢰처,
            출하요청수량=출하요청수량,
            출하요청자=request.user,
            출하희망일=출하희망일,
        )
        messages.success(request, "단품출하요청이 등록되었습니다.")
        return redirect(reverse("afterservices:ASsingleoutalllist"))

    return render(
        request,
        "afterservices/ASsingleoutrequestregisterrack.html",
        {
            "ASvisit": ASvisit,
            "form": form,
            "singlelist": singlelist,
            "seletelist": seletelist,
        },
    )


def ASdonenonvisit(request, pk):
    asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)

    form = forms.ASdoneinsideForm(request.POST or None)

    if form.is_valid():
        처리내용 = form.cleaned_data.get("처리내용")

        AS_models.ASResults.objects.create(
            내부처리=asregisters,
            완료확인자=request.user,
            완료날짜=timezone.now().date(),
            완료유형="내부처리",
            처리내용=처리내용,
        )
        messages.success(request, "해당 AS가 완료 처리되었습니다.")
        return redirect(reverse("afterservices:afterserviceshome"))

    return render(
        request,
        "afterservices/ASdoneinside.html",
        {"asregisters": asregisters, "form": form,},
    )


class AScashcheckneedlist(core_views.onelist):
    templatename = "afterservices/AScashcheckneedlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASVisitContents.objects.filter(재방문여부="견적진행").order_by(
                "-created"
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            order = (
                AS_models.ASVisitContents.objects.filter(재방문여부="견적진행")
                .filter(
                    Q(AS방법__contains=self.search)
                    | Q(고객이름__contains=self.search)
                    | Q(AS처리내역__contains=self.search)
                    | Q(특이사항__contains=self.search)
                    | Q(AS현장방문요청__AS접수__접수번호__contains=self.search)
                    | Q(AS현장방문요청__AS접수__의뢰처__거래처명__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(랙__랙모델명__contains=self.search)
                    | Q(랙__랙시리얼코드__contains=self.search)
                )
                .order_by("-created")
            )
            queryset = []
            for s in order:
                try:
                    s.AS재방문
                except:
                    queryset.append(s)
        return queryset


class asregiserfiledownload(core_views.Filedownload):
    model = models.ASRegisters
    filefolderName = "첨부파일"
    uploadto = "ASregister/"


class ASVCcostdownload(core_views.Filedownload):
    model = models.ASVisitContents
    filefolderName = "견적서첨부"
    uploadto = "cost/"


class ASVCfiledownload(core_views.Filedownload):
    model = models.ASVisitContents
    filefolderName = "첨부파일"
    uploadto = "ASVisitContents/"
