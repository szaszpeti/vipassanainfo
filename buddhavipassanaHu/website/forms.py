from django import forms
from .models import WebsiteRegister


class WebsiteRegisterForm(forms.ModelForm):
    class Meta():
        model = WebsiteRegister
        fields = '__all__'