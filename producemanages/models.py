from django.db import models
import math
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from django.utils import timezone
from StandardInformation import models as SI_models


class ProduceRegister(TimeStampedModel):

    예비작업 = "예비작업"
    조립 = "조립"
    검사 = "검사"
    현재공정_CHOICES = (
        (예비작업, "예비작업"),
        (조립, "조립"),
        (검사, "검사"),
    )
    사영 = "0%"
    사일 = "25%"
    사이 = "50%"
    사삼 = "75%"
    사사 = "100%"
    현재공정달성율_CHOICES = (
        (사영, "0%"),
        (사일, "25%"),
        (사이, "50%"),
        (사삼, "75%"),
        (사사, "100%"),
    )
    작성자 = models.ForeignKey(
        users_models.User,
        related_name="생산계획등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    생산계획등록코드 = models.CharField(max_length=50)
    생산의뢰 = models.OneToOneField(
        orders_models.OrderProduce,
        related_name="생산계획",
        on_delete=models.SET_NULL,
        null=True,
    )
    현재공정 = models.CharField(
        choices=현재공정_CHOICES, max_length=10, null=True, default=예비작업
    )
    현재공정달성율 = models.CharField(
        choices=현재공정달성율_CHOICES, max_length=10, null=True, default=사영
    )
    계획생산량 = models.IntegerField(null=True)
    일일생산량 = models.IntegerField(null=True)
    누적생산량 = models.IntegerField(null=True, blank=True)
    특이사항 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "생산계획등록"
        verbose_name_plural = "생산계획등록"

    def __str__(self):
        return f" '{self.생산의뢰}' 의 생산계획 : {self.생산계획등록코드}"

    def successrate(self):
        if self.누적생산량 is None:
            return f"0%"
        else:
            rate = (self.누적생산량 / self.계획생산량) * 100
            rate = round(rate, 2)
            return f"{rate}%"

    successrate.short_description = "계획 생산량 달성율"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.현재공정 is None:
            self.현재공정 = "예비작업"
            self.현재공정달성율 = "0%"


class WorkOrder(TimeStampedModel):
    생산계획 = "생산계획"
    AS = "AS"

    수리생산_CHOICES = (
        (생산계획, "생산계획"),
        (AS, "AS"),
    )

    생산계획 = models.OneToOneField(
        "ProduceRegister",
        related_name="작업지시서",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수리생산 = models.CharField(
        choices=수리생산_CHOICES, max_length=10, default=생산계획, null=True
    )
    작업지시코드 = models.CharField(max_length=30, null=True)
    수량 = models.IntegerField(null=True)
    특이사항 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "작업지시서"
        verbose_name_plural = "작업지시서"

    def __str__(self):
        return f" '{self.생산계획}' 의 작업지시서 : {self.작업지시코드}"


class WorkOrderRegister(TimeStampedModel):

    작업지시서 = models.OneToOneField(
        "WorkOrder", related_name="작업지시서등록", on_delete=models.SET_NULL, null=True,
    )
    생산담당자 = models.ForeignKey(
        users_models.User, related_name="작업지시서등록", on_delete=models.SET_NULL, null=True,
    )
    생산일시 = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=timezone.now().date(),
        blank=True,
        null=True,
    )
    생산수량 = models.IntegerField(null=True)
    특이사항 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "작업지시서등록"
        verbose_name_plural = "작업지시서등록"

    def __str__(self):
        return f" '{self.작업지시서}' 의 작업지시서 등록"


class MonthlyProduceList(TimeStampedModel):

    단품모델 = models.OneToOneField(
        SI_models.SingleProduct,
        related_name="월별생산계획",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    수량 = models.IntegerField(null=True)
    작성자 = models.ForeignKey(
        users_models.User, related_name="월별생산계획", on_delete=models.SET_NULL, null=True,
    )
    작성일 = models.DateField(auto_now=False, auto_now_add=False, null=True)

    class Meta:
        verbose_name = "월별생산계획"
        verbose_name_plural = "월별생산계획"

    def __str__(self):
        return f" 월별생산계획 : {self.단품모델} {self.수량}{self.단품모델.단위}  <{self.작성자}>"
