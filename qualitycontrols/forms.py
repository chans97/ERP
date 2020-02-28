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
            "검시일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
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


class MaterialCheckRegisterForm(forms.ModelForm):
    class Meta:
        model = models.MaterialCheck
        fields = (
            "수입검사코드",
            "검사지침서번호",
            "검사일자",
            "검사항목",
            "판정기준",
            "시료크기",
            "합격수량",
            "불합격수량",
            "불합격내용",
        )
        help_texts = {
            "수입검사코드": "*수입검사코드 앞에 MR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "검사일자": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }

    def clean(self):
        code = self.cleaned_data.get("수입검사코드")
        partner = models.MaterialCheck.objects.filter(수입검사코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.add_error("수입검사코드", forms.ValidationError("*해당 수입검사코드는 이미 존재합니다."))
            elif code != "MR":
                self.add_error(
                    "수입검사코드", forms.ValidationError("*수입검사코드는 MR로 시작해야 합니다.")
                )

            return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class LowMetarialRegisterForm(forms.ModelForm):
    class Meta:
        model = models.LowMetarial
        fields = (
            "자재부적합코드",
            "검토일",
            "부적합자재의내용과검토방안",
            "처리방안",
        )
        help_texts = {
            "자재부적합코드": "*수입검사코드 앞에 LR을 붙여주시길 바랍니다.",
            "검토일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        widgets = {
            "처리방안": forms.RadioSelect(),
        }

    def clean(self):
        code = self.cleaned_data.get("자재부적합코드")
        partner = models.LowMetarial.objects.filter(자재부적합코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.add_error(
                    "자재부적합코드", forms.ValidationError("*해당 자재부적합코드는 이미 존재합니다.")
                )
            elif code != "LR":
                self.add_error(
                    "자재부적합코드", forms.ValidationError("*자재부적합코드는 LR로 시작해야 합니다.")
                )

            return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class LowMetarialEditForm(LowMetarialRegisterForm):
    def clean(self):
        code = self.cleaned_data.get("자재부적합코드")
        if code:
            code = code[0:2]
            if code != "LR":
                self.add_error(
                    "자재부적합코드", forms.ValidationError("*자재부적합코드는 LR로 시작해야 합니다.")
                )

            return self.cleaned_data


class MaterialCheckEditForm(MaterialCheckRegisterForm):
    def clean(self):
        code = self.cleaned_data.get("수입검사코드")
        if code:
            code = code[0:2]
            if code != "MR":
                self.add_error(
                    "수입검사코드", forms.ValidationError("*수입검사코드는 MR로 시작해야 합니다.")
                )

            return self.cleaned_data
