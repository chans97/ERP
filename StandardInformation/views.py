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


class PartnerView(ListView):
    """HomeView Def"""

    model = models.Partner
    paginate_by = 6
    paginate_orphans = 2
    ordering = "-created"
    context_object_name = "lists"
    template_name = "Standardinformation/partner.html"


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


class PartnerSearchView(ListView):

    model = models.Partner
    paginate_by = 6
    paginate_orphans = 2
    context_object_name = "lists"
    template_name = "Standardinformation/partnersearch.html"

    def get_queryset(self):
        r = self.request.GET.get("search")

        qs = models.Partner.objects.filter(
            Q(거래처코드=r)
            | Q(거래처구분=r)
            | Q(거래처명__contains=r)
            | Q(담당자__first_name=r)
            | Q(사업장주소__contains=r)
            | Q(작성자__first_name=r)
        ).order_by("-created")

        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
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
        context["ss"] = request.GET.get("search")
        return self.render_to_response(context)


class PartnerDetialView(DetailView):
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


def clean(self):
    code = self.cleaned_data.get("거래처코드")
    partner = models.Partner.objects.filter(거래처코드=code)
    partner = list(partner)
    code = code[0:2]
    if partner:
        self.add_error("거래처코드", forms.ValidationError("해당 거래처코드는 이미 존재합니다."))
    elif code != "PN":
        self.add_error("거래처코드", forms.ValidationError("거래처 코드는 PN으로 시작해야 합니다."))

        return self.cleaned_data


class SingleView(ListView):
    """SingleView Def"""

    model = models.SingleProduct
    paginate_by = 6
    paginate_orphans = 2
    ordering = "-created"
    context_object_name = "lists"
    template_name = "Standardinformation/single.html"


class SingleSearchView(ListView):

    model = models.SingleProduct
    paginate_by = 6
    paginate_orphans = 2
    context_object_name = "lists"
    template_name = "Standardinformation/singlesearch.html"

    def get_queryset(self):
        r = self.request.GET.get("search")

        qs = models.SingleProduct.objects.filter(
            Q(모델코드=r) | Q(모델명__contains=r) | Q(규격=r) | Q(단위=r) | Q(작성자__first_name=r)
        ).order_by("-created")

        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
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
        context["ss"] = request.GET.get("search")
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

        messages.success(request, "해당 단품에 포함되는 자재를 기입해주세요.")
        return redirect(
            reverse("StandardInformation:singlematerial", kwargs={"pk": pk})
        )

    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = forms.UploadSingleForm

        return render(
            request, "Standardinformation/singleregister.html", {"form": form},
        )


class SingleDetialView(DetailView):
    model = models.SingleProduct

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        single = models.SingleProduct.objects.get(pk=pk)

        material = single.단품구성자재.all()
        materialnamenum = []
        for mate in material:
            mn = list(mate.단품구성자재.all())[0]
            num = mate.수량
            materialnamenum.append([mn, num])

        user = request.user
        return render(
            request,
            "Standardinformation/singledetail.html",
            {"single": single, "user": user, "materialnamenum": materialnamenum,},
        )


def singlematerial(request, pk):
    single = models.SingleProduct.objects.get(pk=pk)
    form = forms.UploadSingleMaterialForm(request.POST)
    if form.is_valid():
        단품구성자재 = form.cleaned_data.get("단품구성자재")
        수량 = form.cleaned_data.get("수량")
        print(single, 단품구성자재, 수량)
        SM = models.SingleProductMaterial.objects.create(단품모델=single, 수량=수량)
        SM.단품구성자재.set(단품구성자재)
        SM.save()

        messages.success(request, "단품등록이 완료되었습니다..")

        return redirect(reverse("StandardInformation:single"))

    return render(
        request,
        "Standardinformation/singlematerial.html",
        {"single": single, "form": form},
    )
