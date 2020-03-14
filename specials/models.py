from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models


class SpecialApplyRegister(TimeStampedModel):
    작성자 = models.ForeignKey(
        users_models.User, related_name="특채신청등록", on_delete=models.SET_NULL, null=True
    )
    작성일 = models.DateField(auto_now=False, auto_now_add=False)
    특채발행번호 = models.CharField(max_length=50)
    특채발행일 = models.DateField(auto_now=False, auto_now_add=False)

    수주 = models.ForeignKey(
        orders_models.OrderRegister,
        related_name="특채신청등록",
        on_delete=models.SET_NULL,
        null=True,
    )
    폐기시손실액 = models.IntegerField()
    특채신청수량 = models.IntegerField()
    불량내용 = models.TextField()
    사용가능사유 = models.TextField()
    특채관련회의록첨부 = models.FileField(blank=True, null=True)
    제품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="특채신청등록",
        on_delete=models.SET_NULL,
        null=True,
    )
    고객사 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="특채신청등록",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "특채신청등록"
        verbose_name_plural = "특채신청등록"

    def __str__(self):

        return f"의 특채신청 : {self.특채발행번호}"

    def process(self):

        try:
            self.특채등록
            try:
                self.특채등록.특채처리
                try:
                    self.특채등록.특채처리.특채반품
                    return "특채반품완료"
                except:
                    return "특채처리완료"
            except:
                return "특채등록완료"
        except:
            return "특채신청완료"


class SpecialRegister(TimeStampedModel):
    특채신청등록 = models.OneToOneField(
        "SpecialApplyRegister", related_name="특채등록", on_delete=models.CASCADE
    )
    특채등록자 = models.ForeignKey(
        users_models.User, related_name="특채등록", on_delete=models.SET_NULL, null=True
    )
    특채등록일 = models.DateField(auto_now=False, auto_now_add=False)
    특채수량 = models.IntegerField()

    class Meta:
        verbose_name = "특채등록"
        verbose_name_plural = "특채등록"

    def __str__(self):

        return f"의 특채 : {self.특채신청등록.특채발행번호}"


class SpecialConductRegister(TimeStampedModel):
    특채 = models.OneToOneField(
        "SpecialRegister", related_name="특채처리", on_delete=models.CASCADE
    )
    특채수량중납품수량 = models.IntegerField()
    작성자 = models.ForeignKey(
        users_models.User, related_name="특채처리", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "특채처리"
        verbose_name_plural = "특채처리"

    def __str__(self):
        return f"의 특채처리 : {self.특채.특채신청등록.특채발행번호}"


class SpecialRejectRegister(TimeStampedModel):
    특채처리 = models.OneToOneField(
        "SpecialConductRegister", related_name="특채반품", on_delete=models.CASCADE
    )
    특채반품수량 = models.IntegerField()
    작성자 = models.ForeignKey(
        users_models.User, related_name="특채반품", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "특채반품"
        verbose_name_plural = "특채반품"

    def __str__(self):
        return f"의 특채반품 : {self.특채처리.특채.특채신청등록.특채발행번호}"
