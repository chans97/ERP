from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.SpecialApplyRegister)
class SpecialApplyRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "특채신청수량")


@admin.register(models.SpecialRegister)
class SpecialRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "특채수량")


@admin.register(models.SpecialConductRegister)
class SpecialConductRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "특채수량중납품수량")


@admin.register(models.SpecialRejectRegister)
class SpecialRejectRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "특채반품수량")
