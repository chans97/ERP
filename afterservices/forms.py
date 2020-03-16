from django import forms
from . import models
from StandardInformation import models as SI_models
from stocksingle import models as SS_models


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
            "현장명",
        )
        help_texts = {
            "접수번호": "*최종검사코드 앞에 AR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "접수일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
            "방문요청일": "*형식 : yyyy-mm-dd",
        }
        widgets = {
            "불량분류": forms.RadioSelect(),
            "접수제품분류": forms.RadioSelect(),
            "대응유형": forms.RadioSelect(),
        }

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("접수번호")
        codep = self.cleaned_data.get("의뢰처")
        partner = models.ASRegisters.objects.filter(접수번호=code)
        partner = list(partner)
        의뢰처 = models.SI_models.CustomerPartner.objects.get_or_none(거래처코드=codep)

        if code:
            self.is_bound = True
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


class ASRegisterEditForm(forms.ModelForm):
    class Meta:
        model = models.ASRegisters
        fields = (
            "접수일",
            "현상",
            "불량분류코드",
            "불량분류",
            "대응유형",
            "의뢰자전화번호",
            "방문요청일",
        )
        help_texts = {
            "접수일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
            "방문요청일": "*형식 : yyyy-mm-dd",
        }
        widgets = {
            "불량분류": forms.RadioSelect(),
            "대응유형": forms.RadioSelect(),
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASvisitRegisterForm(forms.ModelForm):
    class Meta:
        model = models.ASVisitContents
        fields = (
            "AS날짜",
            "AS방법",
            "고객이름",
            "AS처리내역",
            "특이사항",
            "재방문여부",
        )
        help_texts = {
            "AS날짜": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        widgets = {
            "AS방법": forms.RadioSelect(),
            "재방문여부": forms.RadioSelect(),
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASrevisitRegisterForm(forms.ModelForm):
    class Meta:
        model = models.ASReVisitContents
        fields = (
            "AS날짜",
            "AS방법",
            "고객이름",
            "AS처리내역",
            "특이사항",
        )
        help_texts = {
            "AS날짜": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        widgets = {
            "AS방법": forms.RadioSelect(),
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASrepairrequestregisterForm(forms.ModelForm):
    신청품목 = forms.CharField(
        max_length=20,
        required=True,
        help_text="*모델코드로 입력해주시길 바랍니다.",
        widget=forms.TextInput(attrs={"size": "12"}),
    )

    class Meta:
        model = models.ASRepairRequest
        fields = (
            "수리요청코드",
            "신청수량",
        )
        help_texts = {
            "수리요청코드": "*수리요청코드 앞에 RR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order

    def clean(self):
        self.is_bound = False
        cleaned_data = super().clean()
        code = self.cleaned_data.get("수리요청코드")
        codep = self.cleaned_data.get("신청품목")
        partner = models.ASRepairRequest.objects.filter(수리요청코드=code)
        partner = list(partner)
        single = SI_models.SingleProduct.objects.get_or_none(모델코드=codep)
        if code:
            code = code[0:2]
            if partner:
                self.is_bound = True
                self.add_error("수리요청코드", forms.ValidationError("*해당 수리요청코드는 이미 존재합니다."))
            elif code != "RR":
                self.is_bound = True
                self.add_error("수리요청코드", forms.ValidationError("*수리요청코드 RR로 시작해야 합니다."))
            elif single is None:
                self.is_bound = True
                self.add_error("신청품목", forms.ValidationError("*해당 단품을 찾을 수 없습니다."))
            else:
                self.cleaned_data["신청품목"] = single
                return self.cleaned_data


class ASrepairrequestregisterRackForm(forms.Form):

    수리요청코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text=f"*수리요청코드 앞에 RR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        widget=forms.TextInput(attrs={"size": "12"}),
    )
    신청수량 = forms.IntegerField()
    신청품목 = forms.CharField()

    def clean(self):
        self.is_bound = False
        cleaned_data = super().clean()
        code = self.cleaned_data.get("수리요청코드")
        partner = models.ASRepairRequest.objects.filter(수리요청코드=code)
        partner = list(partner)
        if code:
            code = code[0:2]
            if partner:
                self.is_bound = True
                self.add_error("수리요청코드", forms.ValidationError("*해당 수리요청코드는 이미 존재합니다."))
            elif code != "RR":
                self.is_bound = True
                self.add_error("수리요청코드", forms.ValidationError("*수리요청코드 RR로 시작해야 합니다."))
            else:
                return self.cleaned_data

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASsingleoutrequestregistersingleForm(forms.ModelForm):
    class Meta:
        model = SS_models.StockOfSingleProductOutRequest
        fields = (
            "출하요청수량",
            "출하희망일",
        )
        help_texts = {
            "출하희망일": "*형식 : yyyy-mm-dd(필수가 아닙니다.)",
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASsingleoutrequestregisterrackForm(forms.Form):

    출하희망일 = forms.DateField(required=False, help_text="*형식 : yyyy-mm-dd(필수가 아닙니다.)")
    출하요청수량 = forms.IntegerField(widget=forms.NumberInput(attrs={"min": "0"}))
    신청품목 = forms.CharField()

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order
