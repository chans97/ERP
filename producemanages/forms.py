from django import forms
from . import models
from StandardInformation import models as SI_models


class UploadProducePlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["생산계획등록코드"].widget.attrs.update(size="20")

    class Meta:
        model = models.ProduceRegister
        fields = (
            "생산계획등록코드",
            "계획생산량",
            "특이사항",
            "현재공정",
            "현재공정달성율",
        )
        help_texts = {
            "생산계획등록코드": "*생산계획등록코드 앞에 PP을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        }
        widgets = {
            "현재공정": forms.RadioSelect(),
            "현재공정달성율": forms.RadioSelect(),
            "계획생산량": forms.NumberInput(attrs={"size": "10"}),
        }

    def clean(self):
        code = self.cleaned_data.get("생산계획등록코드")
        partner = models.ProduceRegister.objects.filter(생산계획등록코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.add_error(
                    "생산계획등록코드", forms.ValidationError("*해당 생산계획등록코드는 이미 존재합니다.")
                )
            elif code != "PP":
                self.add_error(
                    "생산계획등록코드", forms.ValidationError("*생산계획등록코드는 PP으로 시작해야 합니다.")
                )

                return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class UpdateProducePlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.ProduceRegister
        fields = (
            "현재공정",
            "현재공정달성율",
            "일일생산량",
        )
        help_texts = {}
        widgets = {
            "현재공정": forms.RadioSelect(),
            "현재공정달성율": forms.RadioSelect(),
            "일일생산량": forms.NumberInput(attrs={"size": "10"}),
        }

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class UpdateProducePlanTotalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.ProduceRegister
        fields = (
            "계획생산량",
            "특이사항",
            "현재공정",
            "현재공정달성율",
        )
        widgets = {
            "현재공정": forms.RadioSelect(),
            "현재공정달성율": forms.RadioSelect(),
            "계획생산량": forms.NumberInput(attrs={"size": "10"}),
        }

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class UploadWorkOrderForm(forms.ModelForm):
    class Meta:
        model = models.WorkOrder
        fields = (
            "작업지시코드",
            "수량",
            "특이사항",
        )
        help_texts = {
            "작업지시코드": "*작업지시코드 앞에 WO을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        }

    def clean(self):
        code = self.cleaned_data.get("작업지시코드")
        partner = models.WorkOrder.objects.filter(작업지시코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.add_error("작업지시코드", forms.ValidationError("*해당 작업지시코드는 이미 존재합니다."))
            elif code != "WO":
                self.add_error(
                    "작업지시코드", forms.ValidationError("*작업지시코드는 WO로 시작해야 합니다.")
                )

                return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner
