from django.contrib import admin
from . import models


@admin.register(models.ProduceRegister)
class ProduceRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "현재공정", "현재공정달성율", "계획생산량", "누적생산량", "successrate")


@admin.register(models.WorkOrder)
class WorkOrder(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "수량")


@admin.register(models.WorkOrderRegister)
class WorkOrderRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "생산담당자")


@admin.register(models.MonthlyProduceList)
class MonthlyProduceList(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "__str__",
        "단품모델",
        "수량",
        "작성자",
    )
