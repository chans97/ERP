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


def firstindecide(request):
    user = request.user
    if user.is_authenticated:

        if user.nowPart.pk == 61:
            return redirect(reverse("orders:ordershome"))
        elif user.nowPart.pk == 62:
            return redirect(reverse("producemanages:producemanageshome"))
        elif user.nowPart.pk == 63:
            return redirect(reverse("producemanages:producehome"))
        elif user.nowPart.pk == 64:
            return redirect(reverse("qualitycontrols:qualitycontrolshome"))
        elif (user.nowPart.pk == 65) or (user.nowPart.pk == 66):
            return redirect(reverse("afterservices:afterserviceshome"))
        elif user.nowPart.pk == 67:
            return redirect(reverse("stockmanages:stockmanageshome"))
        else:
            return render(request, "base.html")

    else:
        return redirect(reverse("users:login"))


def parthome(request, pk):

    """선택 부서를 nowPart로 바꿔서 저장"""

    userlist = user_models.User.objects.all()
    part = user_models.Part.objects.get_or_none(pk=pk)
    request.user.nowPart = part
    request.user.save()
    return redirect(reverse("core:home"))

    """
def 첫번째 부서를 nowPart로 지정하는 함수(request):
    for user in userlist:
        if list(user.부서.all()):
            part = user.부서.all()[0]
            user.nowPart = part
            user.save()

    return redirect(reverse("core:home"))"""


class onelist(View, user_mixins.LoggedInOnlyView):
    """one queryset list with pagenate"""

    templatename = "qualitycontrols/materialchecklist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            materialchecklist = QC_models.MaterialCheckRegister.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in materialchecklist:
                try:
                    s.수입검사
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            materialchecklist = QC_models.MaterialCheckRegister.objects.filter(
                Q(수입검사의뢰코드__contains=self.search)
                | Q(의뢰자__first_name__contains=self.search)
                | Q(자재__자재코드__contains=self.search)
                | Q(자재__자재품명__contains=self.search)
                | Q(created__contains=self.search)
                | Q(created__month__contains=self.search)
                | Q(created__day__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in materialchecklist:
                try:
                    s.수입검사
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

    def get(self, request):
        if self.request.user.__str__() == "AnonymousUser":
            return redirect(reverse("users:login"))

        self.get_page()
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
            },
        )


class twolist(View, user_mixins.LoggedInOnlyView):
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
        if self.request.user.__str__() == "AnonymousUser":
            return redirect(reverse("users:login"))
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


class threelist(View, user_mixins.LoggedInOnlyView):
    """three queryset list with pagenate1, pagenate2, pagenate3"""

    templatename = "qualitycontrols/qualitycontrolshome.html"

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
            order = AS_models.ASRepairRequest.objects.all().order_by("-created")
            queryset = []
            for s in order:
                try:
                    s.수리내역서
                except:
                    queryset.append(s)

            self.s_bool3 = False
        else:
            self.s_bool3 = True
            order = AS_models.ASRepairRequest.objects.filter(
                Q(신청자__contains=search)
                | Q(신청품목__모델명__contains=search)
                | Q(신청품목__모델코드__contains=search)
                | Q(수리요청코드__contains=search)
            ).order_by("-created")

            queryset = []
            for s in order:
                try:
                    s.수리내역서
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

    def get_page3(self):
        self.queryset3 = self.get_third_queryset(self.request)
        self.pagediv3 = 7
        self.totalpage3 = int(math.ceil(len(self.queryset3) / self.pagediv3))
        self.paginator3 = Paginator(self.queryset3, self.pagediv3, orphans=0)
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
        if self.request.user.__str__() == "AnonymousUser":
            return redirect(reverse("users:login"))
        self.get_page()
        self.get_page2()
        self.get_page3()
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


def migrate(request):
    return render(request, "migrate/migrate.html")


def partnermigrate(request):
    form = forms.partnermigrate(request.POST)
    if form.is_valid():
        try:
            Excelfile = request.FILES["Excelfile"]
        except:
            Excelfile = None
        print(Excelfile)

        result = open(Excelfile, "w")

        while True:
            line = result.readline()
            print(line)

            if not line:
                break
        result.close()

        messages.success(request, "거래처가 등록되었습니다.")
        return redirect(reverse("StandardInformation:partner"))

    else:
        try:
            Excelfile = request.FILES["Excelfile"]
        except:
            return render(request, "migrate/partnermigrate.html", {"form": form})

        single = models.partnermigrate.objects.create()
        single.Excelfile = Excelfile
        single.save()
        result = open(single.Excelfile.path, "rt", encoding="UTF8")
        messages.success(request, "엑셀파일을 읽는 중 입니다.")

        num = 0
        while True:

            num += 1
            line = result.readline()
            if not line:
                break
            aline = line.split(",")
            if aline[0] == "구매처":
                거래처구분 = "고객"
            else:
                거래처구분 = aline[0]
            print(num)
            if num != 1:
                SI_models.Partner.objects.create(
                    작성자=request.user,
                    작성일=timezone.now(),
                    거래처구분=거래처구분,
                    거래처코드=aline[1],
                    거래처명=aline[2],
                    사업자등록번호=aline[3],
                    담당자=request.user,
                    거래처담당자=aline[4],
                    연락처=aline[5],
                    이메일=aline[6],
                    사업장주소=aline[7],
                    특이사항="",
                    사용여부=True,
                )
                print(num, ":", aline)

        result.close()
        messages.success(request, "완료되었습니다.")
        return redirect(reverse("StandardInformation:partner"))

    return render(request, "migrate/partnermigrate.html", {"form": form})


def materialmigrate(request):
    form = forms.partnermigrate(request.POST)
    if form.is_valid():
        try:
            Excelfile = request.FILES["Excelfile"]
        except:
            Excelfile = None
        print(Excelfile)

        result = open(Excelfile, "w")

        while True:
            line = result.readline()
            print(line)

            if not line:
                break
        result.close()

        messages.success(request, "거래처가 등록되었습니다.")
        return redirect(reverse("StandardInformation:partner"))
    else:
        try:
            Excelfile = request.FILES["Excelfile"]
        except:
            return render(request, "migrate/materialmigrate.html", {"form": form})
        single = models.partnermigrate.objects.create()
        single.Excelfile = Excelfile
        single.save()
        result = open(single.Excelfile.path, "rt", encoding="UTF8")
        messages.success(request, "엑셀파일을 읽는 중 입니다.")
        num = 0
        while True:
            num += 1
            line = result.readline()
            if not line:
                break
            aline = line.split(",")
            name = aline[4]
            자재공급업체 = SI_models.SupplyPartner.objects.get_or_none(거래처명=name)
            if 자재공급업체:
                if num != 1:
                    SI_models.Material.objects.create(
                        작성자=request.user,
                        자재코드=aline[0],
                        자재품명=aline[1],
                        규격=aline[2],
                        단위=aline[3],
                        자재공급업체=자재공급업체,
                    )
            else:
                messages.error(request, f"{name}(은)는 등록되지 않은 업체입니다.")

        result.close()
        messages.success(request, "완료되었습니다.")
        return redirect(reverse("stockmanages:materialStandarInformation"))
    return render(request, "migrate/materialmigrate.html", {"form": form})


def measuremigrate(request):
    form = forms.partnermigrate(request.POST)
    if form.is_valid():
        try:
            Excelfile = request.FILES["Excelfile"]
        except:
            Excelfile = None
        result = open(Excelfile, "w")
        while True:
            line = result.readline()
            if not line:
                break
        result.close()
        messages.success(request, "완료되었습니다.")
        return redirect(reverse("StandardInformation:partner"))
    else:
        try:
            Excelfile = request.FILES["Excelfile"]
        except:
            return render(request, "migrate/measuremigrate.html", {"form": form})
        single = models.partnermigrate.objects.create()
        single.Excelfile = Excelfile
        single.save()
        result = open(single.Excelfile.path, "rt", encoding="UTF8")
        messages.success(request, "엑셀파일을 읽는 중 입니다.")
        num = 0
        while True:
            num += 1
            line = result.readline()
            if not line:
                break
            aline = line.split(",")

            if num != 1:
                date = aline[3]
                datestr = str(date)
                datelist = datestr.split(".")
                print(num, datelist)
                설치년월일 = datelist[0] + "-" + datelist[1] + "-" + "01"

                SM = SI_models.Measure.objects.create(
                    계측기코드=aline[4],
                    계측기명=aline[1],
                    자산관리번호=aline[2],
                    설치년월일=설치년월일,
                    설치장소=aline[6],
                    작성자=request.user,
                )
            print(num, "done")
        result.close()
        messages.success(request, "완료되었습니다.")
        return redirect(reverse("qualitycontrols:measurelist"))

    return render(request, "migrate/measuremigrate.html", {"form": form})
