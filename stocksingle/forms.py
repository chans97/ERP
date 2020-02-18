from django import forms
from . import models
from StandardInformation import models as SI_models


class UploadSingleOutForm(forms.ModelForm):
    class Meta:
        model = models.StockOfSingleProductOutRequest
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

