from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from importlib import import_module


class User(AbstractUser, TimeStampedModel):
    """custom user """

    부서 = models.ManyToManyField("Part", related_name="user")
    nowPart = models.ForeignKey(
        "Part", related_name="nowuser", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def __str__(self):
        return self.first_name

    def lenofpart(self):
        num = self.부서.count()
        return num

    def ordercount(self):
        count = self.수주등록.count()
        return count


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        "User", related_name="logged_in_user", on_delete=models.CASCADE
    )
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Company(TimeStampedModel):
    """회사명"""

    회사명 = models.CharField(max_length=12, null=True, blank=True)
    사업자등록번호 = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "회사"
        verbose_name_plural = "회사"

    def __str__(self):
        return self.회사명


class Part(TimeStampedModel):
    """부서"""

    해당회사 = models.ForeignKey(
        "Company", related_name="Part", on_delete=models.CASCADE, null=True
    )
    부서명 = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = "부서"
        verbose_name_plural = "부서"

    def __str__(self):
        return f"{self.해당회사} - {self.부서명}"


class Passward(TimeStampedModel):
    """passward for sign up"""

    pw = models.CharField(max_length=12, null=True, blank=True)
