from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.StockOfSingleProduct)
class StockOfSingleProduct(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "__str__",
        "실수량",
        "입고요청포함수량",
        "출하요청제외수량",
    )


@admin.register(models.StockOfSingleProductHistory)
class StockOfSingleProductHistory(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfSingleProductInRequest)
class StockOfSingleProductInRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfSingleProductIn)
class StockOfSingleProductIn(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfSingleProductOutRequest)
class StockOfSingleProductOutRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfSingleProductOut)
class StockOfSingleProductOut(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
