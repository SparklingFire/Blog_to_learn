from django import forms
from custom_user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
import re


class PasswordRecoveryForm(forms.Form):
    email = forms.CharField(label='Введите электронный адрес')

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            self.user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Такая почта не зарегистрирована')
        return email


class PasswordResetForm(forms.Form):
    new_password_1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    new_password_2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    def clean_new_password_2(self):
        new_password_1 = self.cleaned_data.get('new_password_1')
        new_password_2 = self.cleaned_data.get('new_password_2')
        if len(new_password_1) < 5:
            raise forms.ValidationError('Пароль слишком короткий')
        if new_password_1 != new_password_2:
            raise forms.ValidationError('Пароли не совпадают')
        return new_password_1


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Старый пароль')
    new_password_1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    new_password_2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def cleaned_data(self):
        old_password = self.cleaned_data.get('old_password')
        new_password_1 = self.cleaned_data.get('new_password_1')
        new_password_2 = self.cleaned_data.get('new_password_2')
        try:
            authenticate(username=self.user.username,
                         password=old_password)
        except:
            raise forms.ValidationError('Неверный пароль')
        if len(new_password_1) < 5:
            raise forms.ValidationError('Пароль слишком короткий')
        if new_password_1 != new_password_2:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data
