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
    user_name = forms.CharField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def clean(self):
        username = self.cleaned_data.get("username")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError({'password2':"different from password input."})
        if UserTbl.objects.filter(username=username).exists():
            raise ValidationError({"username":"username already exist."})
        return self.cleaned_data
