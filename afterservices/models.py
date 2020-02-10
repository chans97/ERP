from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models

# Create your models here.
class ASRegisters(TimeStampedModel):
    단품 = "단품"
    랙 = "랙"

    접수제품분류_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

    내부처리 = "내부처리"
    현장방문 = "현장방문"

    대응유형_CHOICES = (
        (내부처리, "내부처리"),
        (현장방문, "현장방문"),
    )

    사용법미숙지 = "사용법미숙지"
    랙구성케이블오류 = "랙구성케이블오류"
    단품불량 = "단품불량"

    불량분류_CHOICES = (
        (사용법미숙지, "사용법미숙지"),
        (랙구성케이블오류, "랙구성케이블오류"),
        (단품불량, "단품불량"),
    )

    접수번호 = models.CharField(max_length=20, null=True,)
    접수일 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    접수자 = models.ForeignKey(
        users_models.User, related_name="AS등록", on_delete=models.SET_NULL, null=True
    )
    현상 = models.CharField(max_length=100, null=True,)
    접수제품분류 = models.CharField(
        choices=접수제품분류_CHOICES, max_length=10, blank=True, default=단품
    )
    불량분류코드 = models.CharField(max_length=20, null=True,)
    불량분류 = models.CharField(
        choices=불량분류_CHOICES, max_length=10, blank=True, default=사용법미숙지
    )
    단품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="AS등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    랙 = models.ForeignKey(
        SI_models.RackProduct,
        related_name="AS등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    대응유형 = models.CharField(
        choices=대응유형_CHOICES, max_length=10, blank=True, default=내부처리
    )
    의뢰처 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="AS등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    의뢰자전화번호 = models.IntegerField(null=True)
    방문요청일 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = "AS접수"
        verbose_name_plural = "AS접수"

    def __str__(self):
        return f"AS접수 -'{self.의뢰처}'"


class ASVisitRequests(TimeStampedModel):
    AS접수 = models.ForeignKey(
        ASRegisters,
        related_name="AS현장방문요청",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    AS담당자 = models.ForeignKey(
        users_models.User, related_name="AS현장방문요청", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "AS현장방문요청"
        verbose_name_plural = "AS현장방문요청"

    def __str__(self):
        return f"AS현장방문요청 -'{self.AS접수.의뢰처}'"


class ASVisitContents(TimeStampedModel):

    제품수리 = "제품수리"
    제품교체 = "제품교체"
    제품취소 = "제품취소"
    기타 = "기타"

    AS방법_CHOICES = (
        (제품수리, "제품수리"),
        (제품교체, "제품교체"),
        (제품취소, "제품취소"),
        (기타, "기타"),
    )

    완료 = "완료"
    재방문 = "재방문"

    재방문여부_CHOICES = (
        (완료, "완료"),
        (재방문, "재방문"),
    )
    AS현장방문요청 = models.ForeignKey(
        "ASVisitRequests", related_name="AS현장방문", on_delete=models.SET_NULL, null=True
    )
    AS날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    AS방법 = models.CharField(
        choices=AS방법_CHOICES, max_length=10, blank=True, default=제품수리
    )
    고객이름 = models.CharField(max_length=50, null=True)
    AS처리내역 = models.TextField(null=True)
    특이사항 = models.TextField(null=True, blank=True)
    재방문여부 = models.CharField(
        choices=재방문여부_CHOICES, max_length=10, blank=True, default=완료
    )

    class Meta:
        verbose_name = "AS현장방문"
        verbose_name_plural = "AS현장방문"

    def __str__(self):
        return f"AS현장방문 -'{self.AS현장방문요청.AS접수.의뢰처}'"


class ASReVisitContents(TimeStampedModel):

    제품수리 = "제품수리"
    제품교체 = "제품교체"
    기타 = "기타"

    AS방법_CHOICES = (
        (제품수리, "제품수리"),
        (제품교체, "제품교체"),
        (기타, "기타"),
    )

    전AS현장방문 = models.ForeignKey(
        "ASVisitContents", related_name="AS재방문", on_delete=models.SET_NULL, null=True
    )
    AS날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    AS방법 = models.CharField(
        choices=AS방법_CHOICES, max_length=10, blank=True, default=제품수리
    )
    고객이름 = models.CharField(max_length=50, null=True)
    AS처리내역 = models.TextField(null=True)
    특이사항 = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "AS재현장방문"
        verbose_name_plural = "AS재현장방문"

    def __str__(self):
        return f"AS재방문 -'{self.전AS현장방문.AS현장방문요청.AS접수.의뢰처}'"


class ASResults(TimeStampedModel):
    내부처리 = "내부처리"
    제품취소 = "제품취소"
    재방문 = "재방문"

    완료유형_CHOICES = (
        (내부처리, "내부처리"),
        (제품취소, "제품취소"),
        (재방문, "재방문"),
    )

    내부처리 = models.ForeignKey(
        "ASRegisters",
        related_name="AS완료",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    제품취소 = models.ForeignKey(
        "ASVisitContents",
        related_name="AS완료",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    재방문 = models.ForeignKey(
        "ASReVisitContents",
        related_name="AS완료",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    완료확인자 = models.ForeignKey(
        users_models.User, related_name="AS완료", on_delete=models.SET_NULL, null=True
    )
    완료날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    완료유형 = models.CharField(choices=완료유형_CHOICES, max_length=10, default=내부처리)

    class Meta:
        verbose_name = "AS완료"
        verbose_name_plural = "AS완료"

    def __str__(self):
        if self.완료유형 == "재방문":
            return f"AS완료(방문) -'{self.재방문.전AS현장방문.AS현장방문요청.AS접수.의뢰처}'"
        elif self.완료유형 == "제품취소":
            return f"AS완료(제품취소) -'{self.제품취소.AS현장방문요청.AS접수.의뢰처}'"
        else:
            return f"AS완료(내부처리) - '{self.내부처리.의뢰처}'"
