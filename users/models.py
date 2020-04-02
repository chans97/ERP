from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """custom user """

    부서 = models.ManyToManyField("Part", related_name="user", null=True)

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def __str__(self):
        return self.first_name
    def lenofpart(self):
        num = self.부서.count()
        return num


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
