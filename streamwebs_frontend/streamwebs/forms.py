from __future__ import unicode_literals
from streamwebs.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput()) \
                    .label = _('Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password': _('Password:'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('school', 'birthdate')
        labels = {
            'school': _('School'),
            'birthdate': _('Birthdate'),
        }
