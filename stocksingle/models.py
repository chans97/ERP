from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models
from afterservices import models as AS_models
from producemanages import models as proms_models
from stockrack import models as SR_models


class StockOfSingleProduct(TimeStampedModel):
    단품 = models.OneToOneField(
        SI_models.SingleProduct, related_name="단품재고", on_delete=models.CASCADE
    )
    실수량 = models.IntegerField(null=True, blank=True, default=0)
    입고요청포함수량 = models.IntegerField(null=True, blank=True, default=0)
    출하요청제외수량 = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = "단품재고"
        verbose_name_plural = "단품재고"

    def __str__(self):
        if self.실수량 is None:
            num = 0
        else:
            num = self.실수량
        return f"{self.단품} : {num} {self.단품.단위}"

    def save(self, *args, **kwargs):
        StockOfSingleProductHistory.objects.create(
            단품=self.단품, 실수량=self.실수량, 입고요청포함수량=self.입고요청포함수량, 출하요청제외수량=self.출하요청제외수량,
        )
        super().save(*args, **kwargs)


class StockOfSingleProductHistory(TimeStampedModel):
    단품 = models.ForeignKey(
        SI_models.SingleProduct, related_name="단품재고기록", on_delete=models.CASCADE
    )
    실수량 = models.IntegerField(null=True, blank=True, default=0)
    입고요청포함수량 = models.IntegerField(null=True, blank=True, default=0)
    출하요청제외수량 = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = "단품재고기록용"
        verbose_name_plural = "단품재고기록용"

    def __str__(self):
        date = f"{self.created.date()}  {self.created.hour}: {self.created.minute}"
        if self.실수량 is None:
            num = 0
        else:
            num = self.실수량
        return f"({date}) {self.단품} : {num} {self.단품.단위}"


class speexceptions(Exception):
    pass


class StockOfSingleProductInRequest(TimeStampedModel):
    수주 = models.ForeignKey(
        orders_models.OrderRegister,
        related_name="단품입고요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    출하요청 = models.ForeignKey(
        "StockOfSingleProductOutRequest",
        related_name="단품입고요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    랙출하요청 = models.ForeignKey(
        SR_models.StockOfRackProductOutRequest,
        related_name="단품입고요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    단품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="단품입고요청",
        on_delete=models.CASCADE,
        null=True,
    )
    입고요청수량 = models.IntegerField()
    입고요청자 = models.ForeignKey(
        users_models.User, related_name="단품입고요청", on_delete=models.SET_NULL, null=True,
    )
    입고요청일 = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "단품입고요청"
        verbose_name_plural = "단품입고요청"

    def __str__(self):
        if self.단품.단품재고.실수량 is not None:
            num = self.단품.단품재고.실수량
            return f"<단품입고요청>{self.단품} : {self.입고요청수량} {self.단품.단위} (현재 수량 : {num})"
        else:
            num = 0
            return f"<단품입고요청>{self.단품} : {self.입고요청수량} {self.단품.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.단품.단품재고.입고요청포함수량 is None:
                self.단품.단품재고.입고요청포함수량 = 0
            self.단품.단품재고.입고요청포함수량 += self.입고요청수량
            self.단품.단품재고.save()
        except:
            StockOfSingleProduct.objects.create(단품=self.단품, 입고요청포함수량=self.입고요청수량)

    def unimport(self):
        try:
            self.단품입고등록
            return False
        except:
            return True

    def process(self):
        try:
            self.단품출하등록
            return "입고완료"
        except:
            return "입고요청완료"


class StockOfSingleProductIn(TimeStampedModel):

    단품입고요청 = models.OneToOneField(
        "StockOfSingleProductInRequest",
        related_name="단품입고등록",
        on_delete=models.CASCADE,
        null=True,
    )
    입고자 = models.ForeignKey(
        users_models.User, related_name="단품입고등록", on_delete=models.SET_NULL, null=True,
    )
    입고일 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    입고수량 = models.IntegerField(null=True)

    class Meta:
        verbose_name = "단품입고등록"
        verbose_name_plural = "단품입고등록"

    def __str__(self):
        num = self.단품입고요청.단품.단품재고.실수량
        return f"{self.단품입고요청.단품} : {self.입고수량} {self.단품입고요청.단품.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.단품입고요청.단품.단품재고.실수량 is None:
                self.단품입고요청.단품.단품재고.실수량 = 0
            if self.단품입고요청.단품.단품재고.출하요청제외수량 is None:
                self.단품입고요청.단품.단품재고.출하요청제외수량 = 0
            self.단품입고요청.단품.단품재고.실수량 += self.입고수량
            차이 = self.단품입고요청.입고요청수량 - self.입고수량
            self.단품입고요청.단품.단품재고.입고요청포함수량 -= 차이
            self.단품입고요청.단품.단품재고.출하요청제외수량 += self.입고수량
            self.단품입고요청.단품.단품재고.save()
        except:
            StockOfSingleProduct.objects.create(
                단품=self.단품입고요청.단품, 실수량=self.입고수량, 입고요청포함수량=self.입고수량
            )


class StockOfSingleProductOutRequest(TimeStampedModel):
    수주AS_CHOICES = (("수주", "수주"), ("AS", "AS"))
    수주AS = models.CharField(
        choices=수주AS_CHOICES, max_length=10, default="수주", null=True, blank=True,
    )

    단품 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="단품출하요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    수주 = models.ForeignKey(
        orders_models.OrderRegister,
        related_name="단품출하요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    AS = models.ForeignKey(
        AS_models.ASVisitContents,
        related_name="단품출하요청",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    고객사 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="단품출하요청",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    출하요청수량 = models.IntegerField()
    출하요청자 = models.ForeignKey(
        users_models.User, related_name="단품출하요청", on_delete=models.SET_NULL, null=True,
    )
    출하요청일 = models.DateField(auto_now=False, auto_now_add=True)
    출하희망일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = "단품출하요청"
        verbose_name_plural = "단품출하요청"

    def __str__(self):
        if self.단품.단품재고.실수량 is not None:
            self.단품.단품재고
            num = self.단품.단품재고.실수량
            return f"<단품출하요청>{self.단품} : {self.출하요청수량} {self.단품.단위} (현재 수량 : {num})"
        else:
            num = 0
            return f"<단품출하요청>{self.단품} : {self.출하요청수량} {self.단품.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.단품.단품재고.출하요청제외수량 -= self.출하요청수량
            self.단품.단품재고.save()
        except:
            try:
                ST = StockOfSingleProduct.objects.get(단품=self.단품)
                ST.출하요청제외수량 = self.출하요청수량
                ST.save()
            except:

                StockOfSingleProduct.objects.create(단품=self.단품, 출하요청제외수량=-self.출하요청수량)

    def unexport(self):
        try:
            self.단품출하등록
            return False
        except:
            return True

    def process(self):
        try:
            self.단품출하등록
            return "출하완료"
        except:
            return "출하요청완료"


class StockOfSingleProductOut(TimeStampedModel):

    단품출하요청 = models.OneToOneField(
        "StockOfSingleProductOutRequest",
        related_name="단품출하등록",
        on_delete=models.CASCADE,
        null=True,
    )
    출하자 = models.ForeignKey(
        users_models.User, related_name="단품출하등록", on_delete=models.SET_NULL, null=True,
    )
    출하일 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    출하수량 = models.IntegerField(null=True)
    거래명세서첨부 = models.FileField(
        upload_to="deal", blank=True, null=True, help_text="거래명세서를 첨부해주세요."
    )

    class Meta:
        verbose_name = "단품출하등록"
        verbose_name_plural = "단품출하등록"

    def __str__(self):
        num = self.단품출하요청.단품.단품재고.실수량
        return f"{self.단품출하요청.단품} : {self.출하수량} {self.단품출하요청.단품.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.단품출하요청.단품.단품재고.실수량 is None:
                self.단품출하요청.단품.단품재고.실수량 = 0
            if self.단품출하요청.단품.단품재고.입고요청포함수량 is None:
                self.단품출하요청.단품.단품재고.입고요청포함수량 = 0
            self.단품출하요청.단품.단품재고.실수량 -= self.출하수량
            차이 = self.단품출하요청.출하요청수량 - self.출하수량
            self.단품출하요청.단품.단품재고.출하요청제외수량 += 차이
            self.단품출하요청.단품.단품재고.입고요청포함수량 -= self.출하수량
            self.단품출하요청.단품.단품재고.save()
        except:
            ST = StockOfSingleProduct.objects.get(단품=self.단품출하요청.단품)
            ST.실수량 -= self.출하수량
            ST.출하요청제외수량 = ST.실수량
            ST.save()
