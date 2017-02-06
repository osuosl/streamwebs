# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from streamwebs.models import UserProfile, WQ_Sample, Water_Quality, \
    Macroinvertebrates, Canopy_Cover, TransectZone, \
    RiparianTransect, PhotoPointImage, PhotoPoint, CameraPoint, Site, School, \
    Soil_Survey
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Password'))

    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password')

    email = forms.CharField(required=True)
    first_name = forms.CharField(
        widget=forms.TextInput()
    )

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
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = UserProfile
        fields = ('school', 'birthdate')


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    ''' Renders radio buttons horizontally '''
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class MacroinvertebratesForm(forms.ModelForm):
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = Macroinvertebrates
        fields = ('school', 'date_time', 'weather', 'time_spent',
                  'num_people', 'water_type', 'caddisfly', 'mayfly',
                  'riffle_beetle', 'stonefly', 'water_penny', 'dobsonfly',
                  'clam_or_mussel', 'crane_fly', 'crayfish',
                  'damselfly', 'dragonfly', 'scud', 'fishfly', 'alderfly',
                  'mite', 'aquatic_worm', 'blackfly', 'leech', 'midge',
                  'snail', 'mosquito_larva', 'notes')


class WQForm(forms.ModelForm):
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = Water_Quality
        widgets = {
            'fish_present':
                forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'water_temp_unit':
                forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'air_temp_unit':
                forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'notes':
                forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = (
            'date', 'DEQ_dq_level', 'school',
            'latitude', 'longitude', 'fish_present', 'live_fish',
            'dead_fish', 'water_temp_unit', 'air_temp_unit', 'notes'
        )


class WQFormReadOnly(WQForm):
    def __init__(self, *args, **kwargs):
        super(WQFormReadOnly, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'disabled': True})


class WQSampleForm(forms.ModelForm):
    class Meta:
        model = WQ_Sample
        widgets = {
            'water_temp_tool':
                forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'air_temp_tool':
                forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'oxygen_tool': forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'pH_tool': forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'turbid_tool': forms.RadioSelect(renderer=HorizontalRadioRenderer),
            'salt_tool': forms.RadioSelect(renderer=HorizontalRadioRenderer)
        }
        fields = (
            'water_temperature', 'water_temp_tool',
            'air_temperature', 'air_temp_tool',
            'dissolved_oxygen', 'oxygen_tool',
            'pH', 'pH_tool',
            'turbidity', 'turbid_tool',
            'salinity', 'salt_tool',
            'conductivity', 'total_solids',
            'bod', 'ammonia',
            'nitrite', 'nitrate',
            'phosphates', 'fecal_coliform'
        )


class WQSampleFormReadOnly(WQSampleForm):
    def __init__(self, *args, **kwargs):
        super(WQSampleFormReadOnly, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'disabled': True})


class Canopy_Cover_Form(forms.ModelForm):
    class Meta:
        model = Canopy_Cover
        fields = ('school', 'date_time', 'weather', 'est_canopy_cover',
                  'north_cc', 'west_cc', 'east_cc', 'south_cc')


class TransectZoneForm(forms.ModelForm):
    class Meta:
        model = TransectZone
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = ('conifers', 'hardwoods', 'shrubs', 'comments')


class RiparianTransectForm(forms.ModelForm):
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = RiparianTransect
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = ('school', 'date_time', 'weather', 'slope', 'notes')


class PhotoPointImageForm(forms.ModelForm):
    class Meta:
        model = PhotoPointImage
        fields = ('image', 'date')


class PhotoPointForm(forms.ModelForm):
    class Meta:
        model = PhotoPoint
        fields = ('camera_point', 'pp_date', 'compass_bearing', 'distance',
                  'camera_height', 'notes')


class CameraPointForm(forms.ModelForm):
    class Meta:
        model = CameraPoint
        fields = ('site', 'cp_date', 'location', 'map_datum', 'description')


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('site_name', 'description', 'location', 'image')


class SoilSurveyForm(forms.ModelForm):
    class Meta:
        model = Soil_Survey
        widgets = {
            'landscape_pos': forms.RadioSelect(),
            'cover_type': forms.RadioSelect(),
            'land_use': forms.RadioSelect(),
            'site_char':
                forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = (
            'school', 'date', 'weather', 'landscape_pos', 'cover_type',
            'land_use', 'soil_type', 'distance', 'site_char'
        )


class SoilSurveyFormReadOnly(SoilSurveyForm):
    def __init__(self, *args, **kwargs):
        super(SoilSurveyFormReadOnly, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'disabled': True})


class StatisticsForm(forms.Form):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label=_('starting from'), required=False
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label=_('ending on'), required=False
    )
