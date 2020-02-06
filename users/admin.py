from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "email",
        "부서",
        "is_active",
        # "username",
    )

    fieldsets = UserAdmin.fieldsets + (("Profile", {"fields": ("부서",)},),)


@admin.register(models.Company)
class CustomCooporation(admin.ModelAdmin):
    pass


@admin.register(models.Part)
class CustomPart(admin.ModelAdmin):
    pass
