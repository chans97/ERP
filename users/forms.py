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
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


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
            raise forms.ValidationError("*This email already occupied")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data["password1"]
        if password != password1:
            raise forms.ValidationError("*Password confirmation does not match")
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
