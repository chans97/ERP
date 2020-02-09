from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.StockOfMaterial)
class StockOfMaterial(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "__str__",
        "실수량",
        "입고요청포함수량",
        "출고요청제외수량",
    )


@admin.register(models.StockOfMaterialHistory)
class StockOfMaterialHistory(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialInRequest)
class StockOfMaterialInRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialIn)
class StockOfMaterialIn(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialOutRequest)
class StockOfMaterialOutRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialOut)
class StockOfMaterialOut(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
