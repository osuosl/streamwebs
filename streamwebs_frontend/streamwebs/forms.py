# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from streamwebs.models import UserProfile, WQ_Sample, Water_Quality
from streamwebs.models import Canopy_Cover, CC_Cardinal
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput()) \
                .label = _('Password')
    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password')

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
    class Meta:
        model = UserProfile
        fields = ('school', 'birthdate')
        labels = {
            'school': _('School'),
            'birthdate': _('Birthdate'),
        }


class WQForm(forms.ModelForm):
    class Meta:
        model = Water_Quality
        fields = ('site', 'date', 'DEQ_wq_level', 'latitude',
                  'longitude', 'fish_present', 'live_fish',
                  'dead_fish', 'water_temp_unit',
                  'air_temp_unit', 'notes')
        labels = {'site': _('Stream/Site name:'),
                  'date': _('Date:'),
                  'DEQ_wq_level': _('DEQ Data Quality Level:'),
                  'latitude': _('Latitude:'),
                  'longitude': _('Longitude:'),
                  'fish_present': _('Any fish present?'),
                  'live_fish': _('Number of live fish:'),
                  'dead_fish': _('Number of dead fish:'),
                  'water_temp_unit': _('Water Temperature Units'),
                  'air_temp_unit': _('Air Temperature Units'),
                  'notes': _('Field Notes:'),
                  }


class WQSampleForm(forms.ModelForm):
    class Meta:
        model = WQ_Sample
        fields = ('water_temperature', 'air_temperature', 'dissolved_oxygen',
                  'pH', 'turbidity', 'salinity', 'conductivity',
                  'total_solids', 'bod', 'ammonia', 'nitrite',
                  'nitrate', 'phosphates', 'fecal_coliform')
        labels = {'water_temperature': _('Water Temperature:'),
                  'air_temperature': _('Air Temperature:'),
                  'dissolved_oxygen': _('Dissolved Oxygen (mg/L):'),
                  'pH': _('pH:'),
                  'turbidity': _('Turbidity (NTU):'),
                  'salinity': _('Salinity (PSU) PPT:'),
                  'conductivity': _('Conductivity (µS/cm):'),
                  'total_solids': _('Total Solids (mg/L):'),
                  'bod': _('BOD (mg/L):'),
                  'ammonia': _('Ammonia (mg/L):'),
                  'nitrite': _('Nitrite (mg/L):'),
                  'nitrate': _('Nitrate (mg/L):'),
                  'phosphates': _('Phosphates (mg/L):'),
                  'fecal_coliform': _('Fecal Coliform (CFU/100 mL):'),
                  }


class Canopy_Cover_Form(forms.ModelForm):
    class Meta:
        model = Canopy_Cover
        fields = ('school', 'date_time', 'site', 'weather', 'north', 'east',
                  'south', 'west', 'est_canopy_cover')
        labels = {
            'school': _('School'),
            'est_canopy_cover': _('Estimated Canopy Cover'),
        }


class CC_Cardinal_Form(forms.ModelForm):
    class Meta:
        model = CC_Cardinal
        fields = ('direction', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                  'V', 'W', 'X', 'num_shaded')
        A = forms.BooleanField(initial=False, required=False)
        labels = {
            'direction': _('Direction'),
            'num_shaded': _('Number Shaded')
        }
