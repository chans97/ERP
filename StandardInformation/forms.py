from django import forms
from . import models
from users.models import User


class UploadPartnerForm(forms.ModelForm):
    class Meta:
        model = models.Partner
        fields = (
            "거래처구분",
            "거래처코드",
            "거래처명",
            "사업자등록번호",
            "담당자",
            "연락처",
            "이메일",
            "사업장주소",
            "사업자등록증첨부",
            "사용여부",
            "특이사항",
        )
        help_texts = {
            "거래처코드": "*거래처코드 앞에 PN을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "연락처": "*연락처는 '-'을 제외하고 숫자만 입력해주시길 바랍니다. ",
        }

    def clean(self):
        code = self.cleaned_data.get("거래처코드")
        partner = models.Partner.objects.filter(거래처코드=code)
        partner = list(partner)
        code = code[0:2]
        if partner:
            self.add_error("거래처코드", forms.ValidationError("*해당 거래처코드는 이미 존재합니다."))
        elif code != "PN":
            self.add_error("거래처코드", forms.ValidationError("*거래처 코드는 PN으로 시작해야 합니다."))

            return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner


class UploadSingleForm(forms.ModelForm):
    class Meta:
        model = models.SingleProduct
        fields = (
            "모델코드",
            "모델명",
            "규격",
            "단위",
            "단가",
        )
        help_texts = {
            "모델코드": "*모델코드 앞에 SP를 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "단가": "*단가는 '원'을 제외하고 숫자만 입력해주시길 바랍니다. ",
        }

    def clean(self):
        code = self.cleaned_data.get("모델코드")
        single = models.SingleProduct.objects.filter(모델코드=code)
        single = list(single)
        code = code[0:2]
        if single:
            self.add_error("모델코드", forms.ValidationError("*해당 모델코드는 이미 존재합니다."))
        elif code != "SP":
            self.add_error("모델코드", forms.ValidationError("*단품 모델코드는 SP로 시작해야 합니다."))
        else:
            return self.cleaned_data

    def save(self, *arg, **kwargs):
        single = super().save(commit=False)
        return single


class UploadSingleMaterialForm(forms.Form):
    단품구성자재 = forms.CharField()
    수량 = forms.CharField()

    def clean(self):
        singlematerial = self.cleaned_data.get("단품구성자재")
        material = models.Material.objects.get_or_none(자재코드=singlematerial)

        if material is None:
            self.add_error("단품구성자재", forms.ValidationError("*해당 자재코드는 없는 자재코드입니다."))
        else:
            self.cleaned_data["단품구성자재"] = material
            return self.cleaned_data


class UploadRackForm(forms.ModelForm):
    class Meta:
        model = models.RackProduct
        fields = (
            "랙시리얼코드",
            "랙모델명",
            "규격",
            "단위",
            "단가",
        )
        help_texts = {
            "랙시리얼코드": "*랙시리얼코드 앞에 RP를 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "단가": "*단가는 '원'을 제외하고 숫자만 입력해주시길 바랍니다. ",
        }

    def clean(self):
        code = self.cleaned_data.get("랙시리얼코드")
        rack = models.RackProduct.objects.filter(랙시리얼코드=code)
        rack = list(rack)
        code = code[0:2]
        if rack:
            self.add_error("랙시리얼코드", forms.ValidationError("*해당 모델코드는 이미 존재합니다."))
        elif code != "RP":
            self.add_error("랙시리얼코드", forms.ValidationError("*랙시리얼코드는 RP로 시작해야 합니다."))
        else:
            return self.cleaned_data

    def save(self, *arg, **kwargs):
        rack = super().save(commit=False)
        return rack


class UploadRackSingleForm(forms.Form):
    랙구성단품 = forms.CharField()
    수량 = forms.CharField()

    def clean(self):
        racksingle = self.cleaned_data.get("랙구성단품")
        single = models.SingleProduct.objects.get_or_none(모델코드=racksingle)

        if single is None:
            self.add_error("랙구성단품", forms.ValidationError("*해당 모델코드는 없는 자재코드입니다."))
        else:
            self.cleaned_data["랙구성단품"] = single
            return self.cleaned_data


class UploadRackMaterialForm(forms.Form):
    랙구성자재 = forms.CharField()
    수량 = forms.CharField()

    def clean(self):
        rackmaterial = self.cleaned_data.get("랙구성자재")
        material = models.Material.objects.get_or_none(자재코드=rackmaterial)

        if material is None:
            self.add_error("랙구성자재", forms.ValidationError("*해당 자재코드는 없는 자재코드입니다."))
        else:
            self.cleaned_data["랙구성자재"] = material
            return self.cleaned_data
