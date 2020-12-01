from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.ASRegisters)
class ASRegisters(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.ASVisitContents)
class ASVisitContents(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.ASRepairRequest)
class ASRepairRequest(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.ASReVisitContents)
class ASReVisitContents(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.ASResults)
class v(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"

