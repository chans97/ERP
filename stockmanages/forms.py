from django import forms
from . import models
from StandardInformation import models as SI_models
from stocksingle import models as SS_models
from afterservices import models as AS_models
from qualitycontrols import models as QC_models
from stockrack import models as SR_models


class materialcheckrequest(forms.Form):

    수입검사의뢰코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text=f"*수입검사의뢰코드 앞에 MC을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        widget=forms.TextInput(attrs={"size": "12"}),
    )
    수량 = forms.IntegerField()
    자재 = forms.CharField()

    def clean(self):
        self.is_bound = False
        cleaned_data = super().clean()
        code = self.cleaned_data.get("수입검사의뢰코드")
        partner = QC_models.MaterialCheckRegister.objects.filter(수입검사의뢰코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.is_bound = True
                self.add_error(
                    "수입검사의뢰코드", forms.ValidationError("*해당 수입검사의뢰코드는 이미 존재합니다.")
                )
            elif code != "MC":
                self.is_bound = True
                self.add_error(
                    "수입검사의뢰코드", forms.ValidationError("*수입검사의뢰코드 MC로 시작해야 합니다.")
                )
            else:
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class materialinregisterForm(forms.ModelForm):
    class Meta:
        model = models.StockOfMaterialIn
        fields = (
            "입고일",
            "입고수량",
        )
        help_texts = {
            "입고일": "형식 : yyyy-mm-dd (기본값은 오늘입니다.)",
        }
        widgets = {
            "입고유형": forms.RadioSelect(),
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class materialoutregisterForm(forms.ModelForm):
    class Meta:
        model = models.StockOfMaterialOut
        fields = (
            "출고일",
            "출고수량",
            "출고유형",
        )
        help_texts = {
            "출고일": "형식 : yyyy-mm-dd (기본값은 오늘입니다.)",
        }
        widgets = {
            "출고유형": forms.RadioSelect(),
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class updatestockofmaterial(forms.Form):

    실수량 = forms.IntegerField()
    입고요청포함수량 = forms.IntegerField()
    출고요청제외수량 = forms.IntegerField()
    자재 = forms.CharField()

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class singleinregisterForm(forms.ModelForm):
    class Meta:
        model = SS_models.StockOfSingleProductIn
        fields = (
            "입고일",
            "입고수량",
        )
        help_texts = {
            "입고일": "형식 : yyyy-mm-dd (기본값은 오늘입니다.)",
        }

    def clean(self):
        self.is_bound = False
        cleaned_data = super().clean()

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class singleoutregisterForm(forms.ModelForm):
    class Meta:
        model = SS_models.StockOfSingleProductOut
        fields = (
            "출하일",
            "출하수량",
            "거래명세서첨부",
        )
        help_texts = {
            "출하일": "형식 : yyyy-mm-dd (기본값은 오늘입니다.)",
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class updatestockofsingle(forms.Form):

    실수량 = forms.IntegerField()
    입고요청포함수량 = forms.IntegerField()
    출하요청제외수량 = forms.IntegerField()
    단품 = forms.CharField()

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class rackoutregisterForm(forms.ModelForm):
    class Meta:
        model = SR_models.StockOfRackProductOut
        fields = (
            "출하일",
            "출하수량",
            "거래명세서첨부",
        )
        help_texts = {
            "출하일": "형식 : yyyy-mm-dd (기본값은 오늘입니다.)",
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order

    def clean(self):
        self.is_bound = False
        cleaned_data = super().clean()
