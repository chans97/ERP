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


class PartnerView(user_mixins.LoggedInOnlyView, ListView):
    """HomeView Def"""

    model = models.Partner
    paginate_by = 6
    paginate_orphans = 2
    ordering = "-created"
    context_object_name = "lists"
    template_name = "Standardinformation/partner.html"
    # extra_context = {"search": "검색"}

    def get_queryset(self):

        search = self.request.GET.get("search")
        if search is None:
            return super().get_queryset()
        else:
            qs = models.Partner.objects.filter(
                Q(거래처코드=search)
                | Q(거래처구분=search)
                | Q(거래처명__contains=search)
                | Q(담당자__first_name=search)
                | Q(사업장주소__contains=search)
                | Q(작성자__first_name=search)
            ).order_by("-created")

            return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {"class_name": self.__class__.__name__,}
                )
        context = self.get_context_data()
        if self.request.GET.get("search") is None:
            context["search"] = "search"
            context["s_bool"] = False
        else:
            context["search"] = self.request.GET.get("search")
            context["s_bool"] = True
        return self.render_to_response(context)


class UploadPartnerView(user_mixins.LoggedInOnlyView, FormView):
    model = models.Partner
    fields = (
        "거래처구분",
        "거래처코드",
        "거래처명",
        "사업자등록번호",
        "담당자",
        "연락처",
        "이메일",
        "사업장주소",
        "사업자등록증첨부",
        "특이사항",
        "사용여부",
    )
    template_name = "Standardinformation/partnerregister.html"
    form_class = forms.UploadPartnerForm

    def form_valid(self, form):
        partner = form.save()
        user = self.request.user
        request = self.request

        partner.작성자 = user
        partner.save()
        form.save_m2m()

        messages.success(request, "거래처가 등록되었습니다.")
        return redirect(reverse("StandardInformation:partner"))

    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = forms.UploadPartnerForm

        return render(
            request, "Standardinformation/partnerregister.html", {"form": form},
        )


class PartnerDetialView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Partner

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        partner = models.Partner.objects.get(pk=pk)
        user = request.user
        return render(
            request,
            "Standardinformation/partnerdetail.html",
            {"partner": partner, "user": user},
        )


###png 올리기
"""
def scripts_download(request, pk):

    partner = models.Partner.objects.get_or_none(pk=pk)
    scripts = partner.사업자등록증첨부.path
    title = partner.사업자등록증첨부.__str__()

    response = HttpResponse(open(scripts, "rb"), content_type="image/png")
    response["Content-Disposition"] = "attachment; filename=" + title
    return response"""


def file_download(request, pk):
    """모든파일다운로드"""

    partner = models.Partner.objects.get_or_none(pk=pk)
    file = partner.사업자등록증첨부.path
    title = partner.사업자등록증첨부.__str__()

    response = HttpResponse(open(file, "rb"), content_type="file")
    response["Content-Disposition"] = "attachment; filename=" + title
    return response


def partnerdeleteensure(request, pk):

    partner = models.Partner.objects.get_or_none(pk=pk)
    return render(
        request, "Standardinformation/partnerdeleteensure.html", {"partner": partner},
    )


def partnerdelete(request, pk):
    partner = models.Partner.objects.get_or_none(pk=pk)
    code = partner.거래처코드
    if partner.거래처구분 == "공급처":
        supply = models.SupplyPartner.objects.get(거래처코드=code)
        supply.delete()
    elif partner.거래처구분 == "고객":
        customer = models.CustomerPartner.objects.get(거래처코드=code)
        customer.delete()
    else:
        pass

    partner.delete()

    messages.success(request, "거래처가 삭제되었습니다.")

    return redirect(reverse("StandardInformation:partner"))


class EditPartnerView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Partner
    fields = (
        "거래처구분",
        "거래처명",
        "사업자등록번호",
        "담당자",
        "연락처",
        "이메일",
        "사업장주소",
        "사업자등록증첨부",
        "특이사항",
        "사용여부",
    )
    template_name = "Standardinformation/partneredit.html"


class SingleView(ListView):
    """SingleView Def"""

    model = models.SingleProduct
    paginate_by = 6
    paginate_orphans = 2
    ordering = "-created"
    context_object_name = "lists"
    template_name = "Standardinformation/single.html"

    def get_queryset(self):

        search = self.request.GET.get("search")
        if search is None:
            return super().get_queryset()
        else:
            qs = models.SingleProduct.objects.filter(
                Q(모델코드=search)
                | Q(모델명__contains=search)
                | Q(규격=search)
                | Q(단위=search)
                | Q(작성자__first_name=search)
            ).order_by("-created")

            return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {"class_name": self.__class__.__name__,}
                )
        context = self.get_context_data()
        if self.request.GET.get("search") is None:
            context["search"] = "search"
            context["s_bool"] = False
        else:
            context["search"] = self.request.GET.get("search")
            context["s_bool"] = True
        return self.render_to_response(context)


class UploadSingleView(user_mixins.LoggedInOnlyView, FormView):
    model = models.SingleProduct
    fields = (
        "모델코드",
        "모델명",
        "규격",
        "단위",
        "단가",
    )
    template_name = "Standardinformation/singleregister.html"
    form_class = forms.UploadSingleForm

    def form_valid(self, form):
        single = form.save()
        user = self.request.user
        request = self.request

        single.작성자 = user
        single.save()
        form.save_m2m()
        pk = single.pk

        messages.success(request, "해당 단품에 포함되는 자재를 추가해주세요.")
        return redirect(
            reverse("StandardInformation:singlematerial", kwargs={"pk": pk})
        )

    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = forms.UploadSingleForm

        return render(
            request, "Standardinformation/singleregister.html", {"form": form},
        )


class SingleDetialView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.SingleProduct

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        single = models.SingleProduct.objects.get(pk=pk)

        material = single.단품구성자재.all()
        user = request.user
        return render(
            request,
            "Standardinformation/singledetail.html",
            {"single": single, "user": user, "material": material},
        )


def singlematerial(request, pk):
    single = models.SingleProduct.objects.get(pk=pk)
    form = forms.UploadSingleMaterialForm(request.POST)

    search = request.GET.get("search")
    if search is None:
        material = models.Material.objects.all().order_by("-created")
        s_bool = False
    else:
        s_bool = True
        qs = models.Material.objects.filter(
            Q(자재코드=search)
            | Q(자재품명__contains=search)
            | Q(품목__contains=search)
            | Q(자재공급업체__거래처명__contains=search)
        ).order_by("-created")
        material = qs

    if form.is_valid():
        단품구성자재 = form.cleaned_data.get("단품구성자재")
        수량 = form.cleaned_data.get("수량")
        SM = models.SingleProductMaterial.objects.create(
            단품모델=single, 단품구성자재=단품구성자재, 수량=수량
        )

        return redirect(
            reverse("StandardInformation:singlematerial", kwargs={"pk": pk})
        )
    pagediv = 10
    totalpage = int(math.ceil(len(material) / pagediv))
    paginator = Paginator(material, pagediv, orphans=0)
    page = request.GET.get("page", "1")
    material = paginator.get_page(page)
    nextpage = int(page) + 1
    previouspage = int(page) - 1
    notsamebool = True
    materialofsingle = single.단품구성자재.all()
    if int(page) == totalpage:
        notsamebool = False
    if search is None:
        search = "search"
    return render(
        request,
        "Standardinformation/singlematerial.html",
        {
            "single": single,
            "form": form,
            "material": material,
            "search": search,
            "page": page,
            "totalpage": totalpage,
            "notsamebool": notsamebool,
            "nextpage": nextpage,
            "previouspage": previouspage,
            "s_bool": s_bool,
            "materialofsingle": materialofsingle,
        },
    )


def deletematerialofsingle(request, pk, m_pk):

    materialofsingle = models.SingleProductMaterial.objects.get(pk=m_pk)
    materialofsingle.delete()
    return redirect(reverse("StandardInformation:singlematerial", kwargs={"pk": pk}))


def singledeleteensure(request, pk):

    single = models.SingleProduct.objects.get_or_none(pk=pk)
    return render(
        request, "Standardinformation/singledeleteensure.html", {"single": single},
    )


def singledelete(request, pk):
    single = models.SingleProduct.objects.get_or_none(pk=pk)
    single.delete()

    messages.success(request, "해당 단품이 삭제되었습니다.")

    return redirect(reverse("StandardInformation:single"))


class EditSingleView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.SingleProduct
    fields = (
        "모델코드",
        "모델명",
        "규격",
        "단위",
        "단가",
    )
    template_name = "Standardinformation/singleedit.html"

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse("StandardInformation:singlematerial", kwargs={"pk": pk})

