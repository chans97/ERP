from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models
from producemanages import models as proms_models
from afterservices import models as AS_models


class FinalCheck(TimeStampedModel):
    작업지시서 = models.ForeignKey(
        proms_models.WorkOrderRegister,
        related_name="최종검사",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수리내역서 = models.ForeignKey(
        "RepairRegister",
        related_name="최종검사",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "최종검사"
        verbose_name_plural = "최종검사"

    def __str__(self):
        if self.작업지시서 is None:
            return f"수리완료-{self.수리내역서.최종검사결과.최종검사의뢰}"

        else:

            return f" '{self.작업지시서.작업지시서.작업지시코드}' 의 최종검사의뢰 "


class FinalCheckRegister(TimeStampedModel):

    OK = "OK"
    NO = "NO"

    OKNO_CHOICES = (
        (OK, "OK"),
        (NO, "NO"),
    )

    최종검사의뢰 = models.ForeignKey(
        "FinalCheck", related_name="최종검사등록", on_delete=models.SET_NULL, null=True,
    )
    검시자 = models.ForeignKey(
        users_models.User, related_name="최종검사등록", on_delete=models.SET_NULL, null=True,
    )
    검시일 = models.DateField(auto_now=False, auto_now_add=False)
    CR = models.CharField(max_length=20, null=True, blank=True,)
    MA = models.CharField(max_length=20, null=True, blank=True,)
    MI = models.CharField(max_length=20, null=True, blank=True,)
    검사수준 = models.CharField(max_length=40, null=True, blank=True,)
    Sample방식 = models.CharField(max_length=20, null=True, blank=True,)
    결점수 = models.CharField(max_length=20, null=True, blank=True,)
    전원전압 = models.CharField(max_length=20, null=True, blank=True,)
    POWERTRANS = models.CharField(max_length=20, null=True, blank=True,)
    FUSE_전_ULUSA = models.CharField(max_length=20, null=True, blank=True,)
    LABEL_인쇄물 = models.CharField(max_length=50, null=True, blank=True,)
    기타출하위치 = models.CharField(max_length=50, null=True, blank=True,)
    내용물 = models.CharField(max_length=50, null=True, blank=True,)
    포장검사 = models.CharField(choices=OKNO_CHOICES, max_length=10, blank=True, default=OK)
    동작검사 = models.CharField(choices=OKNO_CHOICES, max_length=10, blank=True, default=OK)
    내부검사 = models.CharField(choices=OKNO_CHOICES, max_length=10, blank=True, default=OK)
    외관검사 = models.CharField(choices=OKNO_CHOICES, max_length=10, blank=True, default=OK)
    내압검사 = models.CharField(choices=OKNO_CHOICES, max_length=10, blank=True, default=OK)
    내용물확인 = models.CharField(
        choices=OKNO_CHOICES, max_length=10, blank=True, default=OK
    )
    가_감전압 = models.CharField(max_length=50)
    HI_POT_내부검사 = models.CharField(max_length=50)
    REMARK = models.TextField(max_length=80)
    부적합수량 = models.IntegerField()
    적합수량 = models.IntegerField()

    class Meta:
        verbose_name = "최종검사결과등록"
        verbose_name_plural = "최종검사결과등록"

    def __str__(self):
        return f" '{self.최종검사의뢰.작업지시서.작업지시서.작업지시코드}' 의 최종검사결과"


class RepairRegister(TimeStampedModel):
    최종검사결과 = "최종검사결과"
    AS = "AS"

    수리요청_CHOICES = (
        (최종검사결과, "최종검사결과"),
        (AS, "AS"),
    )
    최종검사결과 = models.ForeignKey(
        "FinalCheckRegister",
        related_name="부적합등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    AS수리의뢰 = models.ForeignKey(
        AS_models.ASVisitContents,
        related_name="수리내역서",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수리최종 = models.CharField(
        choices=수리요청_CHOICES, max_length=10, default=최종검사결과, null=True, blank=True,
    )
    불량위치및자재 = models.TextField(max_length=300)
    특이사항 = models.TextField(max_length=300, null=True, blank=True,)
    수리내용 = models.TextField(max_length=300, null=True, blank=True,)
    실수리수량 = models.IntegerField()
    폐기수량 = models.IntegerField()

    class Meta:
        verbose_name = "수리내역서"
        verbose_name_plural = "수리내역서"

    def __str__(self):
        return f"수리내역서 -'{self.최종검사결과}'"


class MaterialCheckRegister(TimeStampedModel):

    수입검사의뢰코드 = models.CharField(max_length=30)
    의뢰자 = models.ForeignKey(
        users_models.User, related_name="수입검사의뢰", on_delete=models.SET_NULL, null=True
    )
    자재 = models.ForeignKey(
        SI_models.Material, related_name="수입검사의뢰", on_delete=models.SET_NULL, null=True
    )
    수량 = models.IntegerField()

    class Meta:
        verbose_name = "수입검사의뢰"
        verbose_name_plural = "수입검사의뢰"

    def __str__(self):
        return f"수입검사의뢰 -'{self.자재}'"


class MaterialCheck(TimeStampedModel):
    수입검사코드 = models.CharField(max_length=20)
    수입검사의뢰 = models.ForeignKey("MaterialCheckRegister", on_delete=models.CASCADE)
    검사지침서번호 = models.CharField(max_length=20)
    검사자 = models.ForeignKey(
        users_models.User, related_name="수입검사", on_delete=models.SET_NULL, null=True
    )
    검사일자 = models.DateField(auto_now=False, auto_now_add=False)
    검사항목 = models.CharField(max_length=20, null=True, blank=True,)
    판정기준 = models.CharField(max_length=20, null=True, blank=True,)
    시료크기 = models.IntegerField()
    합격수량 = models.IntegerField()
    불합격수량 = models.IntegerField()
    불합격내용 = models.TextField(max_length=100, null=True, blank=True,)

    class Meta:
        verbose_name = "수입검사"
        verbose_name_plural = "수입검사"

    def __str__(self):
        return f"수입검사 -'{self.수입검사의뢰.자재}'"


class LowMetarial(TimeStampedModel):
    재작업 = "재작업"
    수리 = "수리"
    특채_수리후 = "특채(수리후)"
    특채_무수리 = "특채(무수리)"
    반품 = "반품"
    폐기 = "폐기"
    기타 = "기타"

    처리방안_CHOICES = (
        (재작업, "재작업"),
        (수리, "수리"),
        (특채_수리후, "특채(수리후)"),
        (특채_무수리, "특채(무수리)"),
        (반품, "반품"),
        (폐기, "폐기"),
        (기타, "기타"),
    )

    자재부적합보고서번호 = models.CharField(max_length=20)
    수입검사 = models.ForeignKey("MaterialCheck", on_delete=models.SET_NULL, null=True)
    검토자 = models.ForeignKey(
        users_models.User, related_name="자재부적합보고서", on_delete=models.SET_NULL, null=True
    )
    검토일 = models.DateField(auto_now=False, auto_now_add=False)
    부적합자재의내용과검토방안 = models.TextField(max_length=150, null=True, blank=True,)
    처리방안 = models.CharField(
        choices=처리방안_CHOICES, max_length=10, default=기타, null=True, blank=True,
    )

    class Meta:
        verbose_name = "자재부적합보고서"
        verbose_name_plural = "자재부적합보고서"

    def __str__(self):
        return f"자재부적합보고서 -'{self.수입검사.수입검사의뢰.자재}'"
