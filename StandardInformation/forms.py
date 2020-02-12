from django import forms
from . import models
from users.models import User


class UploadRoomForm(forms.ModelForm):
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
            "거래처코드": "*거래처코드 앞에 PN을 붙여주시길 바랍니다.",
            "연락처": "*연락처는 '-'을 제외하고 숫자만 입력해주시길 바랍니다. ",
        }

    def clean(self):
        code = self.cleaned_data.get("거래처코드")
        partner = models.Partner.objects.filter(거래처코드=code)
        partner = list(partner)
        code = code[0:2]
        if partner:
            self.add_error("거래처코드", forms.ValidationError("해당 거래처코드는 이미 존재합니다."))
        elif code != "PN":
            self.add_error("거래처코드", forms.ValidationError("거래처 코드는 PN으로 시작해야 합니다."))

            return self.cleaned_data

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner
