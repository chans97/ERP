from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
@admin.register(models.StockOfRackProductOutRequest)
class StockOfRackProductOutRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfRackProductOut)
class StockOfRackProductOut(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.StockOfRackProductMaker)
class StockOfRackProductMaker(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
