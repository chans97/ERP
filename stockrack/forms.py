from django import forms
from . import models
from StandardInformation import models as SI_models
from stocksingle import models as SS_models


class UploadRackOutForm(forms.ModelForm):
    class Meta:
        model = models.StockOfRackProductOutRequest
        fields = (
            "출하요청수량",
            "출하희망일",
        )
        help_texts = {
            "출하희망일": "*형식 : (yyyy-mm-dd) (필수항목이 아닙니다.)",
        }
        widgets = {}

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class UploadSingleInForm(forms.ModelForm):
    단품 = forms.CharField(max_length=20)

    class Meta:
        model = SS_models.StockOfSingleProductInRequest
        fields = (
            "입고요청수량",
            "입고요청일",
        )
        help_texts = {
            "입고요청일": "*형식 : (yyyy-mm-dd) (필수항목이 아닙니다.)",
        }
        widgets = {}

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner

    def clean(self):
        code = self.cleaned_data.get("단품", "123")
        single = SI_models.SingleProduct.objects.get_or_none(모델코드=code)
        if not single:
            self.add_error("단품", forms.ValidationError("*다시 입력해주세요."))

        else:
            self.cleaned_data["단품"] = single
            return self.cleaned_data
