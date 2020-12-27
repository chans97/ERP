from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.Partner)
class Partner(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "거래처명",
        "거래처구분",
        "담당자",
        "사용여부",
    )


@admin.register(models.Material)
class Material(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "자재품명",
        "자재공급업체",
    )


@admin.register(models.SingleProduct)
class SingleProduct(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

    list_display = (
        "모델명",
        "규격",
        "단위",
    )


@admin.register(models.SingleProductMaterial)
class SingleProductMeterial(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

    list_display = (
        "__str__",
        "단품모델",
    )


@admin.register(models.RackProduct)
class RackProduct(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "현장명",
        "규격",
        "단위",
    )


@admin.register(models.RackProductMaterial)
class RackProductMaterial(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

    list_display = (
        "__str__",
        "랙모델",
    )


@admin.register(models.Measure)
class Measure(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

    list_display = (
        "계측기명",
        "설치년월일",
        "설치장소",
    )


@admin.register(models.SupplyPartner)
class SupplyPartner(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.CustomerPartner)
class CustomerPartner(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

