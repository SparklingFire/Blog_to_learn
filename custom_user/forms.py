from django import forms
from . import models
from custom_user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("The user doesn't exist or is not activated")
        return username