from django import forms
from django.forms import ModelForm

#To set a class -> (widget=forms.TextInput(attrs={'class': 'my_class'}))

class LoginForm(forms.Form):
    user_wf = forms.CharField(max_length=65)
    # password_wf = forms.CharField(max_length=65, widget=forms.PasswordInput, required=False)

class TaskForm(forms.Form):
    data = forms.CharField(max_length=255)
