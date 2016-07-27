from __future__ import unicode_literals
from streamwebs.models import UserProfile, Macroinvertebrates
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
    password = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password')

    def clean_password(self):
        if self.data['password'] != self.data['password_check']:
            raise forms.ValidationError('Passwords do not match')
        return self.data['password']


class UserProfileForm(forms.ModelForm):
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
        labels = {
            'school': _('School'),
            'birthdate': _('Birthdate'),
        }
