from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models


class ASRegisters(TimeStampedModel):
    접수제품분류_CHOICES = (
        ("단품", "단품"),
        ("랙", "랙"),
    )

    비용_CHOICES = (
        ("유상", "유상"),
        ("무상", "무상"),
    )

    처리방법_CHOICES = (
        ("내부처리", "내부처리"),
        ("현장방문", "현장방문"),
        ("접수보류", "접수보류"),
        ("접수취소", "접수취소"),
        ("택배수령", "택배수령"),
    )

    접수번호 = models.CharField(max_length=20, null=True,)
    접수일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    설치연도 = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )  # 패치부분

    접수자 = models.ForeignKey(
        users_models.User, related_name="AS등록", on_delete=models.SET_NULL, null=True
    )
    접수내용 = models.CharField(max_length=100, null=True)
    현장명 = models.CharField(max_length=50, null=True)
    주소 = models.TextField(max_length=120, null=True, blank=True)
    의뢰자전화번호 = models.CharField(max_length=20, null=True, blank=True)
    비용 = models.CharField(choices=비용_CHOICES, max_length=10, default="유상")
    비고 = models.CharField(max_length=100, null=True)
    첨부파일 = models.FileField(blank=True, null=True, upload_to="ASregister")
    처리방법 = models.CharField(
        choices=처리방법_CHOICES, max_length=10, default="담당자연결", blank=False, null=True,
    )

    class Meta:
        verbose_name = "AS접수"
        verbose_name_plural = "AS접수"

    def __str__(self):
        return f"{self.접수번호} : AS접수 -'{self.접수자}'"

    def process(self):
        try:
            self.AS현장방문
            try:
                self.AS현장방문.AS재방문
                try:
                    self.AS현장방문.AS재방문.AS완료
                    return "AS완료"

                except:
                    if self.AS현장방문.AS재방문.현장택배 == "현장":
                        return "수리/교체후AS현장방문"
                    else:
                        return "수리/교체후AS택배송부"

            except:
                try:
                    self.AS현장방문.AS완료
                    return "AS완료"
                except:
                    if self.처리방법 == "현장방문":
                        return "현장방문완료"
                    else:
                        return "택배수령완료"
        except:
            try:
                self.AS완료
                return "AS완료"
            except:
                return "AS접수완료"


class ASVisitContents(TimeStampedModel):

    AS방법_CHOICES = (
        ("수리의뢰", "수리의뢰"),
        ("자체수리", "자체수리"),
        ("제품교체", "제품교체"),
        ("기타", "기타"),
    )

    처리방법_CHOICES = (
        ("자체", "자체"),
        ("외주", "외주"),
    )

    견적진행여부_CHOICES = (
        ("Yes", "Yes"),
        ("No", "No"),
    )

    AS접수 = models.OneToOneField(
        "ASRegisters", related_name="AS현장방문", on_delete=models.SET_NULL, null=True
    )
    AS날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    AS방법 = models.CharField(
        choices=AS방법_CHOICES, max_length=10, null=True, blank=False, default="기타"
    )
    처리방법 = models.CharField(
        choices=처리방법_CHOICES, max_length=10, null=True, blank=False, default="자체"
    )
    처리기사 = models.CharField(max_length=50, null=True, blank=True)
    견적진행여부 = models.CharField(
        choices=견적진행여부_CHOICES, max_length=10, null=True, blank=False, default="Yes"
    )
    견적서첨부 = models.FileField(blank=True, null=True, upload_to="cost")
    특이사항 = models.TextField(null=True, blank=True)
    첨부파일 = models.FileField(blank=True, null=True, upload_to="ASVisitContents")
    입력자 = models.ForeignKey(
        users_models.User, related_name="AS현장방문", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "AS현장방문"
        verbose_name_plural = "AS현장방문"

    def __str__(self):
        return f"{self.AS접수.접수번호} : AS현장방문 -'{self.AS접수.접수자}'"

    def repair_count(self):
        return len(self.AS수리요청.all())

    def singleout_count(self):
        return len(self.단품출하요청.all())


class ASRepairRequest(TimeStampedModel):
    택배관련_CHOICES = (
        ("선불", "선불"),
        ("착불", "착불"),
    )

    수리요청코드 = models.CharField(max_length=50, null=True, blank=True,)

    AS현장방문 = models.ForeignKey(
        "ASVisitContents", related_name="AS수리요청", on_delete=models.SET_NULL, null=True
    )
    신청자 = models.ForeignKey(
        users_models.User, related_name="AS수리요청", on_delete=models.SET_NULL, null=True
    )
    신청품목 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="AS수리요청",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    고객성명 = models.CharField(max_length=50, null=True, blank=True,)
    고객주소 = models.CharField(max_length=120, null=True, blank=True,)
    고객전화 = models.CharField(max_length=50, null=True, blank=True,)
    고객팩스 = models.CharField(max_length=50, null=True, blank=True,)
    AS의뢰내용 = models.CharField(max_length=50, null=True, blank=True,)
    시리얼번호 = models.CharField(max_length=50, null=True, blank=True,)
    사용자액세서리 = models.CharField(max_length=50, null=True, blank=True,)
    택배관련 = models.CharField(choices=택배관련_CHOICES, max_length=10, default="선불")
    신청수량 = models.IntegerField()

    class Meta:
        verbose_name = "AS수리요청"
        verbose_name_plural = "AS수리요청"

    def __str__(self):
        return f"{self.AS현장방문.AS접수.접수번호} : AS수리요청 -'{self.AS현장방문.AS접수}' : {self.신청품목}({self.신청수량}) "

    def process(self):
        try:
            self.수리내역서
            return "수리완료"
        except:
            return "수리요청완료"


class ASReVisitContents(TimeStampedModel):

    현장택배_CHOICES = (
        ("현장", "현장"),
        ("택배", "택배"),
    )
    AS방법_CHOICES = (
        ("제품수리", "제품수리"),
        ("제품교체", "제품교체"),
        ("기타", "기타"),
    )

    전AS현장방문 = models.OneToOneField(
        "ASVisitContents", related_name="AS재방문", on_delete=models.SET_NULL, null=True
    )
    AS날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    AS방법 = models.CharField(choices=AS방법_CHOICES, max_length=10, default="제품수리")
    현장명 = models.CharField(max_length=50, null=True)
    AS처리내역 = models.TextField(null=True)
    특이사항 = models.TextField(null=True, blank=True)
    수리기사 = models.ForeignKey(
        users_models.User, related_name="AS재방문", on_delete=models.SET_NULL, null=True
    )
    현장택배 = models.CharField(
        choices=현장택배_CHOICES, max_length=10, blank=True, default="현장"
    )

    class Meta:
        verbose_name = "AS재현장방문"
        verbose_name_plural = "AS재현장방문"

    def __str__(self):
        return f"{self.전AS현장방문.AS접수.접수번호} : AS재방문 -'{self.전AS현장방문.AS접수.접수자}'"


class ASResults(TimeStampedModel):
    완료유형_CHOICES = (
        ("내부처리", "내부처리"),
        ("담당자내부처리", "담당자내부처리"),
        ("방문", "방문"),
        ("재방문", "재방문"),
    )

    내부처리 = models.OneToOneField(
        "ASRegisters",
        related_name="AS완료",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    방문 = models.OneToOneField(
        "ASVisitContents",
        related_name="AS완료",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    재방문 = models.OneToOneField(
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
    처리내용 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "AS완료"
        verbose_name_plural = "AS완료"

    def __str__(self):

        if self.완료유형 == "재방문":
            return f"{self.재방문.전AS현장방문.AS접수.접수번호} : AS완료(재방문) -'{self.재방문.전AS현장방문.AS접수.접수자}'"
        elif self.완료유형 == "방문":
            return f"{self.방문.AS접수.접수번호} : AS완료(방문) -'{self.방문.AS접수.접수자}'"
        elif self.완료유형 == "담당자내부처리":
            return (
                f"{self.담당자내부처리.AS접수.접수번호} : AS완료(담당자내부처리) -'{self.담당자내부처리.AS접수.접수자}'"
            )

        else:
            return f"{self.내부처리.접수번호} : AS완료(내부처리) - '{self.내부처리.접수자}'"
