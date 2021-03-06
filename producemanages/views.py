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
from random import randint
from stockrack import models as SR_models
from orders import views as OR_views
from core import views as core_views


class OrderDetail(OR_views.OrderDetail):
    model = OR_models.OrderRegister
    templatename = "producemanages/orderdetail.html"


class OrderDetailForWork(OrderDetail):
    model = OR_models.OrderRegister
    templatename = "producemanages/orderdetailforwork.html"


@login_required(login_url="/")
def producemanageshome(request):

    if request.user.__str__() == "AnonymousUser":
        return redirect(reverse("users:login"))

    user = request.user
    search = request.GET.get("search")
    search_m = request.GET.get("search_m")

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
            | Q(영업구분=search_m)
            | Q(제품구분=search_m)
            | Q(사업장구분=search_m)
            | Q(고객사명__거래처명__contains=search_m)
            | Q(단품모델__모델명__contains=search_m)
            | Q(단품모델__모델코드__contains=search_m)
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
        ).order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)

    pagediv = 7
    totalpage_m = int(math.ceil(len(s_order) / pagediv))
    paginator_m = Paginator(s_order, pagediv, orphans=0)
    page_m = request.GET.get("page_m", "1")
    s_order = paginator_m.get_page(page_m)
    nextpage_m = int(page_m) + 1
    previouspage_m = int(page_m) - 1
    notsamebool_m = True
    totalpage = int(math.ceil(len(a_order) / pagediv))
    paginator = Paginator(a_order, pagediv, orphans=0)
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


@login_required(login_url="/")
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
                | Q(영업구분__contains=search)
                | Q(제품구분__contains=search)
                | Q(사업장구분__contains=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(생산요청__긴급도__contains=search)
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


@login_required(login_url="/")
def produceplanregister(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "PP" + num
            obj = models.ProduceRegister.objects.get_or_none(생산계획등록코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.UploadProducePlanForm(request.POST)
    code = give_number()
    form.initial = {
        "생산계획등록코드": code,
    }

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

        WO = models.WorkOrder.objects.create(
            생산계획=SM, 수리생산="생산계획", 작업지시코드=생산계획등록코드, 수량=계획생산량, 특이사항=f"{생산계획등록코드}의 작업지시서",
        )

        messages.success(request, "생산계획 등록이 완료되었습니다.")

        return redirect(reverse("producemanages:producemanageshome"))
    selectlist = ["현재공정", "현재공정달성율"]
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
            "selectlist": selectlist,
        },
    )


class produceplanupdate(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.ProduceRegister
    template_name = "producemanages/updateproduceplan.html"
    form_class = forms.UpdateProducePlanForm
    initial = {
        "일일생산량": 0,
    }

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
            **response_kwargs,
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
            **response_kwargs,
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
        workorder = plan.작업지시서
        workorder.수량 = 계획생산량
        workorder.특이사항 = 특이사항
        workorder.save()

        messages.success(self.request, "생산계획 수정이 완료되었습니다.")

        return super().form_valid(form)


@login_required(login_url="/")
def produceplandeleteensure(request, pk):
    plan = models.ProduceRegister.objects.get_or_none(pk=pk)
    order = plan.생산의뢰.생산의뢰수주
    return render(
        request,
        "producemanages/produceplandeleteensure.html",
        {"plan": plan, "order": order},
    )


@login_required(login_url="/")
def produceplandelete(request, pk):
    plan = models.ProduceRegister.objects.get_or_none(pk=pk)
    order = plan.생산의뢰.생산의뢰수주
    pk = order.pk
    workorder = plan.작업지시서
    plan.delete()
    workorder.delete()
    messages.success(request, "생산계획이 삭제되었습니다.")
    return redirect(reverse("producemanages:orderdetail", kwargs={"pk": pk}))


@login_required(login_url="/")
def rackmakelist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        s_order = SR_models.StockOfRackProductMaker.objects.filter(랙조립기사=user).order_by(
            "-created"
        )

        s_bool = False
    else:
        s_bool = True
        s_order = (
            SR_models.StockOfRackProductMaker.objects.filter(랙조립기사=user)
            .filter(
                Q(랙출하요청__수주__수주코드__contains=search)
                | Q(현재공정__contains=search)
                | Q(랙조립기사__first_name__contains=search)
                | Q(특이사항__contains=search)
                | Q(랙__현장명__contains=search)
                | Q(랙__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

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
        "producemanages/rackmakelist.html",
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


@login_required(login_url="/")
def rackmakedonelist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        s_order = (
            SR_models.StockOfRackProductMaker.objects.filter(랙조립기사=user)
            .filter(현재공정="완료")
            .order_by("-created")
        )

        s_bool = False
    else:
        s_bool = True
        s_order = (
            SR_models.StockOfRackProductMaker.objects.filter(랙조립기사=user)
            .filter(현재공정="완료")
            .filter(
                Q(랙출하요청__수주__수주코드__contains=search)
                | Q(랙조립기사__first_name__contains=search)
                | Q(특이사항__contains=search)
                | Q(랙__현장명__contains=search)
                | Q(랙__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

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
        "producemanages/rackmakedonelist.html",
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


@login_required(login_url="/")
def workorder(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획

    def give_number():
        while True:
            n = randint(1, 999999)
            num = str(n).zfill(6)
            code = "WO" + num
            obj = models.WorkOrder.objects.get_or_none(작업지시코드=code)
            if obj:
                pass
            else:
                return code

    form = forms.UploadWorkOrderForm(request.POST)
    code = give_number()
    form.initial = {
        "작업지시코드": code,
    }

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
            **response_kwargs,
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

        messages.success(self.request, "작업지시서 수정이 완료되었습니다.")
        return super().form_valid(form)


@login_required(login_url="/")
def workorderdeleteensure(request, pk):
    workorder = models.WorkOrder.objects.get_or_none(pk=pk)
    order = workorder.생산계획.생산의뢰.생산의뢰수주
    return render(
        request,
        "producemanages/workorderdeleteensure.html",
        {"order": order, "workorder": workorder},
    )


@login_required(login_url="/")
def workorderdelete(request, pk):
    workorder = models.WorkOrder.objects.get_or_none(pk=pk)
    order = workorder.생산계획.생산의뢰.생산의뢰수주
    workorder.delete()
    pk = order.pk
    messages.success(request, "작업지시서가 삭제되었습니다.")
    return redirect(reverse("producemanages:orderdetail", kwargs={"pk": pk}))


@login_required(login_url="/")
def producehome(request):
    if request.user.__str__() == "AnonymousUser":
        return redirect(reverse("users:login"))

    user = request.user
    search = request.GET.get("search")
    search_m = request.GET.get("search_m")

    if search is None:
        l_order = []
        order = OR_models.OrderRegister.objects.filter(제품구분="단품").order_by("-created")

        for s in order:
            try:
                s.생산요청.생산계획.작업지시서
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록
                except:
                    l_order.append(s)

            except:
                pass

        s_bool = False
    else:
        s_bool = True
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="단품")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분=search)
                | Q(제품구분=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__현장명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

        l_order = []
        for s in order:
            try:
                s.생산요청.생산계획.작업지시서
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록
                except:
                    l_order.append(s)

            except:
                pass

    if search_m is None:
        s_bool_m = False
        order = OR_models.OrderRegister.objects.all().order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)
    else:
        s_bool_m = True
        order = OR_models.OrderRegister.objects.filter(
            Q(수주코드__contains=search_m)
            | Q(영업구분=search_m)
            | Q(제품구분=search_m)
            | Q(사업장구분=search_m)
            | Q(고객사명__거래처명__contains=search_m)
            | Q(단품모델__모델명__contains=search_m)
            | Q(단품모델__모델코드__contains=search_m)
            | Q(랙모델__현장명__contains=search_m)
            | Q(랙모델__랙시리얼코드__contains=search_m)
        ).order_by("-created")
        a_order = []
        for s in order:
            if str(s.process())[0:3] == "생산중":
                a_order.append(s)

    pagediv = 7

    totalpage_m = int(math.ceil(len(a_order) / pagediv))
    paginator_m = Paginator(a_order, pagediv, orphans=0)
    page_m = request.GET.get("page_m", "1")
    a_order = paginator_m.get_page(page_m)
    nextpage_m = int(page_m) + 1
    previouspage_m = int(page_m) - 1
    notsamebool_m = True
    nonpage_m = False
    if totalpage_m == 0:
        nonpage_m = True

    totalpage = int(math.ceil(len(l_order) / pagediv))
    paginator = Paginator(l_order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    l_order = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    nonpage = False
    if totalpage == 0:
        nonpage = True

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
            "order_m": l_order,
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
            "nonpage": nonpage,
            "nonpage_m": nonpage_m,
            "최종검사완료": "최종검사완료",
            "최종검사의뢰완료": "최종검사의뢰완료",
            "수주등록완료": "수주등록완료",
            "생산의뢰완료": "생산의뢰완료",
        },
    )


@login_required(login_url="/")
def worklist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        l_order = []
        order = OR_models.OrderRegister.objects.filter(제품구분="단품").order_by("-created")

        for s in order:
            try:
                s.생산요청.생산계획.작업지시서
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록
                except:
                    l_order.append(s)

            except:
                pass

        s_bool = False
    else:
        s_bool = True
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="단품")
            .filter(
                Q(수주코드__contains=search)
                | Q(영업구분=search)
                | Q(제품구분=search)
                | Q(사업장구분=search)
                | Q(고객사명__거래처명__contains=search)
                | Q(단품모델__모델명__contains=search)
                | Q(단품모델__모델코드__contains=search)
                | Q(랙모델__현장명__contains=search)
                | Q(랙모델__랙시리얼코드__contains=search)
            )
            .order_by("-created")
        )

        l_order = []
        for s in order:
            try:
                s.생산요청.생산계획.작업지시서
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록
                except:
                    l_order.append(s)

            except:
                pass

    pagediv = 7

    totalpage = int(math.ceil(len(l_order) / pagediv))
    paginator = Paginator(l_order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    l_order = paginator.get_page(page)
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
        "producemanages/worklist.html",
        {
            "s_order": l_order,
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


@login_required(login_url="/")
def workregister(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획
    workorder = produceplan.작업지시서

    form = forms.UploadWorkForm(request.POST)

    if form.is_valid():
        생산일시 = form.cleaned_data.get("생산일시")
        생산수량 = form.cleaned_data.get("생산수량")
        특이사항 = form.cleaned_data.get("특이사항")
        if 생산일시 is None:
            생산일시 = timezone.now().date()

        SM = models.WorkOrderRegister.objects.create(
            작업지시서=workorder, 생산담당자=user, 생산일시=생산일시, 생산수량=생산수량, 특이사항=특이사항,
        )

        messages.success(request, "공정진행 등록이 완료되었습니다.")

        return redirect(reverse("producemanages:producehome"))
    return render(
        request,
        "producemanages/workregister.html",
        {
            "form": form,
            "order": order,
            "produceplan": produceplan,
            "orderproduce": orderproduce,
            "workorder": workorder,
            "today": timezone.now().date(),
        },
    )


@login_required(login_url="/")
def workdonelist(request):
    user = request.user
    search = request.GET.get("search")
    search_m = request.GET.get("search_m")

    if search_m is None:
        s_order_m = []
        l_order_m = []
        order = OR_models.OrderRegister.objects.filter(제품구분="단품").order_by("-created")

        for s in order:
            try:
                s.생산요청.생산계획.작업지시서.작업지시서등록
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                except:
                    l_order_m.append(s)
            except:
                pass
        for s in l_order_m:
            if s.생산요청.생산계획.작업지시서.작업지시서등록.생산담당자 == user:
                s_order_m.append(s)
        s_bool_m = False
    else:
        s_bool_m = True
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="단품")
            .filter(
                Q(수주코드__contains=search_m)
                | Q(영업구분=search_m)
                | Q(제품구분=search_m)
                | Q(사업장구분=search_m)
                | Q(고객사명__거래처명__contains=search_m)
                | Q(단품모델__모델명__contains=search_m)
                | Q(단품모델__모델코드__contains=search_m)
                | Q(랙모델__현장명__contains=search_m)
                | Q(랙모델__랙시리얼코드__contains=search_m)
            )
            .order_by("-created")
        )
        s_order_m = []
        l_order_m = []

        for s in order:
            try:
                s.생산요청.생산계획.작업지시서.작업지시서등록
                try:
                    s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                except:
                    l_order_m.append(s)
            except:
                pass
        for s in l_order_m:
            if s.생산요청.생산계획.작업지시서.작업지시서등록.생산담당자 == user:
                s_order_m.append(s)

    if search is None:
        order = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="최종검사결과")
            .order_by("-created")
        )
        s_order = []
        for s in order:
            try:
                s.최종검사
            except:
                s_order.append(s)
        s_bool = False
    else:
        s_bool = True
        order = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="최종검사결과")
            .filter(
                Q(최종검사결과__최종검사코드__contains=search)
                | Q(최종검사결과__제품__모델명__contains=search)
                | Q(최종검사결과__제품__모델코드__contains=search)
                | Q(작성자__first_name__contains=search)
                | Q(불량위치및자재__contains=search)
                | Q(수리내용__contains=search)
            )
            .order_by("-created")
        )

        s_order = []
        for s in order:
            try:
                s.최종검사
            except:
                s_order.append(s)

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
        "producemanages/workdonelist.html",
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


@login_required(login_url="/")
def orderfinalcheck(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획
    workorder = produceplan.작업지시서
    work = workorder.작업지시서등록

    SM = QC_models.FinalCheck.objects.create(작업지시서=work, 제품=order.단품모델)

    messages.success(request, "최종검사의뢰가 완료되었습니다.")

    return redirect(reverse("producemanages:workdonelist"))


@login_required(login_url="/")
def orderfinaldelete(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획
    workorder = produceplan.작업지시서
    work = workorder.작업지시서등록
    orderfinal = work.최종검사

    orderfinal.delete()

    messages.success(request, "최종검사의뢰가 철회되었습니다.")

    return redirect(reverse("producemanages:orderdetailforwork", kwargs={"pk": pk}))


@login_required(login_url="/")
def workdeleteensure(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획
    workorder = produceplan.작업지시서
    work = workorder.작업지시서등록

    return render(
        request,
        "producemanages/workdeleteensure.html",
        {"plan": produceplan, "order": order, "work": work},
    )


@login_required(login_url="/")
def workdelete(request, pk):
    user = request.user
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    orderproduce = order.생산요청
    produceplan = orderproduce.생산계획
    workorder = produceplan.작업지시서
    work = workorder.작업지시서등록
    work.delete()

    messages.success(request, "공정진행이 삭제되었습니다.")
    return redirect(reverse("producemanages:orderdetailforwork", kwargs={"pk": pk}))


class workupdate(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.WorkOrderRegister
    template_name = "producemanages/workupdate.html"
    form_class = forms.UploadWorkForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        work = models.WorkOrderRegister.objects.get_or_none(pk=pk)
        order = work.작업지시서.생산계획.생산의뢰.생산의뢰수주
        context["order"] = order
        context["today"] = timezone.now().date()
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        work = models.WorkOrderRegister.objects.get_or_none(pk=pk)
        order = work.작업지시서.생산계획.생산의뢰.생산의뢰수주
        pk = order.pk
        return reverse("producemanages:orderdetailforwork", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()
        생산일시 = form.cleaned_data.get("생산일시")
        생산수량 = form.cleaned_data.get("생산수량")
        특이사항 = form.cleaned_data.get("특이사항")
        if 생산일시 is None:
            생산일시 = timezone.now().date()
        pk = self.kwargs.get("pk")
        work = models.WorkOrderRegister.objects.get_or_none(pk=pk)
        work.생산일시 = 생산일시
        work.생산수량 = 생산수량
        work.특이사항 = 특이사항
        work.save()
        messages.success(self.request, "공정진행 수정이 완료되었습니다.")

        return super().form_valid(form)


@login_required(login_url="/")
def finalchecklist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        l_order = []
        최종검사 = QC_models.FinalCheckRegister.objects.exclude(부적합수량=0).order_by(
            "-created"
        )
        for s in 최종검사:
            if s.수리내역서.all():
                pass
            else:
                l_order.append(s)

        s_bool = False
    else:
        s_bool = True
        최종검사 = (
            QC_models.FinalCheckRegister.objects.exclude(부적합수량=0)
            .filter(
                Q(최종검사코드__contains=search)
                | Q(제품__모델명__contains=search)
                | Q(제품__모델코드__contains=search)
            )
            .order_by("-created")
        )

        l_order = []
        for s in 최종검사:
            if s.수리내역서.all():
                pass
            else:
                l_order.append(s)

    pagediv = 7

    totalpage = int(math.ceil(len(l_order) / pagediv))
    paginator = Paginator(l_order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    l_order = paginator.get_page(page)
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
        "producemanages/finalchecklist.html",
        {
            "s_order": l_order,
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


@login_required(login_url="/")
def repairregister(request, pk):
    user = request.user
    finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)

    form = forms.UploadRepairForm(request.POST)

    if form.is_valid():
        postedValue = request.POST
        postDict = dict(postedValue)

        불량위치및자재_list = postDict["불량위치및자재"]
        수리내용_list = postDict["수리내용"]
        실수리수량_list = postDict["실수리수량"]
        폐기수량_list = postDict["폐기수량"]
        특이사항_list = postDict["특이사항"]

        폐기수량_list = [int(x) for x in 폐기수량_list]
        실수리수량_list = [int(x) for x in 실수리수량_list]

        if (sum(폐기수량_list) + sum(실수리수량_list)) > finalcheck.부적합수량:
            messages.error(request, "수리수량과 폐기수량의 합이 부적합 수량보다 많을 수 없습니다.")
            return render(
                request,
                "producemanages/repairregister.html",
                {"form": form, "finalcheck": finalcheck,},
            )

        lenOflist = len(불량위치및자재_list)

        for repair_num in range(lenOflist):
            SM = QC_models.RepairRegister.objects.create(
                수리최종="최종검사결과",
                작성자=user,
                불량위치및자재=불량위치및자재_list[repair_num],
                특이사항=특이사항_list[repair_num],
                수리내용=수리내용_list[repair_num],
                실수리수량=실수리수량_list[repair_num],
                폐기수량=폐기수량_list[repair_num],
                제품=finalcheck.제품,
            )
            SM.최종검사결과.add(finalcheck)

        messages.success(request, "수리내역서가 %d개 등록이 완료되었습니다." % lenOflist)
        return redirect(reverse("producemanages:producehome"))
    return render(
        request,
        "producemanages/repairregister.html",
        {"form": form, "finalcheck": finalcheck,},
    )


class repairupdate(user_mixins.LoggedInOnlyView, UpdateView):
    model = QC_models.RepairRegister
    template_name = "producemanages/repairedit.html"
    form_class = forms.UploadRepairForm

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
        finalcheck = repair.최종검사결과.all()[0]
        context["finalcheck"] = finalcheck
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
        finalcheck = repair.최종검사결과.all()[0]
        order = finalcheck.최종검사의뢰.작업지시서.작업지시서.생산계획.생산의뢰.생산의뢰수주
        pk = order.pk
        return reverse("producemanages:orderdetailforwork", kwargs={"pk": pk})

    def form_valid(self, form):
        print("go")
        self.object = form.save()
        불량위치및자재 = form.cleaned_data.get("불량위치및자재")
        수리내용 = form.cleaned_data.get("수리내용")
        실수리수량 = form.cleaned_data.get("실수리수량")
        폐기수량 = form.cleaned_data.get("폐기수량")
        특이사항 = form.cleaned_data.get("특이사항")
        pk = self.kwargs.get("pk")
        repairPaper = QC_models.RepairRegister.objects.get_or_none(pk=pk)
        repairPaper.불량위치및자재 = 불량위치및자재
        repairPaper.수리내용 = 수리내용
        repairPaper.실수리수량 = 실수리수량
        repairPaper.폐기수량 = 폐기수량
        repairPaper.특이사항 = 특이사항
        print(실수리수량)
        repairPaper.save()

        return super().form_valid(form)


@login_required(login_url="/")
def repairlist(request):
    user = request.user
    search = request.GET.get("search")

    if search is None:
        l_order = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="최종검사결과")
            .order_by("-created")
        )
        s_bool = False
    else:
        s_bool = True
        l_order = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="최종검사결과")
            .filter(
                Q(최종검사결과__최종검사코드__contains=search)
                | Q(최종검사결과__제품__모델명__contains=search)
                | Q(최종검사결과__제품__모델코드__contains=search)
                | Q(작성자__first_name__contains=search)
                | Q(불량위치및자재__contains=search)
                | Q(수리내용__contains=search)
            )
            .order_by("-created")
        )

    pagediv = 7

    totalpage = int(math.ceil(len(l_order) / pagediv))
    paginator = Paginator(l_order, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    l_order = paginator.get_page(page)
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
        "producemanages/repairlist.html",
        {
            "s_order": l_order,
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


@login_required(login_url="/")
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
        "producemanages/repairdetail.html",
        {"repair": repair, "finalcheckboolean": finalcheckboolean, "user": user,},
    )


class repairupdateindetail(repairupdate):
    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
        finalcheck = repair.최종검사결과.all()[0]
        context["finalcheck"] = finalcheck
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
        pk = repair.pk
        return reverse("producemanages:repairdetail", kwargs={"pk": pk})


class repairupdateindetailAS(repairupdateindetail):
    template_name = "producemanages/repaireditAS.html"

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
        ASrequest = repair.AS수리의뢰
        context["ASrequest"] = ASrequest
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )


@login_required(login_url="/")
def repairdeleteensure(request, pk):
    repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
    return render(
        request, "producemanages/repairdeleteensure.html", {"repair": repair,}
    )


@login_required(login_url="/")
def repairdelete(request, pk):
    repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
    repair.delete()
    messages.success(request, "해당 수리내역서가 삭제되었습니다.")
    return redirect(reverse("producemanages:producehome",))


@login_required(login_url="/")
def orderfinalcheckforrepair(request, pk):
    repair = QC_models.RepairRegister.objects.get_or_none(pk=pk)
    SM = QC_models.FinalCheck.objects.create(수리내역서=repair, 제품=repair.제품)

    messages.success(request, "최종검사의뢰가 완료되었습니다.")

    return redirect(reverse("producemanages:workdonelist"))


@login_required(login_url="/")
def checkdonelist(request):
    user = request.user
    search = request.GET.get("search")
    search_m = request.GET.get("search_m")

    if search_m is None:
        s_order_m = []
        l_order_m = []
        order = OR_models.OrderRegister.objects.filter(제품구분="단품").order_by("-created")

        for s in order:
            try:
                s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                l_order_m.append(s)
            except:
                pass

        for s in l_order_m:
            if s.생산요청.생산계획.작업지시서.작업지시서등록.생산담당자 == user:
                s_order_m.append(s)
        s_bool_m = False
    else:
        s_bool_m = True
        order = (
            OR_models.OrderRegister.objects.filter(제품구분="단품")
            .filter(
                Q(수주코드__contains=search_m)
                | Q(영업구분=search_m)
                | Q(제품구분=search_m)
                | Q(사업장구분=search_m)
                | Q(고객사명__거래처명__contains=search_m)
                | Q(단품모델__모델명__contains=search_m)
                | Q(단품모델__모델코드__contains=search_m)
                | Q(랙모델__현장명__contains=search_m)
                | Q(랙모델__랙시리얼코드__contains=search_m)
            )
            .order_by("-created")
        )
        s_order_m = []
        l_order_m = []

        for s in order:
            try:
                s.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                l_order_m.append(s)
            except:
                pass
        for s in l_order_m:
            if s.생산요청.생산계획.작업지시서.작업지시서등록.생산담당자 == user:
                s_order_m.append(s)

    if search is None:
        order = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="최종검사결과")
            .order_by("-created")
        )
        s_order = []
        for s in order:
            try:
                s.최종검사
                s_order.append(s)
            except:
                pass
        s_bool = False
    else:
        s_bool = True
        order = (
            QC_models.RepairRegister.objects.filter(작성자=user)
            .filter(수리최종="최종검사결과")
            .filter(
                Q(최종검사결과__최종검사코드__contains=search)
                | Q(최종검사결과__제품__모델명__contains=search)
                | Q(최종검사결과__제품__모델코드__contains=search)
                | Q(작성자__first_name__contains=search)
                | Q(불량위치및자재__contains=search)
                | Q(수리내용__contains=search)
            )
            .order_by("-created")
        )

        s_order = []
        for s in order:
            try:
                s.최종검사
                s_order.append(s)
            except:
                pass

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
        "producemanages/checkdonelist.html",
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


@login_required(login_url="/")
def finalcheckdetail(request, pk):
    finalcheck = QC_models.FinalCheckRegister.objects.get_or_none(pk=pk)
    user = request.user
    if finalcheck.수리내역서.all():
        repairbool = True
    else:
        repairbool = False

    return render(
        request,
        "producemanages/finalcheckdetail.html",
        {"finalcheck": finalcheck, "repairbool": repairbool},
    )


@login_required(login_url="/")
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
        "producemanages/ASrequestlist.html",
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


@login_required(login_url="/")
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

        messages.success(request, "수리내역서 등록이 완료되었습니다.")
        return redirect(reverse("producemanages:producehome"))
    return render(
        request,
        "producemanages/repairregisterAS.html",
        {"form": form, "ASrequest": ASrequest,},
    )


@login_required(login_url="/")
def finalcheckrequestdelete(request, pk):
    finalcheckrequest = QC_models.FinalCheck.objects.get_or_none(pk=pk)
    pk = finalcheckrequest.수리내역서.pk
    finalcheckrequest.delete()
    messages.success(request, "최종검사 의뢰가 철회되었습니다.")
    return redirect(reverse("producemanages:repairdetail", kwargs={"pk": pk}))


@login_required(login_url="/")
def repairrequestdetail(request, pk):
    user = request.user
    repair = AS_models.ASRepairRequest.objects.get_or_none(pk=pk)
    return render(
        request,
        "producemanages/repairrequestdetail.html",
        {"repair": repair, "user": user,},
    )


class requestrackmakelist(core_views.onelist):
    templatename = "producemanages/requestrackmakelist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            requestrackmakelist = SR_models.StockOfRackProductOutRequest.objects.all().order_by(
                "-created"
            )
            queryset = []
            for s in requestrackmakelist:
                try:
                    s.랙조립
                except:
                    queryset.append(s)
            self.s_bool = False
        else:
            self.s_bool = True
            requestrackmakelist = SR_models.StockOfRackProductOutRequest.objects.filter(
                Q(수주__수주코드__contains=self.search)
                | Q(출하요청자__first_name__contains=self.search)
                | Q(랙__랙시리얼코드__contains=self.search)
                | Q(랙__현장명__contains=self.search)
                | Q(고객사__거래처명__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in requestrackmakelist:
                try:
                    s.랙조립
                except:
                    queryset.append(s)
        return queryset


@login_required(login_url="/")
def rackmakeregister(request, pk):
    user = request.user
    makerequest = SR_models.StockOfRackProductOutRequest.objects.get_or_none(pk=pk)

    form = forms.rackmakeregister(request.POST)
    form.initial = {
        "제작수량": makerequest.출하요청수량,
    }

    if form.is_valid():
        현재공정 = form.cleaned_data.get("현재공정")
        제작수량 = form.cleaned_data.get("제작수량")
        랙조립일자 = form.cleaned_data.get("랙조립일자")
        특이사항 = form.cleaned_data.get("특이사항")

        SM = SR_models.StockOfRackProductMaker.objects.create(
            현재공정=현재공정,
            랙=makerequest.랙,
            랙출하요청=makerequest,
            제작수량=제작수량,
            랙조립기사=user,
            랙조립일자=랙조립일자,
            특이사항=특이사항,
        )

        messages.success(request, "랙조립 등록이 완료되었습니다.")

        return redirect(reverse("producemanages:requestrackmakelist"))
    selectlist = [
        "현재공정",
    ]
    return render(
        request,
        "producemanages/rackmakeregister.html",
        {"form": form, "makerequest": makerequest, "selectlist": selectlist,},
    )


class rackmakeedit(user_mixins.LoggedInOnlyView, UpdateView):
    model = SR_models.StockOfRackProductMaker
    template_name = "producemanages/rackmakeedit.html"
    form_class = forms.rackmakeregister

    def render_to_response(self, context, **response_kwargs):

        response_kwargs.setdefault("content_type", self.content_type)
        pk = self.kwargs.get("pk")
        makerequest = SR_models.StockOfRackProductMaker.objects.get_or_none(pk=pk)
        order = makerequest.랙출하요청.수주
        context["makerequest"] = makerequest
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        makerequest = SR_models.StockOfRackProductMaker.objects.get_or_none(pk=pk)
        order = makerequest.랙출하요청.수주
        pk = order.pk
        return reverse("producemanages:orderdetail", kwargs={"pk": pk})

    def form_valid(self, form):
        self.object = form.save()

        현재공정 = form.cleaned_data.get("현재공정")
        제작수량 = form.cleaned_data.get("제작수량")
        랙조립일자 = form.cleaned_data.get("랙조립일자")
        특이사항 = form.cleaned_data.get("특이사항")
        pk = self.kwargs.get(self.pk_url_kwarg)
        makerequest = SR_models.StockOfRackProductMaker.objects.get_or_none(pk=pk)
        makerequest.현재공정 = 현재공정
        makerequest.제작수량 = 제작수량
        makerequest.랙조립일자 = 랙조립일자
        makerequest.특이사항 = 특이사항
        makerequest.save()

        messages.success(self.request, "수정이 완료되었습니다.")
        return super().form_valid(form)


@login_required(login_url="/")
def rackmakedeleteensure(request, pk):
    makerequest = SR_models.StockOfRackProductMaker.objects.get_or_none(pk=pk)

    return render(
        request,
        "producemanages/rackmakedeleteensure.html",
        {"makerequest": makerequest,},
    )


@login_required(login_url="/")
def rackmakedelete(request, pk):
    makerequest = SR_models.StockOfRackProductMaker.objects.get_or_none(pk=pk)
    order = makerequest.랙출하요청.수주
    pk = order.pk
    makerequest.delete()
    messages.success(request, "랙조립이 삭제되었습니다.")
    return redirect(reverse("producemanages:orderdetail", kwargs={"pk": pk}))


class monthlyplanlist(core_views.onelist):
    templatename = "producemanages/monthlyplanlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:
            monthlyplan = OR_models.OrderRegister.objects.filter(
                영업구분="월별생산계획"
            ).order_by("-created")
            monthlyplan = list(monthlyplan)
            try:
                newest = monthlyplan[0]
                oldest = monthlyplan[-1]
                yeargap = newest.created.year - oldest.created.year
                monthgap = newest.created.month - oldest.created.month
                totalgap = yeargap * 12 + monthgap
                totalgaprange = list(range(0, totalgap + 1))
                totalgaprange.sort(reverse=True)
                self.startyear = oldest.created.year
                self.startmonth = oldest.created.month

                queryset = totalgaprange
            except:
                queryset = []
                self.startyear = None
                self.startmonth = None

            self.s_bool = False
        else:
            self.s_bool = True
            monthlyplan = SR_models.StockOfRackProductOutRequest.objects.filter(
                Q(수주__수주코드__contains=self.search)
                | Q(출하요청자__first_name__contains=self.search)
                | Q(랙__랙시리얼코드__contains=self.search)
                | Q(랙__현장명__contains=self.search)
                | Q(고객사__거래처명__contains=self.search)
            ).order_by("-created")
            queryset = []
            for s in monthlyplan:
                try:
                    s.랙조립
                except:
                    queryset.append(s)
        return queryset

    def get(self, request):
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
                "startmonth": self.startmonth,
                "startyear": self.startyear,
            },
        )


@login_required(login_url="/")
def monthlyplandetail(request, ypk, mpk):
    listformonth = OR_models.OrderRegister.objects.filter(영업구분="월별생산계획").order_by(
        "-created"
    )
    queryset = []
    for order in listformonth:
        if (order.created.year == ypk) and (order.created.month == mpk):
            queryset.append(order)

    return render(
        request,
        "producemanages/monthlyplandetail.html",
        {"queryset": queryset, "ypk": ypk, "mpk": mpk,},
    )


class monthlyplannewlist(core_views.onelist):
    templatename = "producemanages/monthlyplannewlist.html"

    def get_first_queryset(self, request):
        self.search = request.GET.get("search")
        if self.search is None:

            monthlyplan = models.MonthlyProduceList.objects.all().order_by("created")
            queryset = list(monthlyplan)

            self.s_bool = False
        else:
            self.s_bool = True
            monthlyplan = models.MonthlyProduceList.objects.filter(
                Q(작성자__first_name__contains=self.search)
                | Q(단품모델__모델코드__contains=self.search)
                | Q(단품모델__모델명__contains=self.search)
            ).order_by("created")
            queryset = list(monthlyplan)
        return queryset


@login_required(login_url="/")
def monthlyplanregister(request, pk):
    form = forms.monthlyplanregister(request.POST)
    monthlyplan = models.MonthlyProduceList.objects.get_or_none(pk=pk)
    user = request.user
    수량 = monthlyplan.수량

    form.initial = {"수량": 수량}

    if form.is_valid():
        수량 = form.cleaned_data.get("수량")

        def give_new_number():
            while True:
                n = randint(1, 999999)
                num = str(n).zfill(6)
                code = "OR" + num
                obj = OR_models.OrderRegister.objects.get_or_none(수주코드=code)
                if obj:
                    pass
                else:
                    return code

        def give_number():
            while True:
                n = randint(1, 999999)
                num = str(n).zfill(6)
                code = "OP" + num
                obj = OR_models.OrderProduce.objects.get_or_none(생산의뢰코드=code)
                if obj:
                    pass
                else:
                    return code

        single_order = OR_models.OrderRegister.objects.create(
            작성자=user,
            수주코드=give_new_number(),
            영업구분="월별생산계획",
            사업장구분="삼형전자",
            수주일자=timezone.now().date(),
            현장명="월별생산계획",
            특이사항="월별생산계획",
            제품구분="단품",
            단품모델=monthlyplan.단품모델,
            납품수량=수량,
            출하구분="출하미완료",
        )

        SM = OR_models.OrderProduce.objects.create(
            생산의뢰수주=single_order, 생산의뢰코드=give_number(), 긴급도="일반", 생산목표수량=수량,
        )

        def give_PP_number():
            while True:
                n = randint(1, 999999)
                num = str(n).zfill(6)
                code = "PP" + num
                obj = models.ProduceRegister.objects.get_or_none(생산계획등록코드=code)
                if obj:
                    pass
                else:
                    return code

        PP = models.ProduceRegister.objects.create(
            작성자=user,
            생산계획등록코드=give_PP_number(),
            생산의뢰=SM,
            현재공정="예비작업",
            현재공정달성율="0%",
            계획생산량=수량,
            일일생산량=0,
            누적생산량=0,
            특이사항="월별생산계획",
        )

        WO = models.WorkOrder.objects.create(
            생산계획=PP, 수리생산="생산계획", 작업지시코드=give_PP_number(), 수량=수량, 특이사항="월별생산계획의 작업지시서",
        )
        monthlyplan.수량 = 수량
        monthlyplan.작성자 = user
        monthlyplan.작성일 = timezone.now().date()
        monthlyplan.save()

        return HttpResponse(
            '<script type="text/javascript">opener.location.reload(); window.close()</script>'
        )
    return render(
        request,
        "producemanages/monthlyplanregister.html",
        {"monthlyplan": monthlyplan, "user": user, "form": form,},
    )


@login_required(login_url="/")
def monthlyplanregisternew(request):
    search = request.GET.get("search")
    if search is None:
        customer = []
        custo = SI_models.SingleProduct.objects.all().order_by("-created")
        for c in custo:
            try:
                c.월별생산계획
            except:
                customer.append(c)
        s_bool = False
    else:
        s_bool = True
        custo = SI_models.SingleProduct.objects.filter(
            Q(모델코드=search)
            | Q(모델명__contains=search)
            | Q(규격=search)
            | Q(단위=search)
            | Q(작성자__first_name=search)
        ).order_by("-created")
        customer = []
        for c in custo:
            try:
                c.월별생산계획
            except:
                customer.append(c)

    form = forms.monthlyplanregisternew(request.POST)
    user = request.user

    if form.is_valid():
        단품모델 = form.cleaned_data.get("단품모델")
        수량 = form.cleaned_data.get("수량")

        def give_new_number():
            while True:
                n = randint(1, 999999)
                num = str(n).zfill(6)
                code = "OR" + num
                obj = OR_models.OrderRegister.objects.get_or_none(수주코드=code)
                if obj:
                    pass
                else:
                    return code

        def give_number():
            while True:
                n = randint(1, 999999)
                num = str(n).zfill(6)
                code = "OP" + num
                obj = OR_models.OrderProduce.objects.get_or_none(생산의뢰코드=code)
                if obj:
                    pass
                else:
                    return code

        single_order = OR_models.OrderRegister.objects.create(
            작성자=user,
            수주코드=give_new_number(),
            영업구분="월별생산계획",
            사업장구분="삼형전자",
            수주일자=timezone.now().date(),
            현장명="월별생산계획",
            특이사항="월별생산계획",
            제품구분="단품",
            단품모델=단품모델,
            납품수량=수량,
            출하구분="출하미완료",
        )

        SM = OR_models.OrderProduce.objects.create(
            생산의뢰수주=single_order, 생산의뢰코드=give_number(), 긴급도="일반", 생산목표수량=수량,
        )

        def give_PP_number():
            while True:
                n = randint(1, 999999)
                num = str(n).zfill(6)
                code = "PP" + num
                obj = models.ProduceRegister.objects.get_or_none(생산계획등록코드=code)
                if obj:
                    pass
                else:
                    return code

        PP = models.ProduceRegister.objects.create(
            작성자=user,
            생산계획등록코드=give_PP_number(),
            생산의뢰=SM,
            현재공정="예비작업",
            현재공정달성율="0%",
            계획생산량=수량,
            일일생산량=0,
            누적생산량=0,
            특이사항="월별생산계획",
        )

        WO = models.WorkOrder.objects.create(
            생산계획=PP, 수리생산="생산계획", 작업지시코드=give_PP_number(), 수량=수량, 특이사항="월별생산계획의 작업지시서",
        )

        MP = models.MonthlyProduceList.objects.create(
            수량=수량, 단품모델=단품모델, 작성자=user, 작성일=timezone.now().date(),
        )

        return HttpResponse(
            '<script type="text/javascript">opener.location.reload(); window.close()</script>'
        )
    pagediv = 6
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
        "producemanages/monthlyplanregisternew.html",
        {
            "user": user,
            "form": form,
            "customer": customer,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
        },
    )


@login_required(login_url="/")
def deleteallplan(request, pk, ypk, mpk):
    order = OR_models.OrderRegister.objects.get_or_none(pk=pk)
    try:
        workorder = order.생산요청.생산계획.작업지시서
        workorder.delete()
    except:
        pass
    try:
        produceplan = order.생산요청.생산계획
        produceplan.delete()
    except:
        pass
    try:
        orderproduce = order.생산요청
        orderproduce.delete()
    except:
        pass
    order.delete()

    messages.success(request, "생산계획이 철회되었습니다.")
    return redirect(
        reverse("producemanages:monthlyplandetail", kwargs={"ypk": ypk, "mpk": mpk})
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
            "producemanages/rackdetail.html",
            {"rack": rack, "user": user, "material": material, "single": single},
        )
