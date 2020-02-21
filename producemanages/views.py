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

        return render(
            request,
            "producemanages/orderdetail.html",
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
            },
        )


def producemanageshome(request):

    user = request.user
    search_m = request.GET.get("search_m")
    search = request.GET.get("search")

    if search_m is None:
        order = OR_models.OrderRegister.objects.all().order_by("-created")
        l_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                l_order.append(s)
            else:
                pass
        s_order = []
        for s in l_order:
            if s.생산요청.생산계획.작성자 == user:
                s_order.append(s)
        s_bool_m = False
    else:
        s_bool_m = True
        order = OR_models.OrderRegister.objects.filter(
            Q(수주코드__contains=search)
            | Q(영업구분=search)
            | Q(제품구분=search)
            | Q(사업장구분=search)
            | Q(고객사명__거래처명__contains=search)
            | Q(단품모델__모델명__contains=search)
            | Q(단품모델__모델코드__contains=search)
            | Q(랙모델__랙모델명__contains=search)
            | Q(랙모델__랙시리얼코드__contains=search)
        ).order_by("-created")
        l_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                l_order.append(s)
            else:
                pass
        s_order = []
        for s in l_order:
            if s.생산요청.생산계획.작성자 == user:
                s_order.append(s)

    if search is None:
        s_bool = False
        order = OR_models.OrderRegister.objects.all().order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)
    else:
        s_bool = True
        order = OR_models.OrderRegister.objects.filter(
            Q(수주코드__contains=search)
            | Q(영업구분=search)
            | Q(제품구분=search)
            | Q(사업장구분=search)
            | Q(고객사명__거래처명__contains=search)
            | Q(단품모델__모델명__contains=search)
            | Q(단품모델__모델코드__contains=search)
            | Q(랙모델__랙모델명__contains=search)
            | Q(랙모델__랙시리얼코드__contains=search)
        ).order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)

    pagediv = 7
    totalpage_m = int(math.ceil(len(s_order) / pagediv))
    paginator_m = Paginator(s_order, pagediv, orphans=3)
    page_m = request.GET.get("page_m", "1")
    s_order = paginator_m.get_page(page_m)
    nextpage_m = int(page_m) + 1
    previouspage_m = int(page_m) - 1
    notsamebool_m = True
    totalpage = int(math.ceil(len(a_order) / pagediv))
    paginator = Paginator(a_order, pagediv, orphans=3)
    page = request.GET.get("page", "1")
    a_order = paginator.get_page(page)
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
    return render(
        request,
        "producemanages/producemanageshome.html",
        {
            "order_m": s_order,
            "search_m": search_m,
            "page_m": page_m,
            "totalpage_m": totalpage_m,
            "notsamebool_m": notsamebool_m,
            "nextpage_m": nextpage_m,
            "previouspage_m": previouspage_m,
            "s_bool_m": s_bool_m,
            "order": a_order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
        },
    )


def produceplanlist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        s_order = []
        order = (
            OR_models.OrderRegister.objects.filter(출하구분="출하미완료")
            .filter(제품구분="단품")
            .order_by("-created")
        )
        for s in order:
            if s.process() == "생산의뢰완료":
                s_order.append(s)
            else:

                pass

        s_bool = False
    else:
        s_bool = True
        order = (
            OR_models.OrderRegister.objects.filter(출하구분="출하미완료")
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
            if s.process() == "생산의뢰완료":
                s_order.append(s)
            else:
                pass

    pagediv = 7

    totalpage = int(math.ceil(len(s_order) / pagediv))
    paginator = Paginator(s_order, pagediv, orphans=3)
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
        "producemanages/produceplanlist.html",
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


def produceplanregister(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청

    form = forms.UploadProducePlanForm(request.POST)

    if form.is_valid():
        생산계획등록코드 = form.cleaned_data.get("생산계획등록코드")
        현재공정 = form.cleaned_data.get("현재공정")
        현재공정달성율 = form.cleaned_data.get("현재공정달성율")
        계획생산량 = form.cleaned_data.get("계획생산량")
        특이사항 = form.cleaned_data.get("특이사항")

        SM = models.ProduceRegister.objects.create(
            작성자=user,
            생산계획등록코드=생산계획등록코드,
            생산의뢰=orderproduce,
            현재공정=현재공정,
            현재공정달성율=현재공정달성율,
            계획생산량=계획생산량,
            일일생산량=0,
            누적생산량=0,
            특이사항=특이사항,
        )
        SM.save()

        messages.success(request, "생산계획 등록이 완료되었습니다.")

        return redirect(reverse("producemanages:producemanageshome"))
    return render(
        request,
        "producemanages/produceplanregister.html",
        {
            "form": form,
            "order": order,
            "orderproduce": orderproduce,
            "긴급도": "긴급도",
            "생산목표수량": "생산목표수량",
            "단품": "단품",
        },
    )


class produceplanupdate(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.ProduceRegister
    template_name = "producemanages/updateproduceplan.html"
    form_class = forms.UpdateProducePlanForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        plan = models.ProduceRegister.objects.get_or_none(pk=pk)
        order = plan.생산의뢰.생산의뢰수주
        context["order"] = order
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        plan = models.ProduceRegister.objects.get_or_none(pk=pk)
        order = plan.생산의뢰.생산의뢰수주
        pk = order.pk
        return reverse("producemanages:orderdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        현재공정 = form.cleaned_data.get("현재공정")
        현재공정달성율 = form.cleaned_data.get("현재공정달성율")
        일일생산량 = form.cleaned_data.get("일일생산량")
        pk = self.kwargs.get("pk")
        plan = models.ProduceRegister.objects.get_or_none(pk=pk)
        plan.현재공정 = 현재공정
        plan.현재공정달성율 = 현재공정달성율
        plan.일일생산량 = 일일생산량
        plan.누적생산량 += 일일생산량

        plan.save()

        return super().form_valid(form)


class produceplantotalupdate(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.ProduceRegister
    template_name = "producemanages/updateproduceplantotal.html"
    form_class = forms.UpdateProducePlanTotalForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        plan = models.ProduceRegister.objects.get_or_none(pk=pk)
        order = plan.생산의뢰.생산의뢰수주
        context["order"] = order
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        plan = models.ProduceRegister.objects.get_or_none(pk=pk)
        order = plan.생산의뢰.생산의뢰수주
        pk = order.pk
        return reverse("producemanages:orderdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        계획생산량 = form.cleaned_data.get("계획생산량")
        특이사항 = form.cleaned_data.get("특이사항")
        현재공정 = form.cleaned_data.get("현재공정")
        현재공정달성율 = form.cleaned_data.get("현재공정달성율")
        pk = self.kwargs.get("pk")
        plan = models.ProduceRegister.objects.get_or_none(pk=pk)
        plan.계획생산량 = 계획생산량
        plan.특이사항 = 특이사항
        plan.현재공정 = 현재공정
        plan.현재공정달성율 = 현재공정달성율
        plan.save()
        messages.success(request, "생산계획 수정이 완료되었습니다.")

        return super().form_valid(form)


def produceplandeleteensure(request, pk):
    plan = models.ProduceRegister.objects.get_or_none(pk=pk)
    order = plan.생산의뢰.생산의뢰수주
    return render(
        request,
        "producemanages/produceplandeleteensure.html",
        {"plan": plan, "order": order},
    )


def produceplandelete(request, pk):
    plan = models.ProduceRegister.objects.get_or_none(pk=pk)
    order = plan.생산의뢰.생산의뢰수주
    pk = order.pk
    plan.delete()
    messages.success(request, "생산계획이 삭제되었습니다.")
    return redirect(reverse("producemanages:orderdetail", kwargs={"pk": pk}))


def workorderlist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        l_order = []
        order = (
            OR_models.OrderRegister.objects.filter(출하구분="출하미완료")
            .filter(제품구분="단품")
            .order_by("-created")
        )

        s_order = []
        for s in order:
            try:
                s.생산요청.생산계획
                try:
                    s.생산요청.생산계획.작업지시서
                except:
                    l_order.append(s)

            except:
                pass
        for s in l_order:
            if s.생산요청.생산계획.작성자 == user:
                s_order.append(s)

        s_bool = False
    else:
        s_bool = True
        order = (
            OR_models.OrderRegister.objects.filter(출하구분="출하미완료")
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

        l_order = []
        s_order = []
        for s in order:
            try:
                s.생산요청.생산계획
                try:
                    s.생산요청.생산계획.작업지시서
                except:
                    l_order.append(s)

            except:
                pass
        for s in l_order:
            if s.생산요청.생산계획.작성자 == user:
                s_order.append(s)

    pagediv = 7

    totalpage = int(math.ceil(len(s_order) / pagediv))
    paginator = Paginator(s_order, pagediv, orphans=3)
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
        "producemanages/workorderlist.html",
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


def workorder(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획

    form = forms.UploadWorkOrderForm(request.POST)

    if form.is_valid():
        작업지시코드 = form.cleaned_data.get("작업지시코드")
        수량 = form.cleaned_data.get("수량")
        특이사항 = form.cleaned_data.get("특이사항")

        SM = models.WorkOrder.objects.create(
            생산계획=produceplan, 수리생산="생산계획", 작업지시코드=작업지시코드, 수량=수량, 특이사항=특이사항,
        )

        messages.success(request, "작업지시서 등록이 완료되었습니다.")

        return redirect(reverse("producemanages:producemanageshome"))
    return render(
        request,
        "producemanages/workorderregister.html",
        {
            "form": form,
            "order": order,
            "produceplan": produceplan,
            "orderproduce": orderproduce,
            "생산목표수량": "생산목표수량",
            "단품": "단품",
        },
    )


class workorderupdate(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.WorkOrder
    template_name = "producemanages/workorderedit.html"
    form_class = forms.EditWorkOrderForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        workorder = models.WorkOrder.objects.get_or_none(pk=pk)
        order = workorder.생산계획.생산의뢰.생산의뢰수주
        context["order"] = order
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        workorder = models.WorkOrder.objects.get_or_none(pk=pk)
        order = workorder.생산계획.생산의뢰.생산의뢰수주
        pk = order.pk
        return reverse("producemanages:orderdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()

        수량 = form.cleaned_data.get("수량")
        특이사항 = form.cleaned_data.get("특이사항")
        pk = self.kwargs.get(self.pk_url_kwarg)
        workorder = models.WorkOrder.objects.get_or_none(pk=pk)
        print(workorder.수량)
        workorder.수량 = 수량
        workorder.특이사항 = 특이사항

        workorder.save()
        print(workorder.수량)

        messages.success(self.request, "작업지시서 등록이 완료되었습니다.")
        return super().form_valid(form)


def workorderdeleteensure(request, pk):
    workorder = models.WorkOrder.objects.get_or_none(pk=pk)
    order = workorder.생산계획.생산의뢰.생산의뢰수주
    return render(
        request,
        "producemanages/workorderdeleteensure.html",
        {"order": order, "workorder": workorder},
    )


def workorderdelete(request, pk):
    workorder = models.WorkOrder.objects.get_or_none(pk=pk)
    order = workorder.생산계획.생산의뢰.생산의뢰수주
    workorder.delete()
    pk = order.pk
    messages.success(request, "작업지시서가 삭제되었습니다.")
    return redirect(reverse("producemanages:orderdetail", kwargs={"pk": pk}))


def producehome(request):

    user = request.user
    search_m = request.GET.get("search_m")
    search = request.GET.get("search")

    if search_m is None:
        order = OR_models.OrderRegister.objects.all().order_by("-created")
        l_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                l_order.append(s)
            else:
                pass
        s_order = []
        for s in l_order:
            if s.생산요청.생산계획.작성자 == user:
                s_order.append(s)
        s_bool_m = False
    else:
        s_bool_m = True
        order = OR_models.OrderRegister.objects.filter(
            Q(수주코드__contains=search)
            | Q(영업구분=search)
            | Q(제품구분=search)
            | Q(사업장구분=search)
            | Q(고객사명__거래처명__contains=search)
            | Q(단품모델__모델명__contains=search)
            | Q(단품모델__모델코드__contains=search)
            | Q(랙모델__랙모델명__contains=search)
            | Q(랙모델__랙시리얼코드__contains=search)
        ).order_by("-created")
        l_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                l_order.append(s)
            else:
                pass
        s_order = []
        for s in l_order:
            if s.생산요청.생산계획.작성자 == user:
                s_order.append(s)

    if search is None:
        s_bool = False
        order = OR_models.OrderRegister.objects.all().order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)
    else:
        s_bool = True
        order = OR_models.OrderRegister.objects.filter(
            Q(수주코드__contains=search)
            | Q(영업구분=search)
            | Q(제품구분=search)
            | Q(사업장구분=search)
            | Q(고객사명__거래처명__contains=search)
            | Q(단품모델__모델명__contains=search)
            | Q(단품모델__모델코드__contains=search)
            | Q(랙모델__랙모델명__contains=search)
            | Q(랙모델__랙시리얼코드__contains=search)
        ).order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)

    pagediv = 7
    totalpage_m = int(math.ceil(len(s_order) / pagediv))
    paginator_m = Paginator(s_order, pagediv, orphans=3)
    page_m = request.GET.get("page_m", "1")
    s_order = paginator_m.get_page(page_m)
    nextpage_m = int(page_m) + 1
    previouspage_m = int(page_m) - 1
    notsamebool_m = True
    totalpage = int(math.ceil(len(a_order) / pagediv))
    paginator = Paginator(a_order, pagediv, orphans=3)
    page = request.GET.get("page", "1")
    a_order = paginator.get_page(page)
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
    return render(
        request,
        "producemanages/producehome.html",
        {
            "order_m": s_order,
            "search_m": search_m,
            "page_m": page_m,
            "totalpage_m": totalpage_m,
            "notsamebool_m": notsamebool_m,
            "nextpage_m": nextpage_m,
            "previouspage_m": previouspage_m,
            "s_bool_m": s_bool_m,
            "order": a_order,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
        },
    )
