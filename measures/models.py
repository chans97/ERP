from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models


class MeasureCheckRegister(TimeStampedModel):
    계측기 = models.ForeignKey(SI_models.Measure, on_delete=models.CASCADE)
    점검자 = models.ForeignKey(
        users_models.User, related_name="계측기점검등록", on_delete=models.SET_NULL, null=True
    )
    점검일 = models.DateField(auto_now=False, auto_now_add=False)
    점검내용 = models.CharField(max_length=100)
    특이사항 = models.TextField()

    class Meta:
        verbose_name = "계측기점검등록"
        verbose_name_plural = "계측기점검등록"

    def __str__(self):

        return f"{self.계측기} 점검 <{self.점검일}>"


class MeasureRepairRegister(TimeStampedModel):
    계측기 = models.ForeignKey(SI_models.Measure, on_delete=models.CASCADE)
    수리자 = models.ForeignKey(
        users_models.User, related_name="계측기수리등록", on_delete=models.SET_NULL, null=True
    )
    수리일 = models.DateField(auto_now=False, auto_now_add=False)
    수리부문 = models.CharField(max_length=100)
    수리내용 = models.CharField(max_length=100)
    file = models.ImageField(
        upload_to="images", blank=True, null=True, help_text="계측기수리 사진을 첨부해주세요."
    )
    특이사항 = models.TextField()

    class Meta:
        verbose_name = "계측기수리등록"
        verbose_name_plural = "계측기수리등록"

    def __str__(self):
        return f"{self.계측기} 수리 <{self.수리일}>"

