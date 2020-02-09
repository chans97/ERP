from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
@admin.register(models.MeasureCheckRegister)
class MeasureCheckRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"


@admin.register(models.MeasureRepairRegister)
class MeasureRepairRegister(admin.ModelAdmin):
    empty_value_display = "입력 값 없음"
    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width ="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "계측기수리사진"
