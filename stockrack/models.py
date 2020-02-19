from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models
from producemanages import models as proms_models
from stocksingle import models as SS_models
from stockmanages import models as SM_models


class StockOfRackProductOutRequest(TimeStampedModel):
    수주 = models.ForeignKey(
        orders_models.OrderRegister,
        related_name="랙출하요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    랙 = models.ForeignKey(
        SI_models.RackProduct,
        related_name="랙출하요청",
        on_delete=models.CASCADE,
        null=True,
    )
    고객사 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="랙출하요청",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    출하요청수량 = models.IntegerField()
    출하요청자 = models.ForeignKey(
        users_models.User, related_name="랙출하요청", on_delete=models.SET_NULL, null=True,
    )
    출하요청일 = models.DateField(auto_now=False, auto_now_add=True)
    출하희망일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = "랙출하요청"
        verbose_name_plural = "랙출하요청"

    def __str__(self):
        return f"<랙출하요청>{self.랙} : {self.출하요청수량} {self.랙.단위}"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        print("it gogogoo")

    def save(self, *args, **kwargs):
        if self.id:
            print(bool(self.id))
        else:
            for com in self.랙.랙구성단품.all():
                if com.랙구성 == "자재":
                    num = com.수량
                    single = com.랙구성자재
                    출하요청자재수량 = num * self.출하요청수량
                    try:
                        single.자재재고.출고요청제외수량 -= 출하요청자재수량
                        single.자재재고.save()
                        print("Sgood")
                    except:
                        SM_models.StockOfMaterial.objects.create(
                            자재=single, 출고요청제외수량=-출하요청단품수량
                        )
                else:
                    num = com.수량
                    single = com.랙구성단품
                    출하요청단품수량 = num * self.출하요청수량
                    print(single)
                    try:
                        single.단품재고.출하요청제외수량 -= 출하요청단품수량
                        single.단품재고.save()
                    except:
                        SS_models.StockOfSingleProduct.objects.create(
                            단품=single, 출하요청제외수량=-출하요청단품수량
                        )

        super().save(*args, **kwargs)

    def unexport(self):
        try:
            self.랙출하등록
            return False
        except:
            return True


class StockOfRackProductOut(TimeStampedModel):

    랙출하요청 = models.OneToOneField(
        "StockOfRackProductOutRequest",
        related_name="랙출하등록",
        on_delete=models.CASCADE,
        null=True,
    )
    SI_models.CustomerPartner
    출하자 = models.ForeignKey(
        users_models.User, related_name="랙출하등록", on_delete=models.SET_NULL, null=True,
    )
    출하일 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    출하수량 = models.IntegerField(null=True)
    거래명세서첨부 = models.FileField(
        upload_to="deal", blank=True, null=True, help_text="거래명세서를 첨부해주세요."
    )

    class Meta:
        verbose_name = "랙출하등록"
        verbose_name_plural = "랙출하등록"

    def __str__(self):
        return f"{self.랙출하요청.랙} : {self.출하수량} {self.랙출하요청.랙.단위}"

    def save(self, *args, **kwargs):

        try:
            for com in self.랙출하요청.랙.랙구성단품.all():
                if com.랙구성 == "자재":
                    num = com.수량
                    single = com.랙구성자재
                    출하자재수량 = num * self.출하수량
                    출하요청자재수량 = num * self.랙출하요청.출하요청수량
                    single.자재재고.실수량 -= 출하자재수량
                    차이 = 출하요청자재수량 - 출하자재수량
                    single.자재재고.출고요청제외수량 += 차이
                    single.자재재고.입고요청포함수량 -= 출하자재수량
                    single.자재재고.save()
                else:
                    num = com.수량
                    single = com.랙구성단품
                    출하단품수량 = num * self.출하수량
                    출하요청단품수량 = num * self.랙출하요청.출하요청수량
                    single.단품재고.실수량 -= 출하단품수량
                    차이 = 출하요청단품수량 - 출하단품수량
                    single.단품재고.출하요청제외수량 += 차이
                    single.단품재고.입고요청포함수량 -= 출하단품수량
                    single.단품재고.save()
        except:
            pass
        super().save(*args, **kwargs)
