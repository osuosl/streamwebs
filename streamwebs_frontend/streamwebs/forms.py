# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from streamwebs.models import UserProfile, WQ_Sample, Water_Quality
from streamwebs.models import Canopy_Cover, CC_Cardinal
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput()) \
                .label = _('Password')
    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password')
    email = forms.CharField(required=True)

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

    def clean_password(self):
        if self.data['password'] != self.data['password_check']:
            raise forms.ValidationError(_('Passwords do not match'))
        return self.data['password']


class UserProfileForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = UserProfile
        fields = ('school', 'birthdate')


class WQForm(forms.ModelForm):
    class Meta:
        model = Water_Quality
        fields = ('site', 'date', 'DEQ_dq_level', 'latitude',
                  'longitude', 'fish_present', 'live_fish',
                  'dead_fish', 'water_temp_unit',
                  'air_temp_unit', 'notes')


class WQSampleForm(forms.ModelForm):
    class Meta:
        model = WQ_Sample
        fields = ('water_temperature', 'air_temperature', 'dissolved_oxygen',
                  'pH', 'turbidity', 'salinity', 'conductivity',
                  'total_solids', 'bod', 'ammonia', 'nitrite',
                  'nitrate', 'phosphates', 'fecal_coliform')


class Canopy_Cover_Form(forms.ModelForm):
    class Meta:
        model = Canopy_Cover
        fields = ('school', 'date_time', 'site', 'weather', 'north', 'east',
                  'south', 'west', 'est_canopy_cover')


class CC_Cardinal_Form(forms.ModelForm):
    class Meta:
        model = CC_Cardinal
        fields = ('direction', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                  'V', 'W', 'X', 'num_shaded')
