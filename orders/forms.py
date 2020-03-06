from django import forms
from . import models
from StandardInformation import models as SI_models
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from .widgets import DatePickerWidget, CounterTextInput


class UploadOrderForm(forms.Form):

    단품 = "단품"
    랙 = "랙"

    제품구분_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

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

    수주코드 = forms.CharField(help_text="*수주코드 앞에 OR을 붙여주시길 바랍니다.",)
    영업구분 = forms.ChoiceField(choices=영업구분_CHOICES, widget=forms.RadioSelect())
    제품구분 = forms.ChoiceField(choices=제품구분_CHOICES, widget=forms.RadioSelect())
    사업장구분 = forms.ChoiceField(choices=사업장구분_CHOICES, widget=forms.RadioSelect())
    수주일자 = DateField(
        required=True, help_text="*형식 : (yyyy-mm-dd) ", widget=forms.SelectDateWidget
    )
    거래처코드 = forms.CharField(
        max_length=20, required=True, help_text="*거래처 코드로 입력해주시길 바랍니다."
    )
    현장명 = forms.CharField()
    납품요청일 = forms.DateField(
        required=False, help_text="*형식 : (yyyy-mm-dd) ", widget=forms.SelectDateWidget
    )
    특이사항 = forms.CharField(required=False,)

    def clean(self):
        self.is_bound = False
        cleaned_data = super().clean()
        code = self.cleaned_data.get("수주코드")
        order = models.OrderRegister.objects.get_or_none(수주코드=code)
        거래처코드 = self.cleaned_data.get("거래처코드")
        customer = SI_models.CustomerPartner.objects.get_or_none(거래처코드=거래처코드)
        if code:
            self.is_bound = True
            code = code[0:2]

            if order:
                self.add_error("수주코드", forms.ValidationError("*해당 수주코드는 이미 존재합니다."))
            elif code != "OR":
                self.add_error("수주코드", forms.ValidationError("*수주코드는 OR로 시작해야 합니다."))
            elif customer is None:
                self.add_error("거래처코드", forms.ValidationError("*해당 고객사를 찾을 수 없습니다."))
            else:
                self.cleaned_data["거래처코드"] = customer
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class EditOrderForm(forms.Form):

    단품 = "단품"
    랙 = "랙"

    제품구분_CHOICES = (
        (단품, "단품"),
        (랙, "랙"),
    )

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

    영업구분 = forms.ChoiceField(choices=영업구분_CHOICES, widget=forms.RadioSelect())
    제품구분 = forms.ChoiceField(choices=제품구분_CHOICES, widget=forms.RadioSelect())
    사업장구분 = forms.ChoiceField(choices=사업장구분_CHOICES, widget=forms.RadioSelect())
    수주일자 = forms.DateField(required=True, help_text="*형식 : (yyyy-mm-dd) ",)
    거래처코드 = forms.CharField(
        max_length=20, required=True, help_text="*거래처 코드로 입력해주시길 바랍니다."
    )
    현장명 = forms.CharField()
    납품요청일 = forms.DateField(required=False, help_text="*형식 : (yyyy-mm-dd) ")
    특이사항 = forms.CharField(required=False,)

    def clean(self):
        cleaned_data = super().clean()
        code = self.cleaned_data.get("수주코드")
        order = models.OrderRegister.objects.get_or_none(수주코드=code)
        거래처코드 = self.cleaned_data.get("거래처코드")
        customer = SI_models.CustomerPartner.objects.get_or_none(거래처코드=거래처코드)
        if code:
            code = code[0:2]

            if order:
                self.add_error("수주코드", forms.ValidationError("*해당 수주코드는 이미 존재합니다."))
            elif code != "OR":
                self.add_error("수주코드", forms.ValidationError("*수주코드는 OR로 시작해야 합니다."))
            elif customer is None:
                self.add_error("거래처코드", forms.ValidationError("*해당 고객사를 찾을 수 없습니다."))
            else:
                self.cleaned_data["거래처코드"] = customer
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class OrderSingleForm(forms.Form):

    단품모델코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text="*모델코드로 입력해주시길 바랍니다.",
        widget=forms.TextInput(attrs={"size": "12"}),
    )
    납품수량 = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        code = self.cleaned_data.get("단품모델코드")
        single = SI_models.SingleProduct.objects.get_or_none(모델코드=code)
        if code:
            if single is None:
                self.add_error("단품모델코드", forms.ValidationError("*해당 단품을 찾을 수 없습니다."))
            else:
                self.cleaned_data["단품모델코드"] = single
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class OrderRackForm(forms.Form):

    랙시리얼코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text="*랙시리얼코드로 입력해주시길 바랍니다.",
        widget=forms.TextInput(attrs={"size": "12"}),
    )
    납품수량 = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        code = self.cleaned_data.get("랙시리얼코드")
        rack = SI_models.RackProduct.objects.get_or_none(랙시리얼코드=code)
        if code:
            if rack is None:
                self.add_error("랙시리얼코드", forms.ValidationError("*해당 랙을 찾을 수 없습니다."))
            else:
                self.cleaned_data["랙시리얼코드"] = rack
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class UploadOrderProduceForm(forms.ModelForm):
    일반 = "일반"
    긴급 = "긴급"

    긴급도_CHOICES = (
        (일반, "일반"),
        (긴급, "긴급"),
    )

    긴급도 = forms.ChoiceField(choices=긴급도_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = models.OrderProduce
        fields = (
            "생산의뢰코드",
            "생산목표수량",
        )
        help_texts = {
            "생산의뢰코드": "*생산의뢰코드 앞에 OP을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        }
        widgets = {}

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("생산의뢰코드")
        partner = models.OrderProduce.objects.filter(생산의뢰코드=code)
        partner = list(partner)
        if code:
            self.is_bound = True
            code = code[0:2]
            if partner:
                self.add_error("생산의뢰코드", forms.ValidationError("*해당 생산의뢰코드는 이미 존재합니다."))
            elif code != "OP":
                self.add_error(
                    "생산의뢰코드", forms.ValidationError("*생산의뢰코드는 OP으로 시작해야 합니다.")
                )

                return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class EditOrderProduceForm(forms.ModelForm):
    일반 = "일반"
    긴급 = "긴급"

    긴급도_CHOICES = (
        (일반, "일반"),
        (긴급, "긴급"),
    )

    긴급도 = forms.ChoiceField(choices=긴급도_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = models.OrderProduce
        fields = ("생산목표수량",)

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner
