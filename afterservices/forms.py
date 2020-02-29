from django import forms
from . import models
from StandardInformation import models as SI_models


class ASRegisterForm(forms.ModelForm):
    의뢰처 = forms.CharField(
        max_length=20, required=True, help_text="*거래처 코드로 입력해주시길 바랍니다."
    )

    class Meta:
        model = models.ASRegisters
        fields = (
            "접수번호",
            "접수일",
            "현상",
            "불량분류코드",
            "불량분류",
            "접수제품분류",
            "대응유형",
            "의뢰자전화번호",
            "방문요청일",
        )
        help_texts = {
            "접수번호": "*최종검사코드 앞에 AR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "접수일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        widgets = {
            "불량분류": forms.RadioSelect(),
            "접수제품분류": forms.RadioSelect(),
            "대응유형": forms.RadioSelect(),
        }

    def clean(self):
        code = self.cleaned_data.get("접수번호")
        codep = self.cleaned_data.get("의뢰처")
        partner = models.ASRegisters.objects.filter(접수번호=code)
        partner = list(partner)
        의뢰처 = models.SI_models.CustomerPartner.objects.get_or_none(거래처코드=codep)

        if code:
            code = code[0:2]
            if partner:
                self.add_error("접수번호", forms.ValidationError("*해당 접수번호는 이미 존재합니다."))
            elif code != "AR":
                self.add_error("접수번호", forms.ValidationError("*접수번호는 AR로 시작해야 합니다."))
            elif 의뢰처 is None:
                self.add_error("의뢰처", forms.ValidationError("*존재하지 않는 거래처입니다."))
            else:
                self.cleaned_data["의뢰처"] = 의뢰처
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class ASSingleForm(forms.Form):

    단품모델코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text="*모델코드로 입력해주시길 바랍니다.",
        widget=forms.TextInput(attrs={"size": "12"}),
    )

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


class ASRackForm(forms.Form):

    랙시리얼코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text="*랙시리얼코드로 입력해주시길 바랍니다.",
        widget=forms.TextInput(attrs={"size": "12"}),
    )

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

