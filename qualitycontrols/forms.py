from django import forms
from . import models
from StandardInformation import models as SI_models
from measures import models as MS_models
from specials import models as S_models
from stockmanages import models as SM_models


class FinalCheckRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["최종검사코드"].widget.attrs.update(size="20")

    class Meta:
        model = models.FinalCheckRegister
        fields = (
            "최종검사코드",
            "검시일",
            "치명적불량",
            "중불량",
            "경불량",
            "검사수준",
            "샘플링방식",
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
        self.is_bound = False
        code = self.cleaned_data.get("최종검사코드")
        partner = models.FinalCheckRegister.objects.filter(최종검사코드=code)
        partner = list(partner)
        if code:
            self.is_bound = True
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
        self.is_bound = False
        code = self.cleaned_data.get("수입검사코드")
        partner = models.MaterialCheck.objects.filter(수입검사코드=code)
        partner = list(partner)
        if code:
            self.is_bound = True
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
        self.is_bound = False
        code = self.cleaned_data.get("자재부적합코드")
        partner = models.LowMetarial.objects.filter(자재부적합코드=code)
        partner = list(partner)
        if code:
            self.is_bound = True
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


class measureeditForm(forms.ModelForm):
    class Meta:
        model = SI_models.Measure
        fields = (
            "계측기코드",
            "계측기명",
            "자산관리번호",
            "계측기규격",
            "설치년월일",
            "사용공정명",
            "설치장소",
            "file",
        )
        help_texts = {
            "계측기코드": "*계측기코드 앞에 MS을 붙여주시길 바랍니다.",
            "설치년월일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        labels = {"file": "계측기사진"}

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


"""    def clean(self):
        code = self.cleaned_data.get("계측기코드")
        partner = SI_models.Measure.objects.filter(계측기코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.add_error("계측기코드", forms.ValidationError("*해당 계측기코드는 이미 존재합니다."))
            elif code != "MS":
                self.add_error("계측기코드", forms.ValidationError("*계측기코드는 MS로 시작해야 합니다."))

            return self.cleaned_data
"""


class measurecheckeditForm(forms.ModelForm):
    class Meta:
        model = MS_models.MeasureCheckRegister
        fields = (
            "점검일",
            "점검내용",
            "특이사항",
        )
        help_texts = {
            "점검일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class measurecheckregisterForm(forms.ModelForm):
    계측기 = forms.CharField(max_length=20, required=True)

    class Meta:
        model = MS_models.MeasureCheckRegister
        fields = (
            "점검일",
            "점검내용",
            "특이사항",
        )
        help_texts = {
            "점검일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }

    def clean(self):
        code = self.cleaned_data.get("계측기")
        partner = SI_models.Measure.objects.get_or_none(pk=code)
        if code:
            if partner:
                self.cleaned_data["계측기"] = partner
                return self.cleaned_data
            else:
                self.add_error("계측기", forms.ValidationError("*올바른 입력값이 아닙니다."))

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class measurerepaireditForm(forms.ModelForm):
    class Meta:
        model = MS_models.MeasureRepairRegister
        fields = (
            "수리일",
            "수리내용",
            "특이사항",
            "수리부문",
            "file",
        )
        help_texts = {
            "수리일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        labels = {"수리현장사진": "계측기사진"}

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class measurerepairregisterForm(forms.ModelForm):
    계측기 = forms.CharField(max_length=20, required=True)

    class Meta:
        model = MS_models.MeasureRepairRegister
        fields = (
            "수리일",
            "수리내용",
            "특이사항",
            "수리부문",
            "file",
        )
        help_texts = {
            "수리일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        labels = {"file": "수리현장사진"}

    def clean(self):
        code = self.cleaned_data.get("계측기")
        partner = SI_models.Measure.objects.get_or_none(pk=code)
        if code:
            if partner:
                self.cleaned_data["계측기"] = partner
                return self.cleaned_data
            else:
                self.add_error("계측기", forms.ValidationError("*올바른 입력값이 아닙니다."))

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class measureregisterForm(forms.ModelForm):
    class Meta:
        model = SI_models.Measure
        fields = (
            "계측기코드",
            "계측기명",
            "자산관리번호",
            "계측기규격",
            "설치년월일",
            "사용공정명",
            "설치장소",
            "file",
        )
        help_texts = {
            "계측기코드": "*계측기코드 앞에 MS을 붙여주시길 바랍니다.",
            "설치년월일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        labels = {"file": "계측기사진"}

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("계측기코드")
        partner = SI_models.Measure.objects.filter(계측기코드=code)
        partner = list(partner)
        if code:
            self.is_bound = True
            code = code[0:2]
            if partner:
                self.add_error("계측기코드", forms.ValidationError("*해당 계측기코드는 이미 존재합니다."))
            elif code != "MS":
                self.add_error("계측기코드", forms.ValidationError("*계측기코드는 MS로 시작해야 합니다."))

            return self.cleaned_data


class SpecialRegisterForm(forms.ModelForm):
    class Meta:
        model = S_models.SpecialRegister
        fields = (
            "특채등록일",
            "특채수량",
        )
        help_texts = {
            "특채등록일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("특채수량")
        if code:
            self.is_bound = True
            return self.cleaned_data


class specialconductregisterForm(forms.ModelForm):
    class Meta:
        model = S_models.SpecialConductRegister
        fields = ("특채수량중납품수량",)

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("특채수량중납품수량")
        if code:
            self.is_bound = True
            return self.cleaned_data


class specialrejectregisterForm(forms.ModelForm):
    class Meta:
        model = S_models.SpecialRejectRegister
        fields = ("특채반품수량",)

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("특채반품수량")
        if code:
            self.is_bound = True
            return self.cleaned_data


class materialoutrequest(forms.ModelForm):
    자재 = forms.CharField(max_length=20)

    class Meta:
        model = SM_models.StockOfMaterialOutRequest
        fields = (
            "출고요청수량",
            "출고요청일",
            "출고유형",
        )
        widgets = {
            "출고유형": forms.RadioSelect(),
        }
        help_texts = {
            "출고요청일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("자재")
        material = SI_models.Material.objects.get_or_none(자재코드=code)

        if code:
            self.is_bound = True
            self.cleaned_data["자재"] = material
            return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner
