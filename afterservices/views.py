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


class afterserviceshome(View, user_mixins.LoggedInOnlyView):
    """two queryset list with pagenate1, pagenate2"""

    templatename = "afterservices/afterserviceshome.html"

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
                except:
                    queryset.append(s)
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
                except:
                    queryset.append(s)
        return queryset

    def get_page(self):
        self.queryset = self.get_first_queryset(self.request)
        self.pagediv = 7
        self.totalpage = int(math.ceil(len(self.queryset) / self.pagediv))
        self.paginator = Paginator(self.queryset, self.pagediv, orphans=0)
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
        self.paginator2 = Paginator(self.queryset2, self.pagediv2, orphans=0)
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

    def get(self, request):
        self.get_page()
        self.get_page2()
        return render(
            request,
            self.templatename,
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
            },
        )


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
    templatename = "afterservices/ASvisitrequestsalllist.html"

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
    assuccess.delete()
    messages.success(request, "AS완료가 철회되었습니다.")
    return redirect(
        reverse("afterservices:ASrequestdetail", kwargs={"pk": assuccess.내부처리.pk,})
    )

