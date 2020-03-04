from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models
from producemanages import models as proms_models


class StockOfMaterial(TimeStampedModel):
    자재 = models.OneToOneField(
        SI_models.Material, related_name="자재재고", on_delete=models.CASCADE
    )
    실수량 = models.IntegerField(null=True, blank=True, default=0)
    입고요청포함수량 = models.IntegerField(null=True, blank=True, default=0)
    출고요청제외수량 = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = "자재재고"
        verbose_name_plural = "자재재고"

    def __str__(self):
        if self.실수량 is None:
            num = 0
        else:
            num = self.실수량
        return f"{self.자재} : {num} {self.자재.단위}"

    def save(self, *args, **kwargs):
        StockOfMaterialHistory.objects.create(
            자재=self.자재, 실수량=self.실수량, 입고요청포함수량=self.입고요청포함수량, 출고요청제외수량=self.출고요청제외수량,
        )
        super().save(*args, **kwargs)


class StockOfMaterialHistory(TimeStampedModel):
    자재 = models.ForeignKey(
        SI_models.Material, related_name="자재재고기록", on_delete=models.CASCADE
    )
    실수량 = models.IntegerField(null=True, blank=True, default=0)
    입고요청포함수량 = models.IntegerField(null=True, blank=True, default=0)
    출고요청제외수량 = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = "자재재고기록용"
        verbose_name_plural = "자재재고기록용"

    def __str__(self):
        date = f"{self.created.date()}  {self.created.hour}: {self.created.minute}"
        if self.실수량 is None:
            num = 0
        else:
            num = self.실수량
        return f"({date}) {self.자재} : {num} {self.자재.단위}"


class StockOfMaterialInRequest(TimeStampedModel):
    일반 = "일반"
    반납 = "반납"

    입고유형_CHOICES = (
        (일반, "일반"),
        (반납, "반납"),
    )

    자재 = models.ForeignKey(
        SI_models.Material, related_name="자재입고요청", on_delete=models.CASCADE, null=True
    )
    입고요청수량 = models.IntegerField()
    입고요청자 = models.ForeignKey(
        users_models.User, related_name="자재입고요청", on_delete=models.SET_NULL, null=True,
    )
    입고요청일 = models.DateField(auto_now=False, auto_now_add=False)
    입고유형 = models.CharField(choices=입고유형_CHOICES, max_length=10, null=True, default=일반)

    class Meta:
        verbose_name = "자재입고요청"
        verbose_name_plural = "자재입고요청"

    def __str__(self):
        if self.자재.자재재고.실수량 is not None:
            self.자재.자재재고
            num = self.자재.자재재고.실수량
            return f"<자재입고요청>{self.자재} : {self.입고요청수량} {self.자재.단위} (현재 수량 : {num})"
        else:
            num = 0
            return f"<자재입고요청>{self.자재} : {self.입고요청수량} {self.자재.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.자재.자재재고.입고요청포함수량 += self.입고요청수량
            self.자재.자재재고.save()
        except:
            StockOfMaterial.objects.create(자재=self.자재, 입고요청포함수량=self.입고요청수량)


class StockOfMaterialIn(TimeStampedModel):

    일반 = "일반"
    반납 = "반납"

    입고유형_CHOICES = (
        (일반, "일반"),
        (반납, "반납"),
    )

    자재입고요청 = models.OneToOneField(
        "StockOfMaterialInRequest",
        related_name="자재입고등록",
        on_delete=models.CASCADE,
        null=True,
    )
    입고자 = models.ForeignKey(
        users_models.User, related_name="자재입고등록", on_delete=models.SET_NULL, null=True,
    )
    입고일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    입고수량 = models.IntegerField(null=True)
    입고유형 = models.CharField(choices=입고유형_CHOICES, max_length=10, null=True, default=일반)

    class Meta:
        verbose_name = "자재입고등록"
        verbose_name_plural = "자재입고등록"

    def __str__(self):
        num = self.자재입고요청.자재.자재재고.실수량
        return f"{self.자재입고요청.자재} : {self.입고수량} {self.자재입고요청.자재.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.자재입고요청.자재.자재재고.실수량 is None:
                self.자재입고요청.자재.자재재고.실수량 = 0
            if self.자재입고요청.자재.자재재고.출고요청제외수량 is None:
                self.자재입고요청.자재.자재재고.출고요청제외수량 = 0
            self.자재입고요청.자재.자재재고.실수량 += self.입고수량
            차이 = self.자재입고요청.입고요청수량 - self.입고수량
            self.자재입고요청.자재.자재재고.입고요청포함수량 -= 차이
            self.자재입고요청.자재.자재재고.출고요청제외수량 += self.입고수량
            self.자재입고요청.자재.자재재고.save()
        except:
            StockOfMaterial.objects.create(
                자재=self.자재입고요청.자재, 실수량=self.입고수량, 입고요청포함수량=self.입고수량
            )


class StockOfMaterialOutRequest(TimeStampedModel):
    생산 = "생산"
    AS = "AS"

    출고유형_CHOICES = (
        (생산, "생산"),
        (AS, "AS"),
    )
    자재 = models.ForeignKey(
        SI_models.Material, related_name="자재출고요청", on_delete=models.CASCADE, null=True
    )
    출고요청수량 = models.IntegerField()
    출고요청자 = models.ForeignKey(
        users_models.User, related_name="자재출고요청", on_delete=models.SET_NULL, null=True,
    )
    출고요청일 = models.DateField(auto_now=False, auto_now_add=False,)
    출고유형 = models.CharField(choices=출고유형_CHOICES, max_length=10, null=True, default=생산)

    class Meta:
        verbose_name = "자재출고요청"
        verbose_name_plural = "자재출고요청"

    def __str__(self):
        if self.자재.자재재고.실수량 is not None:
            self.자재.자재재고
            num = self.자재.자재재고.실수량
            return f"<자재출고요청>{self.자재} : {self.출고요청수량} {self.자재.단위} (현재 수량 : {num})"
        else:
            num = 0
            return f"<자재출고요청>{self.자재} : {self.출고요청수량} {self.자재.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.자재.자재재고.출고요청제외수량 -= self.출고요청수량
            self.자재.자재재고.save()
        except:
            try:
                ST = StockOfMaterial.objects.get(자재=self.자재)
                ST.출고요청제외수량 = self.출고요청수량
                ST.save()
            except:

                StockOfMaterial.objects.create(자재=self.자재, 출고요청제외수량=-self.출고요청수량)


class StockOfMaterialOut(TimeStampedModel):

    생산 = "생산"
    AS = "AS"

    출고유형_CHOICES = (
        (생산, "생산"),
        (AS, "AS"),
    )

    자재출고요청 = models.OneToOneField(
        "StockOfMaterialOutRequest",
        related_name="자재출고등록",
        on_delete=models.CASCADE,
        null=True,
    )
    출고자 = models.ForeignKey(
        users_models.User, related_name="자재출고등록", on_delete=models.SET_NULL, null=True,
    )
    출고일 = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    출고수량 = models.IntegerField(null=True)
    출고유형 = models.CharField(choices=출고유형_CHOICES, max_length=10, null=True, default=생산)

    class Meta:
        verbose_name = "자재출고등록"
        verbose_name_plural = "자재출고등록"

    def __str__(self):
        num = self.자재출고요청.자재.자재재고.실수량
        return f"{self.자재출고요청.자재} : {self.출고수량} {self.자재출고요청.자재.단위} (현재 수량 : {num})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.자재출고요청.자재.자재재고.실수량 is None:
                self.자재출고요청.자재.자재재고.실수량 = 0
            if self.자재출고요청.자재.자재재고.입고요청포함수량 is None:
                self.자재출고요청.자재.자재재고.입고요청포함수량 = 0
            self.자재출고요청.자재.자재재고.실수량 -= self.출고수량
            차이 = self.자재출고요청.출고요청수량 - self.출고수량
            self.자재출고요청.자재.자재재고.출고요청제외수량 += 차이
            self.자재출고요청.자재.자재재고.입고요청포함수량 -= self.출고수량
            self.자재출고요청.자재.자재재고.save()
        except:
            ST = StockOfMaterial.objects.get(자재=self.자재출고요청.자재)
            ST.실수량 -= self.출고수량
            ST.출고요청제외수량 = ST.실수량
            ST.save()

