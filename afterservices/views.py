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
