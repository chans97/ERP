from django.contrib import admin
from django.utils.html import mark_safe
from . import models
from . import forms


@admin.register(models.partnermigrate)
class partnermigrate(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
