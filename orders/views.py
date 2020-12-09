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
from random import randint
from django.utils import timezone


@login_required
def orderregister(request):
    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "OR" + num
            obj = models.OrderRegister.objects.get_or_none(수주코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.UploadOrderForm(request.POST)
    code = give_number()
    now = timezone.now().date()
    form.initial = {"수주코드": code, "수주일자": now}

    search = request.GET.get("search")
    if search is None:
        customer = SI_models.Partner.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = SI_models.Partner.objects.filter(
            Q(작성자__first_name=search)
            | Q(거래처구분=search)
            | Q(거래처코드=search)
            | Q(거래처명__contains=search)
            | Q(담당자__first_name=search)
            | Q(사업장주소__contains=search)
        ).order_by("-created")
        customer = qs

    if form.is_valid():
        수주코드 = form.cleaned_data.get("수주코드")
        영업구분 = form.cleaned_data.get("영업구분")
        사업장구분 = form.cleaned_data.get("사업장구분")
        수주일자 = form.cleaned_data.get("수주일자")
        거래처코드 = form.cleaned_data.get("거래처코드")
        현장명 = form.cleaned_data.get("현장명")
        납품요청일 = form.cleaned_data.get("납품요청일")
        특이사항 = form.cleaned_data.get("특이사항")
        제품구분 = form.cleaned_data.get("제품구분")

        SM = models.OrderRegister.objects.create(
            작성자=request.user,
            수주코드=수주코드,
            영업구분=영업구분,
            사업장구분=사업장구분,
            수주일자=수주일자,
            고객사명=거래처코드,
            현장명=현장명,
            납품요청일=납품요청일,
            특이사항=특이사항,
            제품구분=제품구분,
            납품수량=0,
        )

        pk = SM.pk
        if SM.제품구분 == "단품":
            return redirect(reverse("orders:ordersingle", kwargs={"pk": pk}))
        else:
            return redirect(reverse("orders:orderrack", kwargs={"pk": pk}))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = ["제품구분", "영업구분", "사업장구분"]
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "orders/orderregister.html",
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


@login_required
def ordersingle(request, pk):
    form = forms.OrderSingleForm(request.POST)

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
        납품수량 = form.cleaned_data.get("납품수량")
        SM = models.OrderRegister.objects.get(pk=pk)
        SM.단품모델 = 단품모델코드
        SM.납품수량 = 납품수량
        SM.save()

        messages.success(request, "단품수주가 등록되었습니다.")

        return redirect(reverse("orders:ordershome"))

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
        "orders/ordersingle.html",
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


@login_required
def orderrack(request, pk):
    form = forms.OrderRackForm(request.POST)

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
        납품수량 = form.cleaned_data.get("납품수량")
        SM = models.OrderRegister.objects.get(pk=pk)
        SM.랙모델 = 랙시리얼코드
        SM.납품수량 = 납품수량
        SM.save()

        messages.success(request, "랙수주가 등록되었습니다.")

        return redirect(reverse("orders:ordershome"))

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
        "orders/orderrack.html",
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


@login_required
def ordershome(request):
    if request.user.__str__() == "AnonymousUser":
        return redirect(reverse("users:login"))

    user = request.user
    search_m = request.GET.get("search_m")
    search = request.GET.get("search")

    order_m = (
        models.OrderRegister.objects.filter(작성자=user)
        .filter(출하구분="출하미완료")
        .order_by("-created")
    )
    if search_m is None:
        s_bool_m = False
        my_order_count = order_m.count()
    else:
        s_bool_m = True
        qs_m = models.OrderRegister.objects.filter(작성자=user).filter(출하구분="출하미완료")
        qs = qs_m.filter(
            Q(수주코드__contains=search_m)
            | Q(영업구분=search_m)
            | Q(제품구분=search_m)
            | Q(사업장구분=search_m)
            | Q(고객사명__거래처명__contains=search_m)
            | Q(단품모델__모델명=search_m)
            | Q(랙모델__랙모델명=search_m)
        ).order_by("-created")
        my_order_count = order_m.count()
        order_m = qs

    order = models.OrderRegister.objects.all().order_by("-created")
    if search is None:
        order_count = order.count()
        s_bool = False
    else:
        s_bool = True
        qs = models.OrderRegister.objects.filter(
            Q(수주코드__contains=search)
            | Q(영업구분=search)
            | Q(작성자__first_name=search)
            | Q(제품구분=search)
            | Q(사업장구분=search)
            | Q(고객사명__거래처명__contains=search)
            | Q(단품모델__모델명=search)
            | Q(랙모델__랙모델명=search)
        ).order_by("-created")
        order_count = order.count()
        order = qs

    pagediv = 7
    totalpage_m = int(math.ceil(len(order_m) / pagediv))
    paginator_m = Paginator(order_m, pagediv, orphans=0)
    page_m = request.GET.get("page_m", "1")
    order_m = paginator_m.get_page(page_m)
    nextpage_m = int(page_m) + 1
    previouspage_m = int(page_m) - 1
    notsamebool_m = True
    totalpage = int(math.ceil(len(order) / pagediv))
    paginator = Paginator(order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    order = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True

    if int(page_m) == totalpage_m:
        notsamebool_m = False
    if (search_m is None) or (search_m == ""):
        search_m = "search"

    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    now = timezone.now().date()
    return render(
        request,
        "orders/ordershome.html",
        {
            "order_count": order_count,
            "my_order_count": my_order_count,
            "order_m": order_m,
            "search_m": search_m,
            "page_m": page_m,
            "totalpage_m": totalpage_m,
            "notsamebool_m": notsamebool_m,
            "nextpage_m": nextpage_m,
            "previouspage_m": previouspage_m,
            "s_bool_m": s_bool_m,
            "order": order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "now": now,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
        },
    )


class OrderDetail(user_mixins.LoggedInOnlyView, DetailView):
    templatename = "orders/orderdetail.html"
    model = models.OrderRegister

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        order = models.OrderRegister.objects.get(pk=pk)
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

        ordersingleback = order.단품입고요청.all()
        pkbacklist = []
        for orderib in ordersingleback:
            pkbacklist.append(orderib.pk)
        ordersingleback = []
        for pki in pkbacklist:
            SSB = SS_models.StockOfSingleProductInRequest.objects.get_or_none(pk=pki)
            ordersingleback.append(SSB)

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
            self.templatename,
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
                "ordersingleback": ordersingleback,
                "workboolean": workboolean,
                "workdoneboolean": workdoneboolean,
                "orderfinalboolean": orderfinalboolean,
                "repairboolean": repairboolean,
            },
        )


@login_required
def orderedit(request, pk):
    입찰 = False
    대리점 = False
    AS = False
    내부계획 = False
    단품 = False
    랙 = False
    삼형전자 = False
    엠에스텔레콤 = False

    form = forms.EditOrderForm(request.POST)

    search = request.GET.get("search")
    SM = models.OrderRegister.objects.get(pk=pk)
    i수주코드 = SM.수주코드
    i영업구분 = SM.영업구분
    i사업장구분 = SM.사업장구분
    i제품구분 = SM.제품구분
    i수주일자 = SM.수주일자
    i거래처코드 = SM.고객사명.거래처코드
    i현장명 = SM.현장명
    i납품요청일 = SM.납품요청일
    i특이사항 = SM.특이사항
    if i영업구분 == "입찰":
        입찰 = True
    elif i영업구분 == "대리점":
        대리점 = True
    elif i영업구분 == "AS":
        AS = True
    else:
        내부계획 = True
    if i제품구분 == "단품":
        단품 = True
    else:
        랙 = True

    if i사업장구분 == "삼형전자":
        삼형전자 = True
    else:
        엠에스텔레콤 = True

    if i납품요청일 is None:
        i납품요청일 = ""

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
        영업구분 = form.cleaned_data.get("영업구분")
        사업장구분 = form.cleaned_data.get("사업장구분")
        수주일자 = form.cleaned_data.get("수주일자")
        거래처코드 = form.cleaned_data.get("거래처코드")
        거래처코드 = SI_models.CustomerPartner.objects.get_or_none(거래처코드=거래처코드)
        현장명 = form.cleaned_data.get("현장명", " ")
        납품요청일 = form.cleaned_data.get("납품요청일")
        특이사항 = form.cleaned_data.get("특이사항")
        제품구분 = form.cleaned_data.get("제품구분")
        if 제품구분 == "단품":
            SM.랙모델 = None
        else:
            SM.단품모델 = None

        SM.작성자 = request.user
        SM.영업구분 = 영업구분
        SM.사업장구분 = 사업장구분

        SM.수주일자 = 수주일자
        SM.고객사명 = 거래처코드
        SM.현장명 = 현장명
        SM.납품요청일 = 납품요청일
        SM.특이사항 = 특이사항
        SM.제품구분 = 제품구분
        SM.save()

        if SM.제품구분 == "단품":
            return redirect(reverse("orders:ordersingleedit", kwargs={"pk": pk}))
        else:
            return redirect(reverse("orders:orderrackedit", kwargs={"pk": pk}))

    pagediv = 10
    totalpage = int(math.ceil(len(customer) / pagediv))
    paginator = Paginator(customer, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    customer = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    seletelist = ["제품구분", "영업구분", "사업장구분"]
    if int(page) == totalpage:
        notsamebool = False
    if (search is None) or (search == ""):
        search = "search"
    return render(
        request,
        "orders/orderedit.html",
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
            "i수주코드": i수주코드,
            "i수주일자": i수주일자,
            "i거래처코드": i거래처코드,
            "i현장명": i현장명,
            "i납품요청일": i납품요청일,
            "i특이사항": i특이사항,
            "입찰": 입찰,
            "대리점": 대리점,
            "AS": AS,
            "내부계획": 내부계획,
            "단품": 단품,
            "랙": 랙,
            "삼형전자": 삼형전자,
            "엠에스텔레콤": 엠에스텔레콤,
        },
    )


@login_required
def ordersingleedit(request, pk):
    form = forms.OrderSingleForm(request.POST)
    SM = models.OrderRegister.objects.get(pk=pk)

    search = request.GET.get("search")
    if SM.단품모델 is not None:
        단품모델 = SM.단품모델.모델코드
    else:
        단품모델 = ""
    납품수량 = SM.납품수량
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
        납품수량 = form.cleaned_data.get("납품수량")
        SM.단품모델 = 단품모델코드
        SM.납품수량 = 납품수량
        SM.save()
        messages.success(request, "단품수주가 수정되었습니다.")
        return redirect(reverse("orders:ordershome"))
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
        "orders/ordersingleedit.html",
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
            "단품모델": 단품모델,
            "납품수량": 납품수량,
        },
    )


@login_required
def orderrackedit(request, pk):
    form = forms.OrderRackForm(request.POST)

    SM = models.OrderRegister.objects.get(pk=pk)
    if SM.랙모델 is not None:
        랙모델 = SM.랙모델.랙시리얼코드
    else:
        랙모델 = ""
    납품수량 = SM.납품수량

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
        납품수량 = form.cleaned_data.get("납품수량")
        SM.랙모델 = 랙시리얼코드
        SM.납품수량 = 납품수량
        SM.save()

        messages.success(request, "랙수주가 수정되었습니다.")

        return redirect(reverse("orders:ordershome"))

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
        "orders/orderrackedit.html",
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
            "랙모델": 랙모델,
            "납품수량": 납품수량,
        },
    )


@login_required
def orderdeleteensure(request, pk):

    order = models.OrderRegister.objects.get_or_none(pk=pk)
    return render(request, "orders/orderdeleteensure.html", {"order": order},)


@login_required
def orderdelete(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    order.delete()

    messages.success(request, "해당 수주가 삭제되었습니다.")

    return redirect(reverse("orders:ordershome"))


@login_required
def orderproduce(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        s_order = []
        order = (
            models.OrderRegister.objects.filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(제품구분="단품")
            .order_by("-created")
        )
        for s in order:
            if s.process() == "수주등록완료":
                s_order.append(s)
            else:
                pass

        s_bool = False
    else:
        s_bool = True
        order = (
            models.OrderRegister.objects.filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(제품구분="단품")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분=search)
                | Q(제품구분=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__랙모델명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )
        s_order = []
        for s in order:
            if s.process() == "수주등록완료":
                s_order.append(s)
            else:
                pass

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
        "orders/orderproduce.html",
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


@login_required
def orderproduceregister(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "OP" + num
            obj = models.OrderProduce.objects.get_or_none(생산의뢰코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.UploadOrderProduceForm(request.POST)
    code = give_number()
    now = timezone.now().date()
    form.initial = {"생산의뢰코드": code, "생산목표수량": order.납품수량}

    if form.is_valid():
        생산의뢰코드 = form.cleaned_data.get("생산의뢰코드")
        긴급도 = form.cleaned_data.get("긴급도")
        생산목표수량 = form.cleaned_data.get("생산목표수량")
        SM = models.OrderProduce.objects.create(
            생산의뢰수주=order, 생산의뢰코드=생산의뢰코드, 긴급도=긴급도, 생산목표수량=생산목표수량,
        )
        SM.save()

        messages.success(request, "생산의뢰 등록이 완료되었습니다.")

        return redirect(reverse("orders:ordershome"))
    return render(
        request,
        "orders/orderproduceregister.html",
        {"form": form, "order": order, "긴급도": "긴급도", "생산목표수량": "생산목표수량", "단품": "단품"},
    )


@login_required
def orderproduceedit(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    produce = order.생산요청
    form = forms.EditOrderProduceForm(request.POST)
    일반 = False
    긴급 = False
    생산의뢰코드 = produce.생산의뢰코드
    생산목표수량 = produce.생산목표수량
    if produce.긴급도 == "일반":
        일반 = True
    elif produce.긴급도 == "긴급":
        긴급 = True
    else:
        pass

    if form.is_valid():
        긴급도 = form.cleaned_data.get("긴급도")
        생산목표수량 = form.cleaned_data.get("생산목표수량")
        produce.긴급도 = 긴급도
        produce.생산목표수량 = 생산목표수량
        produce.save()

        messages.success(request, "생산의뢰가 수정되었습니다.")

        return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))
    return render(
        request,
        "orders/orderproduceedit.html",
        {
            "form": form,
            "order": order,
            "긴급도": "긴급도",
            "생산목표수량": "생산목표수량",
            "단품": "단품",
            "일반": 일반,
            "긴급": 긴급,
            "생산의뢰코드": 생산의뢰코드,
            "생산목표수량": 생산목표수량,
        },
    )


@login_required
def orderproducedeleteensure(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)

    orderproduce = order.생산요청
    return render(
        request, "orders/orderproducedeleteensure.html", {"orderproduce": orderproduce},
    )


@login_required
def orderproducedelete(request, pk):
    orderproduce = models.OrderProduce.objects.get_or_none(pk=pk)
    pk = orderproduce.생산의뢰수주.pk
    orderproduce.delete()

    messages.success(request, "해당 생산의뢰가 삭제되었습니다.")

    return redirect(reverse("orders:orderdetail", kwargs={"pk": pk}))


@login_required
def endorder(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        order = (
            models.OrderRegister.objects.filter(작성자=user)
            .filter(출하구분="출하미완료")
            .order_by("-created")
        )

        s_bool = False
    else:
        s_bool = True
        order = (
            models.OrderRegister.objects.filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분=search)
                | Q(제품구분=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__랙모델명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

    pagediv = 7

    totalpage = int(math.ceil(len(order) / pagediv))
    paginator = Paginator(order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    order = paginator.get_page(page)
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
        "orders/endorder.html",
        {
            "order": order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "nonpage": nonpage,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
        },
    )


@login_required
def endorderforout(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    order.출하구분 = "출하완료"
    order.save()
    messages.success(request, "해당 수주는 출하완료 처리되었습니다.")
    return redirect(reverse("orders:endorder"))


@login_required
def endorderforoutforstock(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    order.출하구분 = "출하완료"
    order.save()
    messages.success(request, "해당 수주는 출하완료 처리되었습니다.")
    return redirect(reverse("stocksingle:ordersingleout"))


@login_required
def endorderlist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        order = models.OrderRegister.objects.filter(출하구분="출하완료").order_by("-created")

        s_bool = False
    else:
        s_bool = True
        order = (
            models.OrderRegister.objects.filter(출하구분="출하완료")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분=search)
                | Q(제품구분=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__랙모델명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

    pagediv = 7

    totalpage = int(math.ceil(len(order) / pagediv))
    paginator = Paginator(order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    order = paginator.get_page(page)
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
        "orders/endorderlist.html",
        {
            "order": order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "nonpage": nonpage,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
            "user": user,
        },
    )


@login_required
def endorderforin(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    order.출하구분 = "출하미완료"
    order.save()
    messages.success(request, "해당 수주의 출하완료가 철회되었습니다.")
    return redirect(reverse("orders:endorderlist"))


@login_required
def orderproduceforrack(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        s_order = []
        order = (
            models.OrderRegister.objects.filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(제품구분="랙")
            .order_by("-created")
        )
        for s in order:
            if s.process() == "수주등록완료":
                s_order.append(s)
            else:
                pass

        s_bool = False
    else:
        s_bool = True
        order = (
            models.OrderRegister.objects.filter(작성자=user)
            .filter(출하구분="출하미완료")
            .filter(제품구분="랙")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분=search)
                | Q(제품구분=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__랙모델명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )
        s_order = []
        for s in order:
            if s.process() == "수주등록완료":
                s_order.append(s)
            else:
                pass

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
        "orders/orderproduceforrack.html",
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


@login_required
def informationforrackproduce(request, pk):
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    rack = order.랙모델
    single = rack.랙구성단품.filter(랙구성="단품")
    ordersinglelist = order.단품생산의뢰.all()
    boollist = []
    for os in ordersinglelist:
        for ss in single:
            if os.단품모델 == ss.랙구성단품:
                boollist.append(ss.랙구성단품)

    user = request.user
    return render(
        request,
        "orders/informationforrackproduce.html",
        {
            "order": order,
            "rack": rack,
            "user": user,
            "single": single,
            "boollist": boollist,
        },
    )


@login_required
def producesingleforrack(request, pk, spk):
    form = forms.UploadOrderProduceForm(request.POST)
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    rack = order.랙모델
    racksingle = rack.랙구성단품.filter(랙구성="단품")
    single = SI_models.SingleProduct.objects.get_or_none(pk=spk)
    user = request.user

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "OP" + num
            obj = models.OrderProduce.objects.get_or_none(생산의뢰코드=code)
            if obj:
                pass
            else:
                return code

    code = give_number()
    for singletest in racksingle:
        if singletest.랙구성단품 == single:
            matenum = singletest.수량
    result = order.납품수량 * matenum
    recommend = result - single.단품재고.출하요청제외수량
    if recommend < 0:
        recommend = 0

    form.initial = {"생산의뢰코드": code, "생산목표수량": recommend}

    if form.is_valid():

        def give_new_number():
            while True:
                n = randint(1, 99)
                num = str(n).zfill(2)
                code = order.수주코드 + "-" + num
                obj = models.OrderRegister.objects.get_or_none(수주코드=code)
                if obj:
                    pass
                else:
                    return code

        single_order = models.OrderRegister.objects.create(
            랙생산의뢰=order,
            작성자=request.user,
            수주코드=give_new_number(),
            영업구분="내부계획",
            사업장구분=order.사업장구분,
            수주일자=order.수주일자,
            고객사명=order.고객사명,
            현장명=order.현장명,
            납품요청일=order.납품요청일,
            특이사항=f"수주코드({order.수주코드})의 생산의뢰로 인한 내부계획생산",
            제품구분="단품",
            단품모델=single,
            납품수량=0,
            출하구분="출하미완료",
        )
        생산의뢰코드 = form.cleaned_data.get("생산의뢰코드")
        긴급도 = form.cleaned_data.get("긴급도")
        생산목표수량 = form.cleaned_data.get("생산목표수량")
        SM = models.OrderProduce.objects.create(
            생산의뢰수주=single_order, 생산의뢰코드=생산의뢰코드, 긴급도=긴급도, 생산목표수량=생산목표수량,
        )
        single_order.납품수량 = 생산목표수량
        single_order.save()

        return HttpResponse(
            '<script type="text/javascript">opener.location.reload(); window.close()</script>'
        )
    return render(
        request,
        "orders/producesingleforrack.html",
        {"order": order, "user": user, "single": single, "form": form,},
    )


@login_required
def blueprintdownload(request, pk):
    """파일 다운로드 유니코드화 패치"""
    order = models.OrderRegister.objects.get_or_none(pk=pk)
    filepath = order.랙조립도면.path
    title = order.랙조립도면.__str__()
    title = urllib.parse.quote(title.encode("utf-8"))
    title = title.replace("blueprint/", "")

    with open(filepath, "rb") as f:
        response = HttpResponse(f, content_type="application/force-download")
        titling = 'attachment; filename="{}"'.format(title)
        response["Content-Disposition"] = titling
        return response
