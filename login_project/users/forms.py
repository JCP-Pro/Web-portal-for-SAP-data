from django import forms
from django.forms import ModelForm

class LoginForm(forms.Form):
    user_wf = forms.CharField(max_length=65)
    # password_wf = forms.CharField(max_length=65, widget=forms.PasswordInput, required=False)