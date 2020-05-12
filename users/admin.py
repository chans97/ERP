from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "is_active",
        # "username",
    )

    fieldsets = UserAdmin.fieldsets + (("Profile", {"fields": ("부서", "nowPart")},),)


@admin.register(models.Company)
class CustomCooporation(admin.ModelAdmin):
    pass


@admin.register(models.Part)
class CustomPart(admin.ModelAdmin):
    pass


@admin.register(models.Passward)
class Passward(admin.ModelAdmin):
    pass
