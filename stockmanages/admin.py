from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.StockOfMaterial)
class StockOfMaterial(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialHistory)
class StockOfMaterialHistory(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialInRequest)
class StockOfMaterialInRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfMaterialIn)
class StockOfMaterialIn(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

