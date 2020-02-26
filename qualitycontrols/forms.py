from django import forms
from . import models
from StandardInformation import models as SI_models


class FinalCheckRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["최종검사코드"].widget.attrs.update(size="20")

    class Meta:
        model = models.FinalCheckRegister
        fields = (
            "최종검사코드",
            "검시일",
            "CR",
            "MA",
            "MI",
            "검사수준",
            "Sample방식",
            "결점수",
            "전원전압",
            "POWERTRANS",
            "FUSE_전_ULUSA",
            "LABEL_인쇄물",
            "기타출하위치",
            "내용물",
            "포장검사",
            "동작검사",
            "내부검사",
            "외관검사",
            "내압검사",
            "내용물확인",
            "가_감전압",
            "HI_POT_내부검사",
            "REMARK",
            "부적합수량",
            "적합수량",
        )
        help_texts = {
            "최종검사코드": "*최종검사코드 앞에 FC를 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "검시일": "*형식 : yyyy-mm-dd",
        }
        widgets = {
            "포장검사": forms.RadioSelect(),
            "동작검사": forms.RadioSelect(),
            "내부검사": forms.RadioSelect(),
            "외관검사": forms.RadioSelect(),
            "내압검사": forms.RadioSelect(),
            "내용물확인": forms.RadioSelect(),
        }

    def clean(self):
        code = self.cleaned_data.get("최종검사코드")
        partner = models.FinalCheckRegister.objects.filter(최종검사코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.add_error("최종검사코드", forms.ValidationError("*해당 최종검사코드는 이미 존재합니다."))
            elif code != "FC":
                self.add_error(
                    "최종검사코드", forms.ValidationError("*최종검사코드는 FC로 시작해야 합니다.")
                )

            return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class FinalCheckEditForm(FinalCheckRegisterForm):
    def clean(self):
        code = self.cleaned_data.get("최종검사코드")
        partner = None
        if code:
            code = code[0:2]
            if partner:
                self.add_error("최종검사코드", forms.ValidationError("*해당 최종검사코드는 이미 존재합니다."))
            elif code != "FC":
                self.add_error(
                    "최종검사코드", forms.ValidationError("*최종검사코드는 FC로 시작해야 합니다.")
                )

            return self.cleaned_data
