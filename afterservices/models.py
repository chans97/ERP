from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models


class ASRegisters(TimeStampedModel):
    단품 = "단품"
    랙 = "랙"

    접수제품분류_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

    내부처리 = "내부처리"
    담당자연결 = "담당자연결"

    대응유형_CHOICES = (
        (내부처리, "내부처리"),
        (담당자연결, "담당자연결"),
    )

    비용_CHOICES = (
        ("유상", "유상"),
        ("무상", "무상"),
    )

    인계후_CHOICES = (
        (내부처리, "내부처리"),
        ("현장방문", "현장방문"),
        ("접수보류", "접수보류"),
        ("접수취소", "접수취소"),
    )

    사용법미숙지 = "사용법미숙지"
    랙구성케이블오류 = "랙구성케이블오류"
    단품불량 = "단품불량"

    접수번호 = models.CharField(max_length=20, null=True,)
    접수일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    접수자 = models.ForeignKey(
        users_models.User, related_name="AS등록", on_delete=models.SET_NULL, null=True
    )
    현상 = models.CharField(max_length=100, null=True,)
    불량분류코드 = models.CharField(max_length=20, null=True,)
    불량분류 = models.CharField(max_length=30)
    접수제품분류 = models.CharField(choices=접수제품분류_CHOICES, max_length=10, default=단품)
    현장명 = models.CharField(max_length=50, null=True,)
    인계후 = models.CharField(choices=인계후_CHOICES, max_length=10, default="", null=True,)

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
        choices=대응유형_CHOICES, max_length=10, default=담당자연결, blank=True, null=True,
    )
    비용 = models.CharField(choices=비용_CHOICES, max_length=10, default="유상")
    의뢰처 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="AS등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    의뢰자전화번호 = models.CharField(max_length=20, null=True, blank=True)
    방문요청일 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = "AS접수"
        verbose_name_plural = "AS접수"

    def __str__(self):
        return f"{self.접수번호} : AS접수 -'{self.의뢰처}'"

    def process(self):
        try:
            self.AS현장방문요청
            try:
                self.AS현장방문요청.AS현장방문
                try:
                    self.AS현장방문요청.AS현장방문.AS재방문
                    try:
                        self.AS현장방문요청.AS현장방문.AS재방문.AS완료
                        return "AS완료"

                    except:
                        return "재방문완료"

                except:
                    try:
                        self.AS현장방문요청.AS현장방문.AS완료
                        return "AS완료"
                    except:
                        return "현장방문완료"

            except:
                try:
                    self.AS현장방문요청.AS완료
                    return "AS완료"
                except:
                    return "AS담당부 인계완료"

        except:
            try:
                self.AS완료
                return "AS완료"
            except:
                return "AS접수완료"


class ASVisitRequests(TimeStampedModel):
    AS접수 = models.OneToOneField(
        ASRegisters,
        related_name="AS현장방문요청",
        on_delete=models.CASCADE,
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
        return f"{self.AS접수.접수번호} : AS현장방문요청 -'{self.AS접수.의뢰처}'"


class ASVisitContents(TimeStampedModel):

    단품 = "단품"
    랙 = "랙"

    접수제품분류_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

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
        ("견적진행", "견적진행"),
    )
    AS현장방문요청 = models.OneToOneField(
        "ASVisitRequests", related_name="AS현장방문", on_delete=models.SET_NULL, null=True
    )
    AS날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    AS방법 = models.CharField(choices=AS방법_CHOICES, max_length=10, default=제품수리)
    고객이름 = models.CharField(max_length=50, null=True, blank=True)
    처리기사 = models.CharField(max_length=50, null=True, blank=True)
    처리회사 = models.CharField(max_length=50, null=True, blank=True)
    AS처리내역 = models.TextField(null=True)
    특이사항 = models.TextField(null=True, blank=True)
    재방문여부 = models.CharField(choices=재방문여부_CHOICES, max_length=10, default=완료)
    수리기사 = models.ForeignKey(
        users_models.User, related_name="AS현장방문", on_delete=models.SET_NULL, null=True
    )
    접수제품분류 = models.CharField(
        choices=접수제품분류_CHOICES, max_length=10, blank=True, default=단품
    )
    하자파일 = models.FileField(blank=True, null=True, upload_to="bad")
    견적서 = models.FileField(blank=True, null=True, upload_to="cost")
    단품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="AS현장방문",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    랙 = models.ForeignKey(
        SI_models.RackProduct,
        related_name="AS현장방문",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "AS현장방문"
        verbose_name_plural = "AS현장방문"

    def __str__(self):
        return f"{self.AS현장방문요청.AS접수.접수번호} : AS현장방문 -'{self.AS현장방문요청.AS접수.의뢰처}'"

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
        return f"{self.AS현장방문.AS현장방문요청.AS접수.접수번호} : AS수리요청 -'{self.AS현장방문.AS현장방문요청.AS접수.의뢰처}' : {self.신청품목}({self.신청수량}) "

    def process(self):
        try:
            self.수리내역서
            return "수리완료"
        except:
            return "수리요청완료"


class ASReVisitContents(TimeStampedModel):
    단품 = "단품"
    랙 = "랙"

    접수제품분류_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

    제품수리 = "제품수리"
    제품교체 = "제품교체"
    기타 = "기타"

    AS방법_CHOICES = (
        (제품수리, "제품수리"),
        (제품교체, "제품교체"),
        (기타, "기타"),
    )

    전AS현장방문 = models.OneToOneField(
        "ASVisitContents", related_name="AS재방문", on_delete=models.SET_NULL, null=True
    )
    AS날짜 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    AS방법 = models.CharField(choices=AS방법_CHOICES, max_length=10, default=제품수리)
    고객이름 = models.CharField(max_length=50, null=True)
    AS처리내역 = models.TextField(null=True)
    특이사항 = models.TextField(null=True, blank=True)
    수리기사 = models.ForeignKey(
        users_models.User, related_name="AS재방문", on_delete=models.SET_NULL, null=True
    )
    접수제품분류 = models.CharField(
        choices=접수제품분류_CHOICES, max_length=10, blank=True, default=단품
    )

    단품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="AS재방문",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    랙 = models.ForeignKey(
        SI_models.RackProduct,
        related_name="AS재방문",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "AS재현장방문"
        verbose_name_plural = "AS재현장방문"

    def __str__(self):
        return f"{self.전AS현장방문.AS현장방문요청.AS접수.접수번호} : AS재방문 -'{self.전AS현장방문.AS현장방문요청.AS접수.의뢰처}'"


class ASResults(TimeStampedModel):
    내부처리 = "내부처리"
    방문 = "방문"
    재방문 = "재방문"

    완료유형_CHOICES = (
        (내부처리, "내부처리"),
        ("담당자내부처리", "담당자내부처리"),
        (방문, "방문"),
        (재방문, "재방문"),
    )

    내부처리 = models.OneToOneField(
        "ASRegisters",
        related_name="AS완료",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    담당자내부처리 = models.OneToOneField(
        "ASVisitRequests",
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
            return f"{self.재방문.전AS현장방문.AS현장방문요청.AS접수.접수번호} : AS완료(재방문) -'{self.재방문.전AS현장방문.AS현장방문요청.AS접수.의뢰처}'"
        elif self.완료유형 == "방문":
            return f"{self.방문.AS현장방문요청.AS접수.접수번호} : AS완료(방문) -'{self.방문.AS현장방문요청.AS접수.의뢰처}'"
        elif self.완료유형 == "담당자내부처리":
            return (
                f"{self.담당자내부처리.AS접수.접수번호} : AS완료(담당자내부처리) -'{self.담당자내부처리.AS접수.의뢰처}'"
            )

        else:
            return f"{self.내부처리.접수번호} : AS완료(내부처리) - '{self.내부처리.의뢰처}'"
