from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.Partner)
class Partner(admin.ModelAdmin):
    list_display = (
        "거래처명",
        "거래처구분",
        "담당자",
        "사용여부",
    )


@admin.register(models.Material)
class Material(admin.ModelAdmin):
    list_display = (
        "자재품명",
        "자재공급업체",
    )


@admin.register(models.SingleProduct)
class SingleProduct(admin.ModelAdmin):

    filter_horizontal = ("단품구성자재",)
    list_display = (
        "모델명",
        "규격",
        "단위",
    )


@admin.register(models.SingleProductMaterial)
class SingleProductMeterial(admin.ModelAdmin):

    filter_horizontal = ("단품구성자재",)


@admin.register(models.RackProduct)
class RackProduct(admin.ModelAdmin):
    filter_horizontal = ("랙구성단품",)
    list_display = (
        "랙모델명",
        "규격",
        "단위",
    )


@admin.register(models.RackProductMaterial)
class RackProductMaterial(admin.ModelAdmin):
    filter_horizontal = ("랙구성단품",)


@admin.register(models.Measure)
class Measure(admin.ModelAdmin):

    list_display = (
        "계측기명",
        "설치년월일",
        "설치장소",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width ="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "계측기사진"

