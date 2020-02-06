from django.db import models


class Partner(models.Model):

    고객 = "고객"
    대리점 = "대리점"
    공급처 = "공급처"

    거래처_CHOICES = (
        (고객, "고객"),
        (대리점, "대리점"),
        (공급처, "공급처"),
    )

    작성자 = models.ForeignKey(
        "users.User", related_name="거래처작성자", on_delete=models.SET_NULL, null=True
    )
    작성일 = models.DateField(auto_now=True, auto_now_add=False)
    거래처구분 = models.CharField(choices=거래처_CHOICES, max_length=4, blank=True, default=공급처)
    거래처코드 = models.IntegerField(null=True)
    거래처명 = models.CharField(max_length=160, blank=True)
    사업자등록번호 = models.IntegerField(null=True)
    담당자 = models.ForeignKey(
        "users.User", related_name="거래처담당자", on_delete=models.SET_NULL, null=True
    )
    연락처 = models.IntegerField()
    이메일 = models.EmailField(max_length=254)
    사업장주소 = models.CharField(max_length=160, blank=True)
    사업자등록증첨부 = models.FileField(blank=True)
    특이사항 = models.TextField(blank=True)
    사용여부 = models.BooleanField(default=False)

    class Meta:
        verbose_name = "거래처"
        verbose_name_plural = "거래처"

    def __str__(self):
        return self.거래처명

    def save(self, *args, **kwargs):
        if self.거래처구분 == "공급처":
            S = SupplyPartner.objects.create(
                공급처작성자 = self.작성자,
                작성일 = self.작성일,
                거래처구분 = self.거래처구분,
                거래처코드 = self.거래처코드,
                거래처명 = self.거래처명,
                사업자등록번호 = self.사업자등록번호,
                공급처담당자 = self.담당자,
                연락처 = self.연락처,
                이메일 = self.이메일,
                사업장주소 = self.사업장주소,
                사업자등록증첨부 = self.사업자등록증첨부,
                특이사항 = self.특이사항,
                사용여부 = self.사용여부,

            )
            
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

class SupplyPartner(models.Model):
    고객 = "고객"
    대리점 = "대리점"
    공급처 = "공급처"
    거래처_CHOICES = (
        (고객, "고객"),
        (대리점, "대리점"),
        (공급처, "공급처"),
    )
    공급처작성자 = models.ForeignKey(
        "users.User", related_name="공급처거래처작성자", on_delete=models.SET_NULL, null=True
    )
    작성일 = models.DateField(auto_now=True, auto_now_add=False)
    거래처구분 = models.CharField(choices=거래처_CHOICES, max_length=4, blank=True, default=공급처)
    거래처코드 = models.IntegerField(null=True)
    거래처명 = models.CharField(max_length=160, blank=True)
    사업자등록번호 = models.IntegerField(null=True)
    공급처담당자 = models.ForeignKey(
        "users.User", related_name="공급처거래처담당자", on_delete=models.SET_NULL, null=True
    )
    연락처 = models.IntegerField()
    이메일 = models.EmailField(max_length=254)
    사업장주소 = models.CharField(max_length=160, blank=True)
    사업자등록증첨부 = models.FileField(blank=True)
    특이사항 = models.TextField(blank=True)
    사용여부 = models.BooleanField(default=False)

    class Meta:
        verbose_name = "공급처"
        verbose_name_plural = "공급처"

    def __str__(self):
        return self.거래처명    
    

class Material(models.Model):

    EA = "EA"
    ROLL = "ROLL"
    BOX = "BOX"
    SET = "SET"
    봉 = "봉"

    단위_CHOICES = (
        (EA, "EA"),
        (ROLL, "ROLL"),
        (BOX, "BOX"),
        (SET, "SET"),
        (봉, "봉"),
    )

    자재코드 = models.CharField(max_length=160, blank=True)
    자재품명 = models.CharField(max_length=160, blank=True)
    규격 = models.CharField(max_length=160, blank=True)
    단위 = models.CharField(choices=단위_CHOICES, max_length=4, blank=True, default=EA)
    자재공급업체 = models.ForeignKey(
        "SupplyPartner", related_name="자재공급업체", on_delete=models.SET_NULL, null=True
    )

    단가 = models.IntegerField(null=True)
    특이사항 = models.TextField(blank=True)

    class Meta:
        verbose_name = "자재"
        verbose_name_plural = "자재"

    def __str__(self):
        return self.자재품명

class SingleProduct(models.Model):

    작성자 = models.ForeignKey(
        "users.User", related_name="단품제품작성자", on_delete=models.SET_NULL, null=True
    )
    작성일 = models.DateField(auto_now=True, auto_now_add=False)
    모델코드 =models.CharField(max_length=160, blank=True)
    모델명 = models.CharField(max_length=160, blank=True)
    규격 = models.CharField(max_length=160, blank=True)
    단위 = models.CharField(max_length=160, blank=True)
    단가 = models.IntegerField(null=True)
    단품구성자재 = models.ManyToManyField(
        "SingleProductMaterial", related_name="단품제품",  blank =True,
    )


    class Meta:
        verbose_name = "단품제품"
        verbose_name_plural = "단품제품"

    def __str__(self):
        return self.모델명

class SingleProductMaterial(models.Model):
    단품구성자재 = models.ManyToManyField(
        "Material", related_name="단품구성자재",  blank =True,
    )
    수량 = models.IntegerField(null=True)

    class Meta:
        
        verbose_name = "단품제품구성자재"
        verbose_name_plural = "단품제품구성자재"

    def __str__(self):
        자재품명 = self.단품구성자재.values()[0]["자재품명"]
        단위 = self.단품구성자재.values()[0]["단위"]
        return f"{자재품명} : {self.수량} {단위}"

class RackProduct(models.Model):
    
    작성자 = models.ForeignKey(
        "users.User", related_name="랙제품작성자", on_delete=models.SET_NULL, null=True
    )
    작성일 = models.DateField(auto_now=True, auto_now_add=False)
    랙시리얼코드 =models.CharField(max_length=160, blank=True)
    랙모델명 = models.CharField(max_length=160, blank=True)
    규격 = models.CharField(max_length=160, blank=True)
    단위 = models.CharField(max_length=160, blank=True)
    단가 = models.IntegerField(null=True)
    랙구성단품 = models.ManyToManyField(
        "RackProductMaterial", related_name="랙제품",  blank =True,
    )

    
    class Meta:
        verbose_name = "랙제품"
        verbose_name_plural = "랙제품"

    def __str__(self):
        return self.랙모델명

class RackProductMaterial(models.Model):
    랙구성단품 = models.ManyToManyField(
        "SingleProduct", related_name="랙구성단품",  blank =True,
    )
    수량 = models.IntegerField(null=True)


    class Meta:
        verbose_name = "랙구성단품"
        verbose_name_plural = "랙구성단품"

    def __str__(self):
        자재품명 = self.랙구성단품.values()[0]["모델명"]
        단위 = self.랙구성단품.values()[0]["단위"]
        return f"{자재품명} : {self.수량} {단위}"

class Measure(models.Model):
    계측기코드 = models.CharField(max_length=160, blank=True)
    계측기명= models.CharField(max_length=160, blank=True)
    자산관리번호 = models.IntegerField()
    계측기규격= models.CharField(max_length=160, blank=True)
    설치년월일 = models.DateField(auto_now=False, auto_now_add=False)
    사용공정명= models.CharField(max_length=160, blank=True)
    설치장소= models.CharField(max_length=160, blank=True)
    file= models.ImageField(upload_to="images", blank=True, help_text="계측기의 사진을 첨부해주세요.")

    class Meta:
        verbose_name = "계측기"
        verbose_name_plural = "계측기"

    def __str__(self):
        return self.계측기명