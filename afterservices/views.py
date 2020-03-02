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


class afterserviceshome(core_views.twolist):
    pass


def ASregister(request):
    form = forms.ASRegisterForm(request.POST)
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
        접수번호 = form.cleaned_data.get("접수번호")
        접수일 = form.cleaned_data.get("접수일")
        현상 = form.cleaned_data.get("현상")
        불량분류코드 = form.cleaned_data.get("불량분류코드")
        불량분류 = form.cleaned_data.get("불량분류")
        접수제품분류 = form.cleaned_data.get("접수제품분류")
        대응유형 = form.cleaned_data.get("대응유형")
        의뢰처 = form.cleaned_data.get("의뢰처")
        의뢰자전화번호 = form.cleaned_data.get("의뢰자전화번호")
        방문요청일 = form.cleaned_data.get("방문요청일")
        if 접수일 is None:
            접수일 = timezone.now().date()
        SM = AS_models.ASRegisters.objects.create(
            접수번호=접수번호,
            접수일=접수일,
            접수자=request.user,
            현상=현상,
            불량분류코드=불량분류코드,
            불량분류=불량분류,
            접수제품분류=접수제품분류,
            대응유형=대응유형,
            의뢰처=의뢰처,
            의뢰자전화번호=의뢰자전화번호,
            방문요청일=방문요청일,
        )

        pk = SM.pk

        if SM.접수제품분류 == "단품":
            return redirect(
                reverse("afterservices:afterservicesingle", kwargs={"pk": pk})
            )
        else:
            return redirect(
                reverse("afterservices:afterservicesrack", kwargs={"pk": pk})
            )

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = [
        "불량분류",
        "접수제품분류",
        "대응유형",
    ]
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "afterservices/ASregister.html",
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


def afterservicesingle(request, pk):
    form = forms.ASSingleForm(request.POST)
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
        SM = models.ASRegisters.objects.get(pk=pk)
        SM.단품 = 단품모델코드
        SM.save()

        messages.success(request, "AS접수가 등록되었습니다.")

        return redirect(reverse("afterservices:afterserviceshome"))

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
        "afterservices/afterservicesingle.html",
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


def afterservicesrack(request, pk):
    form = forms.ASRackForm(request.POST)

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
        SM = models.ASRegisters.objects.get(pk=pk)
        SM.랙 = 랙시리얼코드
        SM.save()

        messages.success(request, "AS접수가 등록되었습니다.")

        return redirect(reverse("afterservices:afterserviceshome"))

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
        "afterservices/afterservicesrack.html",
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


class ASvisitrequestslist(core_views.onelist):
    templatename = "afterservices/ASvisitrequestslist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            requestslist = AS_models.ASRegisters.objects.exclude(대응유형="내부처리").order_by(
                "-created"
            )
            queryset = []
            for s in requestslist:
                try:
                    s.AS현장방문요청
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            requestslist = (
                AS_models.ASRegisters.objects.exclude(대응유형="내부처리")
                .filter(
                    Q(접수번호__contains=self.search)
                    | Q(현상__contains=self.search)
                    | Q(대응유형__contains=self.search)
                    | Q(불량분류코드__contains=self.search)
                    | Q(불량분류__contains=self.search)
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
                    s.AS현장방문요청
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)
        return queryset


def ASvisitrequests(request, pk):
    asregister = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    AS_models.ASVisitRequests.objects.create(AS접수=asregister)
    messages.success(request, "AS방문요청이 완료되었습니다.")
    return redirect(reverse("afterservices:ASvisitrequestslist"))


class ASregisterall(core_views.onelist):
    templatename = "afterservices/ASregisterall.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            queryset = AS_models.ASRegisters.objects.all().order_by("-created")

            self.s_bool = False
        else:
            self.s_bool = True
            queryset = (
                AS_models.ASRegisters.objects.all()
                .filter(
                    Q(접수번호__contains=self.search)
                    | Q(현상__contains=self.search)
                    | Q(대응유형__contains=self.search)
                    | Q(불량분류코드__contains=self.search)
                    | Q(불량분류__contains=self.search)
                    | Q(접수자__first_name__contains=self.search)
                    | Q(단품__모델코드__contains=self.search)
                    | Q(단품__모델명__contains=self.search)
                    | Q(랙__랙시리얼코드__contains=self.search)
                    | Q(랙__랙모델명__contains=self.search)
                    | Q(의뢰처__거래처명__contains=self.search)
                )
                .order_by("-created")
            )
        return queryset


def ASrequestdetail(request, pk):
    asregister = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    return render(
        request, "afterservices/ASrequestdetail.html", {"asregister": asregister,}
    )


class ASRegistersedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = AS_models.ASRegisters
    template_name = "afterservices/ASregisteredit.html"
    form_class = forms.ASRegisterEditForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
        seletelist = [
            "불량분류",
            "대응유형",
        ]
        context["asregisters"] = asregisters
        context["seletelist"] = seletelist

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
        pk = asregisters.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))

    def form_valid(self, form):
        self.object = form.save()
        접수일 = form.cleaned_data.get("접수일")
        현상 = form.cleaned_data.get("현상")
        불량분류코드 = form.cleaned_data.get("불량분류코드")
        불량분류 = form.cleaned_data.get("불량분류")
        대응유형 = form.cleaned_data.get("대응유형")
        의뢰자전화번호 = form.cleaned_data.get("의뢰자전화번호")
        방문요청일 = form.cleaned_data.get("방문요청일")
        if 접수일 is None:
            접수일 = timezone.now().date()

        pk = self.kwargs.get("pk")
        asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
        asregisters.접수일 = 접수일
        asregisters.현상 = 현상
        asregisters.불량분류코드 = 불량분류코드
        asregisters.불량분류 = 불량분류
        asregisters.대응유형 = 대응유형
        asregisters.의뢰자전화번호 = 의뢰자전화번호
        asregisters.방문요청일 = 방문요청일
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
            requestslist = AS_models.ASRegisters.objects.filter(대응유형="내부처리").order_by(
                "-created"
            )
            queryset = []
            for s in requestslist:
                try:
                    s.AS현장방문요청
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            requestslist = (
                AS_models.ASRegisters.objects.filter(대응유형="내부처리")
                .filter(
                    Q(접수번호__contains=self.search)
                    | Q(현상__contains=self.search)
                    | Q(대응유형__contains=self.search)
                    | Q(불량분류코드__contains=self.search)
                    | Q(불량분류__contains=self.search)
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
                    s.AS현장방문요청
                except:
                    try:
                        s.AS완료
                    except:
                        queryset.append(s)
        return queryset


def ASdoneinside(request, pk):
    asregisters = AS_models.ASRegisters.objects.get_or_none(pk=pk)
    AS_models.ASResults.objects.create(
        내부처리=asregisters, 완료확인자=request.user, 완료날짜=timezone.now().date(), 완료유형="내부처리",
    )
    messages.success(request, "해당 AS가 완료 처리되었습니다.")
    return redirect(reverse("afterservices:ASregisterdoneinsidelist"))


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
        pk = assuccess.방문.AS현장방문요청.AS접수.pk
    else:
        pk = assuccess.재방문.전AS현장방문.AS현장방문요청.AS접수.pk

    assuccess.delete()
    messages.success(request, "AS완료가 철회되었습니다.")
    return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk,}))


class ASvisitneedlist(core_views.onelist):
    templatename = "afterservices/ASvisitneedlist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASVisitRequests.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                except:
                    queryset.append(s)

            self.s_bool = False
        else:
            self.s_bool = True
            order = AS_models.ASVisitRequests.objects.filter(
                Q(AS담당자__first_name__contains=self.search)
                | Q(AS접수__접수번호__contains=self.search)
                | Q(AS접수__현상__contains=self.search)
                | Q(AS접수__불량분류코드__contains=self.search)
                | Q(AS접수__대응유형__contains=self.search)
                | Q(AS접수__의뢰처__거래처명__contains=self.search)
                | Q(AS접수__단품__모델명__contains=self.search)
                | Q(AS접수__단품__모델코드__contains=self.search)
                | Q(AS접수__랙__랙모델명__contains=self.search)
                | Q(AS접수__랙__랙시리얼코드__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.AS현장방문
                except:
                    queryset.append(s)
        return queryset


def ASvisitregister(request, pk):
    ASrequest = AS_models.ASVisitRequests.objects.get_or_none(pk=pk)
    form = forms.ASvisitRegisterForm(request.POST)

    if form.is_valid():
        AS날짜 = form.cleaned_data.get("AS날짜")
        AS방법 = form.cleaned_data.get("AS방법")
        고객이름 = form.cleaned_data.get("고객이름")
        AS처리내역 = form.cleaned_data.get("AS처리내역")
        특이사항 = form.cleaned_data.get("특이사항")
        재방문여부 = form.cleaned_data.get("재방문여부")
        if AS날짜 is None:
            AS날짜 = timezone.now().date()
        SM = AS_models.ASVisitContents.objects.create(
            AS날짜=AS날짜,
            AS방법=AS방법,
            고객이름=고객이름,
            AS처리내역=AS처리내역,
            특이사항=특이사항,
            재방문여부=재방문여부,
            AS현장방문요청=ASrequest,
            수리기사=request.user,
            접수제품분류=ASrequest.AS접수.접수제품분류,
            단품=ASrequest.AS접수.단품,
            랙=ASrequest.AS접수.랙,
        )
        messages.success(request, "AS현장방문이 등록되었습니다.")
        return redirect(reverse("afterservices:ASvisitneedlist"))

    seletelist = [
        "AS방법",
        "재방문여부",
    ]
    return render(
        request,
        "afterservices/ASvisitregister.html",
        {"ASrequest": ASrequest, "form": form, "seletelist": seletelist,},
    )


class ASvisitedit(UpdateView):
    model = AS_models.ASVisitContents
    template_name = "afterservices/ASvisitregister.html"
    form_class = forms.ASvisitRegisterForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        ASrequest = visitRegister.AS현장방문요청
        seletelist = [
            "AS방법",
            "재방문여부",
        ]
        context["ASrequest"] = ASrequest
        context["seletelist"] = seletelist

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        pk = visitRegister.AS현장방문요청.AS접수.pk
        return redirect(reverse("afterservices:ASrequestdetail", kwargs={"pk": pk}))

    def form_valid(self, form):
        self.object = form.save()
        AS날짜 = form.cleaned_data.get("AS날짜")
        AS방법 = form.cleaned_data.get("AS방법")
        고객이름 = form.cleaned_data.get("고객이름")
        AS처리내역 = form.cleaned_data.get("AS처리내역")
        특이사항 = form.cleaned_data.get("특이사항")
        재방문여부 = form.cleaned_data.get("재방문여부")
        if AS날짜 is None:
            AS날짜 = timezone.now().date()

        pk = self.kwargs.get("pk")
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        visitRegister.AS날짜 = AS날짜
        visitRegister.AS방법 = AS방법
        visitRegister.고객이름 = 고객이름
        visitRegister.AS처리내역 = AS처리내역
        visitRegister.특이사항 = 특이사항
        visitRegister.재방문여부 = 재방문여부
        visitRegister.save()
        messages.success(self.request, "수정이 완료되었습니다.")
        pk = visitRegister.AS현장방문요청.AS접수.pk
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
    form = forms.ASrevisitRegisterForm(request.POST)

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
            접수제품분류=ASvisit.접수제품분류,
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
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        visitRegister = AS_models.ASVisitContents.objects.get_or_none(pk=pk)
        pk = visitRegister.전AS현장방문.AS현장방문요청.AS접수.pk
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
        pk = visitRegister.전AS현장방문.AS현장방문요청.AS접수.pk
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


class ASsuccesslist(core_views.twolist):
    templatename = "afterservices/ASsuccesslist.html"

    def get_first_queryset(self, request):
        user = self.request.user
        self.search = request.GET.get("search")
        if self.search is None:
            order = AS_models.ASVisitRequests.objects.all().order_by("-created")
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

            self.s_bool = False
        else:
            self.s_bool = True
            order = AS_models.ASVisitRequests.objects.filter(
                Q(AS담당자__first_name__contains=self.search)
                | Q(AS접수__접수번호__contains=self.search)
                | Q(AS접수__현상__contains=self.search)
                | Q(AS접수__불량분류코드__contains=self.search)
                | Q(AS접수__대응유형__contains=self.search)
                | Q(AS접수__의뢰처__거래처명__contains=self.search)
                | Q(AS접수__단품__모델명__contains=self.search)
                | Q(AS접수__단품__모델코드__contains=self.search)
                | Q(AS접수__랙__랙모델명__contains=self.search)
                | Q(AS접수__랙__랙시리얼코드__contains=self.search)
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

    def get_second_queryset(self, request):
        self.search2 = request.GET.get("search2")
        if self.search2 is None:
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
            self.s_bool2 = False
        else:
            self.s_bool2 = True
            order = (
                AS_models.ASVisitContents.objects.filter(재방문여부="재방문")
                .filter(
                    Q(AS방법__contains=self.search2)
                    | Q(고객이름__contains=self.search2)
                    | Q(AS처리내역__contains=self.search2)
                    | Q(특이사항__contains=self.search2)
                    | Q(AS현장방문요청__AS접수__접수번호__contains=self.search2)
                    | Q(AS현장방문요청__AS접수__의뢰처__거래처명__contains=self.search2)
                    | Q(단품__모델명__contains=self.search2)
                    | Q(단품__모델코드__contains=self.search2)
                    | Q(랙__랙모델명__contains=self.search2)
                    | Q(랙__랙시리얼코드__contains=self.search2)
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
