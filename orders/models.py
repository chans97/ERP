from django.db import models
from core.models import TimeStampedModel
from StandardInformation import models as SI_models


class OrderRegister(TimeStampedModel):

    입찰 = "입찰"
    대리점 = "대리점"
    AS = "A/S"
    내부계획 = "내부계획"

    영업구분_CHOICES = ((입찰, "입찰"), (대리점, "대리점"), (AS, "A/S"), (내부계획, "내부계획"))

    삼형전자 = "삼형전자"
    엠에스텔레콤 = "엠에스텔레콤"

    사업장구분_CHOICES = (
        (삼형전자, "삼형전자"),
        (엠에스텔레콤, "엠에스텔레콤"),
    )

    단품 = "단품"
    랙 = "랙"

    제품구분_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

    수주코드 = models.CharField(max_length=50)
    영업구분 = models.CharField(choices=영업구분_CHOICES, max_length=10, blank=True, default=입찰)
    제품구분 = models.CharField(choices=제품구분_CHOICES, max_length=10, blank=True, default=단품)
    사업장구분 = models.CharField(
        choices=사업장구분_CHOICES, max_length=10, blank=True, default=삼형전자
    )
    수주일자 = models.DateField(auto_now=False, auto_now_add=False)
    고객사명 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    현장명 = models.CharField(max_length=50)
    납품요청일 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    납품수량 = models.IntegerField()
    특이사항 = models.TextField(blank=True)
    단품모델 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    랙모델 = models.ForeignKey(
        SI_models.RackProduct,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "수주등록"
        verbose_name_plural = "수주등록"

    def __str__(self):
        if self.고객사명 is None:
            return f"{self.수주코드}"

        else:
            return f"{self.고객사명}의 수주 : {self.수주코드}"


class OrderProduce(TimeStampedModel):

    일반 = "일반"
    긴급 = "긴급"

    긴급도_CHOICES = (
        (일반, "일반"),
        (긴급, "긴급"),
    )

    생산의뢰수주 = models.ForeignKey(
        "OrderRegister",
        related_name="생산요청",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    생산의뢰코드 = models.CharField(max_length=50)

    긴급도 = models.CharField(choices=긴급도_CHOICES, max_length=10, blank=True, default=일반)
    생산목표수량 = models.IntegerField()

    class Meta:
        verbose_name = "생산의뢰등록"
        verbose_name_plural = "생산의뢰등록"

    def __str__(self):
        return f" '{self.생산의뢰수주.수주코드}' 의 생산의뢰 : {self.생산의뢰코드}"

