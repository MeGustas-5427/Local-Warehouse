from django import forms
from adviser.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = adviser_user
        widgets = {
        'password': forms.PasswordInput(),
    }