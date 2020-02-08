from django.contrib import admin
from . import models


@admin.register(models.FinalCheck)
class FinalCheck(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.FinalCheckRegister)
class FinalCheckRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.RepairRegister)
class RepairRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.MaterialCheckRegister)
class MaterialCheckRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.MaterialCheck)
class MaterialCheck(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.LowMetarial)
class LowMetarial(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
