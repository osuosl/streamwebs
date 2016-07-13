from __future__ import unicode_literals
from streamwebs.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean_password(self):
        if self.data['password'] != self.data['password_check']:
            raise forms.ValidationError('Passwords do not match')
        return self.data['password']


class UserProfileForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = UserProfile
        fields = ('school', 'birthdate')
