from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.OrderRegister)
class OrderRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "수주코드",
        "영업구분",
        "사업장구분",
        "납품요청일",
        "단품모델",
    )


@admin.register(models.OrderProduce)
class OrderProduce(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = (
        "__str__",
        "긴급도",
        "생산목표수량",
    )
