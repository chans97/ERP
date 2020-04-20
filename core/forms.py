from django import forms
from . import models
from users.models import User
from StandardInformation import models as SI_models


class partnermigrate(forms.ModelForm):
    class Meta:
        model = models.partnermigrate
        fields = ("Excelfile",)

    def save(self, *arg, **kwargs):
        partner = super().save(commit=False)
        return partner
