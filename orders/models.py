from django.db import models
from core.models import TimeStampedModel
from StandardInformation import models as SI_models
from users import models as users_models


class OrderRegister(TimeStampedModel):

    입찰 = "입찰"
    대리점 = "대리점"
    AS = "A/S"
    내부계획 = "내부계획"

    영업구분_CHOICES = ((입찰, "입찰"), (대리점, "대리점"), (AS, "A/S"), (내부계획, "내부계획"))

    삼형전자 = "삼형전자"
    엠에스텔레콤 = "엠에스텔레콤"

    사업장구분_CHOICES = (
        (삼형전자, "삼형전자"),
        (엠에스텔레콤, "엠에스텔레콤"),
    )

    출하완료 = "출하완료"
    출하미완료 = "출하미완료"

    출하구분_CHOICES = (
        (출하완료, "출하완료"),
        (출하미완료, "출하미완료"),
    )

    단품 = "단품"
    랙 = "랙"

    제품구분_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )
    랙생산의뢰 = models.ForeignKey(
        "self", related_name="단품생산의뢰", on_delete=models.SET_NULL, null=True, blank=True
    )
    작성자 = models.ForeignKey(
        users_models.User,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    수주코드 = models.CharField(max_length=50)
    영업구분 = models.CharField(choices=영업구분_CHOICES, max_length=10, blank=True, default=입찰)
    제품구분 = models.CharField(choices=제품구분_CHOICES, max_length=10, blank=True, default=단품)
    사업장구분 = models.CharField(
        choices=사업장구분_CHOICES, max_length=10, blank=True, default=삼형전자
    )
    수주일자 = models.DateField(auto_now=False, auto_now_add=False)
    고객사명 = models.ForeignKey(
        SI_models.CustomerPartner,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    현장명 = models.CharField(max_length=50)
    납품요청일 = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    납품수량 = models.IntegerField()
    특이사항 = models.TextField(blank=True)
    단품모델 = models.ForeignKey(
        SI_models.SingleProduct,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    랙모델 = models.ForeignKey(
        SI_models.RackProduct,
        related_name="수주등록",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    출하구분 = models.CharField(
        choices=출하구분_CHOICES, max_length=10, blank=True, default=출하미완료
    )
    랙조립도면 = models.FileField(
        upload_to="blueprint", blank=True, null=True, help_text="랙 수주의 경우 조립도면을 첨부해주세요."
    )

    class Meta:
        verbose_name = "수주등록"
        verbose_name_plural = "수주등록"

    def __str__(self):
        if self.고객사명 is None:
            return f"{self.수주코드}"

        else:
            return f"{self.고객사명}의 수주 : {self.수주코드}"

    def process(self):
        try:
            pro = self.생산요청
            try:
                cess = self.생산요청.생산계획.현재공정
                pro = self.생산요청.생산계획.현재공정달성율
                try:
                    pro = self.생산요청.생산계획.작업지시서.작업지시서등록.최종검사
                    try:
                        pro = self.생산요청.생산계획.작업지시서.작업지시서등록.최종검사.최종검사등록
                        return "최종검사완료"
                    except:
                        return "최종검사의뢰완료"
                except:
                    return f"생산중({cess}:{pro})"
            except:
                return "생산의뢰완료"
        except:
            return "수주등록완료"

    def singlestock(self):
        return self.단품모델.단품재고.실수량

    def singlestockincludeexception(self):
        return self.단품모델.단품재고.출하요청제외수량

    def leftsingle(self):
        left = 0
        try:
            for q in self.단품출하요청.all():
                left += q.출하요청수량
        except:
            pass

        return left

    def backsingle(self):
        back = 0
        try:
            for q in self.단품입고요청.all():
                back += q.입고요청수량
        except:
            pass

        return back

    def needtoout(self):
        needtoout = self.납품수량 - self.leftsingle()
        return needtoout

    def rackstock(self):
        rackstock = []
        for com in self.랙모델.랙구성단품.all():
            if com.랙구성 == "자재":
                num = com.수량
                single = com.랙구성자재
                number = int(single.자재재고.실수량 / num)
                rackstock.append(number)
            else:
                num = com.수량
                single = com.랙구성단품
                number = int(single.단품재고.실수량 / num)
                rackstock.append(number)
        stock = min(rackstock)
        if stock < 0:
            stock = 0
        return stock

    def rackstockincludeexception(self):
        rackstock = []
        for com in self.랙모델.랙구성단품.all():
            if com.랙구성 == "자재":
                num = com.수량
                single = com.랙구성자재
                number = int(single.자재재고.출고요청제외수량 / num)
                rackstock.append(number)
            else:
                num = com.수량
                single = com.랙구성단품
                number = int(single.단품재고.출하요청제외수량 / num)
                rackstock.append(number)
        stock = min(rackstock)
        if stock < 0:
            stock = 0
        return stock

    def leftrack(self):
        left = 0
        try:
            for q in self.랙출하요청.all():
                left += q.출하요청수량
        except:
            pass

        return left

    def needtooutrack(self):
        needtoout = self.납품수량 - self.leftrack()
        return needtoout


class OrderProduce(TimeStampedModel):

    일반 = "일반"
    긴급 = "긴급"

    긴급도_CHOICES = (
        (일반, "일반"),
        (긴급, "긴급"),
    )

    생산의뢰수주 = models.OneToOneField(
        "OrderRegister",
        related_name="생산요청",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    생산의뢰코드 = models.CharField(max_length=50)

    긴급도 = models.CharField(choices=긴급도_CHOICES, max_length=10, blank=True, default=일반)
    생산목표수량 = models.IntegerField()

    class Meta:
        verbose_name = "생산의뢰등록"
        verbose_name_plural = "생산의뢰등록"

    def __str__(self):
        return f" '{self.생산의뢰수주}' 의 생산의뢰 : {self.생산의뢰코드}"
