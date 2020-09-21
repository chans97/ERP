from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models
from producemanages import models as proms_models
from afterservices import models as AS_models
from django.utils import timezone


class FinalCheck(TimeStampedModel):
    작업지시서 = models.OneToOneField(
        proms_models.WorkOrderRegister,
        related_name="최종검사",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수리내역서 = models.OneToOneField(
        "RepairRegister",
        related_name="최종검사",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    제품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="최종검사",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "최종검사"
        verbose_name_plural = "최종검사"

    def __str__(self):
        if self.작업지시서 is None:
            return f"수리완료-{self.수리내역서}"

        else:

            return f" '{self.작업지시서}' 의 최종검사의뢰 "


class FinalCheckRegister(TimeStampedModel):

    OK = "OK"
    NO = "NO"

    OKNO_CHOICES = (
        (OK, "OK"),
        (NO, "NO"),
    )
    있음 = "있음"
    없음 = "없음"

    있음없음_CHOICES = (
        (있음, "있음"),
        (없음, "없음"),
    )

    전원전압_CHOICES = (
        ("DC 24V", "DC 24V"),
        ("AC 220V", "AC 220V"),
    )

    POWERTRANS_CHOICES = (
        ("T-EPD2083-01", "T-EPD2083-01"),
        ("T-EPB2032-01", "T-EPB2032-01"),
        ("T-EPA2403-01", "T-EPA2403-01"),
        ("T-EPA2243-01", "T-EPA2243-01"),
        ("T-EPA2123-01", "T-EPA2123-01"),
        ("T-EWA2240-01", "T-EWA2240-01"),
        ("EWA2120-01", "EWA2120-01"),
        ("R-EWA2360-01", "R-EWA2360-01"),
    )

    FUSE_전_ULUSA_CHOICES = (
        ("31.8mm 1A", "31.8mm 1A"),
        ("31.8mm 2A", "31.8mm 2A"),
        ("31.8mm 3A", "31.8mm 3A"),
        ("31.8mm 4A", "31.8mm 4A"),
        ("31.8mm 5A", "31.8mm 5A"),
        ("31.8mm 10A", "31.8mm 10A"),
        ("31.8mm 15A", "31.8mm 15A"),
        ("20mm 2A", "20mm 2A"),
        ("20mm 3.15A", "20mm 3.15A"),
        ("20mm 5A", "20mm 5A"),
    )

    LABEL_인쇄물_CHOICES = (
        ("후면 좌측", "후면 좌측"),
        ("후면 우측", "후면 우측"),
        ("후면 중심", "후면 중심"),
        ("후면 우측아래", "후면 우측아래"),
        ("후면 좌측아래", "후면 좌측아래"),
    )

    수리비_CHOICES = (
        ("무상", "무상"),
        ("유상", "유상"),
    )

    택배_CHOICES = (
        ("선불", "선불"),
        ("신용", "신용"),
        ("착불", "착불"),
    )

    최종검사코드 = models.CharField(max_length=20, null=True, blank=True,)
    최종검사의뢰 = models.OneToOneField(
        "FinalCheck", related_name="최종검사등록", on_delete=models.SET_NULL, null=True,
    )
    검시자 = models.ForeignKey(
        users_models.User, related_name="최종검사등록", on_delete=models.SET_NULL, null=True,
    )
    검시일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    치명적불량 = models.CharField(max_length=20, null=True,)
    중불량 = models.CharField(max_length=20, null=True,)
    경불량 = models.CharField(max_length=20, null=True,)
    검사수준 = models.CharField(max_length=40, null=True,)
    샘플링방식 = models.CharField(max_length=20, null=True,)
    결점수 = models.CharField(max_length=20, null=True,)
    전원전압 = models.CharField(
        choices=전원전압_CHOICES, max_length=20, null=True, default="DC 24V"
    )
    POWERTRANS = models.CharField(
        choices=POWERTRANS_CHOICES, max_length=20, null=True, default="T-EPD2083-01",
    )
    FUSE_전_ULUSA = models.CharField(
        choices=FUSE_전_ULUSA_CHOICES, max_length=20, null=True, default="31.8mm 1A",
    )
    LABEL_인쇄물 = models.CharField(
        choices=LABEL_인쇄물_CHOICES, max_length=20, null=True, default="후면 좌측",
    )
    기타출하위치 = models.CharField(max_length=50, null=True, blank=True,)
    내용물 = models.CharField(choices=있음없음_CHOICES, max_length=20, null=True, default="있음")
    포장검사 = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    동작검사 = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    내부검사 = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    외관검사 = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    내압검사_DC = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    내압검사_AC = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    내용물확인 = models.CharField(
        choices=OKNO_CHOICES, max_length=20, null=True, default="OK"
    )
    가_감전압 = models.CharField(max_length=50, blank=True, null=True)
    HI_POT_내부검사 = models.CharField(max_length=50, blank=True, null=True)
    특이사항 = models.TextField(max_length=80, blank=True, null=True)
    부적합수량 = models.IntegerField(null=True)
    적합수량 = models.IntegerField(null=True)
    제품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="최종검사등록",
        on_delete=models.SET_NULL,
        null=True,
    )
    동작이상유무 = models.CharField(max_length=100, null=True, blank=True)
    외형이상유무 = models.CharField(max_length=100, null=True, blank=True)

    수리내역 = models.CharField(max_length=100, null=True, blank=True)
    특기사항 = models.CharField(max_length=100, null=True, blank=True)
    수리자 = models.ForeignKey(
        users_models.User,
        related_name="AS총괄장수리",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수리비 = models.CharField(choices=수리비_CHOICES, max_length=100, blank=True, null=True)
    기본요금 = models.IntegerField(null=True, blank=True)
    부품비 = models.IntegerField(null=True, blank=True)
    택배 = models.CharField(choices=택배_CHOICES, max_length=100, blank=True, null=True)
    화물 = models.CharField(max_length=100, null=True, blank=True)
    발송날짜 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    발송자 = models.ForeignKey(
        users_models.User,
        related_name="AS총괄장발송",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    입금확인 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    비고 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "최종검사결과등록"
        verbose_name_plural = "최종검사결과등록"

    def __str__(self):
        return f" '{self.최종검사코드}' 의 최종검사결과"


class RepairRegister(TimeStampedModel):
    최종검사결과 = "최종검사결과"
    AS = "AS"

    수리최종_CHOICES = (
        (최종검사결과, "최종검사결과"),
        (AS, "AS"),
    )
    최종검사결과 = models.ManyToManyField(
        "FinalCheckRegister", related_name="수리내역서", null=True,
    )
    AS수리의뢰 = models.OneToOneField(
        AS_models.ASRepairRequest,
        related_name="수리내역서",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수리최종 = models.CharField(
        choices=수리최종_CHOICES, max_length=10, default=최종검사결과, null=True, blank=True,
    )
    작성자 = models.ForeignKey(
        users_models.User, related_name="수리내역서", on_delete=models.SET_NULL, null=True
    )
    불량위치및자재 = models.TextField(max_length=300, null=True,)
    특이사항 = models.TextField(max_length=300, null=True, blank=True,)
    수리내용 = models.TextField(max_length=300, null=True, blank=True,)
    실수리수량 = models.IntegerField(null=True,)
    폐기수량 = models.IntegerField(null=True,)
    제품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="수리내역서",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "수리내역서"
        verbose_name_plural = "수리내역서"

    def __str__(self):
        if self.수리최종 == "최종검사결과":
            return f"수리내역서 -'{self.최종검사결과}'"
        else:
            return f"수리내역서 -'{self.AS수리의뢰}'"

    def finalcheckboolean(self):
        try:
            self.최종검사
            try:
                self.최종검사.최종검사등록
                return "최종검사완료"
            except:
                return "최종검사의뢰완료"
        except:
            return "수리완료"


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

    def process(self):
        try:
            self.수입검사
            return "수입검사완료"
        except:
            return "수입검사요청완료"


class MaterialCheck(TimeStampedModel):

    판정기준_CHOICES = (
        ("AC 0", "AC 0"),
        ("Re 1", "Re 1"),
    )

    수입검사코드 = models.CharField(max_length=20)
    수입검사의뢰 = models.OneToOneField(
        "MaterialCheckRegister",
        related_name="수입검사",
        on_delete=models.SET_NULL,
        null=True,
    )
    검사지침서 = models.CharField(max_length=100, null=True, blank=True,)
    검사자 = models.ForeignKey(
        users_models.User, related_name="수입검사", on_delete=models.SET_NULL, null=True
    )
    검사일자 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    검사항목 = models.CharField(max_length=20, null=True, blank=True,)
    판정기준 = models.CharField(max_length=20, null=True, blank=True, default="AC=0, RE=1")
    시료크기 = models.IntegerField()
    적합수량 = models.IntegerField()
    부적합수량 = models.IntegerField()
    부적합내용 = models.TextField(max_length=100, null=True, blank=True,)
    자재 = models.ForeignKey(
        SI_models.Material, related_name="수입검사", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "수입검사"
        verbose_name_plural = "수입검사"

    def __str__(self):
        return f"수입검사 -'{self.수입검사의뢰.자재}'"

    def process(self):
        try:
            self.자재부적합보고서
            return "자재부적합등록완료"
        except:
            return "수입검사등록완료"


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

    자재부적합코드 = models.CharField(max_length=20)
    수입검사 = models.OneToOneField(
        "MaterialCheck", related_name="자재부적합보고서", on_delete=models.SET_NULL, null=True
    )
    검토자 = models.ForeignKey(
        users_models.User, related_name="자재부적합보고서", on_delete=models.SET_NULL, null=True
    )
    검토일 = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        default=timezone.now().date(),
        null=True,
    )
    부적합자재의내용과검토방안 = models.TextField(max_length=150, null=True, blank=True,)
    처리방안 = models.CharField(choices=처리방안_CHOICES, max_length=10, default=기타, null=True,)
    자재 = models.ForeignKey(
        SI_models.Material,
        related_name="자재부적합보고서",
        on_delete=models.SET_NULL,
        null=True,
    )
    첨부파일 = models.FileField(blank=True, null=True, upload_to="lowmaterial")

    class Meta:
        verbose_name = "자재부적합보고서"
        verbose_name_plural = "자재부적합보고서"

    def __str__(self):
        return f"자재부적합보고서 -'{self.자재부적합코드}'"
