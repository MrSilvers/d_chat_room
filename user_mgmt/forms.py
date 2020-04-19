from django import forms
from django.core.exceptions import ValidationError

from .models import UserTbl

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput()
    )
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(
            render_value=True,
            )
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = UserTbl.objects.filter(username=username)
        if not user.exists():
            raise ValidationError({'username':"username is not exist."})
        user = user.first()
        if password != user.password:
            raise ValidationError({"password":"password is error."})
        return self.cleaned_data

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label="Password",
        widget=forms.widgets.PasswordInput(
            render_value=True,
        )
    )
    password1 = forms.CharField(
        label="Repeat Password",
        widget=forms.widgets.PasswordInput(
            render_value=True,
        )
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise ValidationError({'password1':"different from password input."})
        if UserTbl.objects.filter(username=username).exists():
            raise ValidationError({"username":"username already exist."})
        return self.cleaned_data
