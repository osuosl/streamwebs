# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from streamwebs.models import UserProfile, WQ_Sample, Water_Quality, \
    Macroinvertebrates, Canopy_Cover, CC_Cardinal, TransectZone, \
    RiparianTransect, Resource
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


class MacroinvertebratesForm(forms.ModelForm):
    class Meta:
        model = Macroinvertebrates
        fields = ('school', 'date_time', 'weather', 'site', 'time_spent',
                  'num_people', 'riffle', 'pool', 'caddisfly', 'mayfly',
                  'riffle_beetle', 'stonefly', 'water_penny', 'dobsonfly',
                  'clam_or_mussel', 'crane_fly', 'crayfish',
                  'damselfly', 'dragonfly', 'scud', 'fishfly', 'alderfly',
                  'mite', 'aquatic_worm', 'blackfly', 'leech', 'midge',
                  'snail', 'mosquito_larva', 'wq_rating',
                  'somewhat_sensitive_total', 'sensitive_total',
                  'tolerant_total')


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


class TransectZoneForm(forms.ModelForm):
    class Meta:
        model = TransectZone
        fields = ('conifers', 'hardwoods', 'shrubs', 'comments')


class Resource_Data_Sheet_Form(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('name', 'res_type', 'downloadable', 'thumbnail')


class Resource_Publication_Form(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('name', 'res_type', 'downloadable', 'thumbnail')


class RiparianTransectForm(forms.ModelForm):
    class Meta:
        model = RiparianTransect
        fields = ('school', 'date_time', 'weather', 'site', 'slope', 'notes')
