from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Passward"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀렸습니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지 않는 사용자입니다."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "부서", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "부서": forms.CheckboxSelectMultiple(),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    field_order = [
        "first_name",
        "email",
        "password",
        "password1",
        "부서",
    ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = models.User.objects.get(username=email)
            raise forms.ValidationError("*이미 존제하는 이메일입니다.")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data["password1"]
        if password != password1:
            raise forms.ValidationError("*확인 비밀번호가 같지 않습니다.")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.nowPart = self.cleaned_data.get("부서")[0]
        user.save()


class ForgotEmailForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "부서",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "부서": forms.CheckboxSelectMultiple(),
        }

    field_order = [
        "first_name",
        "부서",
    ]


class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "부서", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "부서": forms.CheckboxSelectMultiple(),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    field_order = [
        "first_name",
        "email",
        "부서",
    ]
