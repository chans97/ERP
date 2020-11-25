from django import forms
from . import models
from StandardInformation import models as SI_models
from stocksingle import models as SS_models


class ASRegisterForm(forms.ModelForm):
    class Meta:
        model = models.ASRegisters
        fields = (
            "접수번호",
            "접수일",
            "설치연도",
            "비용",
            "현장명",
            "의뢰자전화번호",
            "주소",
            "접수내용",
            "처리방법",
            "첨부파일",
            "비고",
        )
        help_texts = {
            "접수번호": "*최종검사코드 앞에 AR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
            "접수일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        widgets = {
            "처리방법": forms.RadioSelect(),
            "비용": forms.RadioSelect(),
        }

    def clean(self):
        self.is_bound = False
        code = self.cleaned_data.get("접수번호")
        partner = models.ASRegisters.objects.filter(접수번호=code)
        partner = list(partner)

        if code:
            self.is_bound = True
            code = code[0:2]
            if partner:
                self.add_error("접수번호", forms.ValidationError("*해당 접수번호는 이미 존재합니다."))
            elif code != "AR":
                self.add_error("접수번호", forms.ValidationError("*접수번호는 AR로 시작해야 합니다."))
            else:
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
            "접수내용",
            "의뢰자전화번호",
            "비용",
        )
        help_texts = {
            "접수일": "*형식 : yyyy-mm-dd(기본값은 오늘입니다.)",
        }
        widgets = {
            "비용": forms.RadioSelect(),
        }

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASvisitRegisterForm(forms.ModelForm):
    class Meta:
        model = models.ASVisitContents
        fields = ("AS날짜", "AS방법", "처리기사", "처리회사", "AS처리내역", "특이사항", "재방문여부", "하자파일")
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
            "고객성명",
            "고객주소",
            "고객전화",
            "고객팩스",
            "AS의뢰내용",
            "시리얼번호",
            "사용자액세서리",
            "택배관련",
            "신청수량",
        )
        help_texts = {
            "수리요청코드": "*수리요청코드 앞에 RR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        }
        widgets = {
            "택배관련": forms.RadioSelect(),
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
    택배관련_CHOICES = (
        ("선불", "선불"),
        ("착불", "착불"),
    )

    수리요청코드 = forms.CharField(
        max_length=20,
        required=True,
        help_text=f"*수리요청코드 앞에 RR을 붙여주시길 바랍니다.(한 번 설정하면, 바꿀 수 없습니다.)",
        widget=forms.TextInput(attrs={"size": "12"}),
    )
    신청수량 = forms.IntegerField()
    신청품목 = forms.CharField()
    고객성명 = forms.CharField()
    고객주소 = forms.CharField()
    고객전화 = forms.CharField()
    고객팩스 = forms.CharField()
    AS의뢰내용 = forms.CharField()
    시리얼번호 = forms.CharField()
    사용자액세서리 = forms.CharField()
    택배관련 = forms.ChoiceField(choices=택배관련_CHOICES, widget=forms.RadioSelect())

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


class ASdoneinsideForm(forms.ModelForm):
    class Meta:
        model = models.ASResults
        fields = ("처리내용",)

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order


class ASconductForm(forms.ModelForm):
    class Meta:
        model = models.ASRegisters
        fields = ()
        widgets = {}

    def save(self, *arg, **kwargs):
        order = super().save(commit=False)
        return order

