# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from streamwebs.models import UserProfile, WQ_Sample, Water_Quality, \
    Macroinvertebrates, Canopy_Cover, TransectZone, \
    RiparianTransect, PhotoPointImage, PhotoPoint, CameraPoint, Site, School, \
    Soil_Survey, Resource, RipAquaticSurvey
from django.contrib.auth.models import User
from django import forms
from django.forms import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

TIME_PERIOD_CHOICES = (
    ('AM', _('AM')),
    ('PM', _('PM'))
)


def clean_unique_lower(form, field, exclude_initial=True,
                       error_message="The %(field)s %(value)s\
                                     must be unique."):
    value = form.cleaned_data.get(field)
    lower_value = ''.join(value.split()).lower()

    if lower_value:
        qset = form._meta.model._default_manager.filter(**{field: lower_value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qset = qset.exclude(**{field: initial_value})
        if qset.count() > 0:
            raise forms.ValidationError(
                error_message % {'field': field, 'value': lower_value})
    return lower_value


def clean_password_validators(self):
    password = self.data['password']

    # Call password validators
    validate_password(password)

    if self.data['password'] != self.data['password_check']:
        raise forms.ValidationError(_('Passwords did not match'))
    return self.data['password']


class UserFormOptionalNameEmail(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    email = forms.CharField(required=False)

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Password'))

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
        }

    def clean_password(self):
        return clean_password_validators(self)

    def clean_email(self):
        return clean_unique_lower(self, 'email', error_message=u'A user with \
                                  that email address already exists.')


class UserFormEmailAsUsername(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Password'))

    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password')

    email = forms.CharField(
        required=True, widget=forms.TextInput(),
        label='Email Address', validators=[validate_email])

    first_name = forms.CharField(
        widget=forms.TextInput()
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        labels = {
            'email': _('Email Address'),
            'password': _('Password:'),
            'first_name': _('First Name'),
        }

    def clean_password(self):
        return clean_password_validators(self)

    def clean_email(self):
        return clean_unique_lower(self, 'email', error_message=u'A user with \
                                  that email address already exists.')


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    email = forms.CharField(required=False)

    class Meta:
        model = User
        # Add all the fields you want a user to change
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_email(self):
        return clean_unique_lower(self, 'email', error_message=u'A user with \
                                  that email address already exists.')


class UserEmailForm(forms.ModelForm):
    email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        return clean_unique_lower(self, 'email', error_message=u'A user with \
                                  that email address already exists.')


class UserPasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Old Password'))
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('New Password'))
    password_check = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('New Password Repeat'))

    class Meta:
        model = User
        fields = ('password',)

    def clean_password(self):
        if self.data['old_password'] == self.data['password']:
            raise forms.ValidationError(_('Your old password and new ' +
                                          'password cannot be the same.'))
        return clean_password_validators(self)


class UserProfileForm(forms.ModelForm):
    captcha = ReCaptchaField()
    school = forms.ModelChoiceField(
        widget=forms.TextInput(),
        queryset=School.objects.all().order_by('name'), empty_label=None)

    class Meta:
        model = UserProfile
        fields = ('school',)


class MacroinvertebratesForm(forms.ModelForm):
    weather = forms.CharField(required=False)
    time_spent = forms.IntegerField(required=False)
    num_people = forms.IntegerField(required=False)
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    time = forms.TimeField(input_formats=['%I:%M'])
    ampm = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, label="AM/PM")

    class Meta:
        model = Macroinvertebrates
        widgets = {
            'notes': forms.Textarea(
                attrs={'class': 'materialize-textarea'})
        }
        fields = ('date', 'time', 'ampm', 'weather', 'time_spent',
                  'num_people', 'water_type', 'caddisfly', 'mayfly',
                  'riffle_beetle', 'stonefly', 'water_penny', 'dobsonfly',
                  'clam_or_mussel', 'crane_fly', 'crayfish',
                  'damselfly', 'dragonfly', 'scud', 'fishfly', 'alderfly',
                  'mite', 'aquatic_worm', 'blackfly', 'leech', 'midge',
                  'snail', 'mosquito_larva', 'notes')


class WQForm(forms.ModelForm):
    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    time = forms.TimeField(input_formats=['%I:%M'])
    ampm = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, label="AM/PM")

    class Meta:
        model = Water_Quality
        widgets = {
            'fish_present': forms.RadioSelect(),
            'water_temp_unit': forms.RadioSelect(),
            'air_temp_unit': forms.RadioSelect(),
            'notes':
                forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = (
            'date', 'time', 'ampm', 'DEQ_dq_level',
            'latitude', 'longitude', 'fish_present', 'live_fish',
            'dead_fish', 'water_temp_unit', 'air_temp_unit', 'notes'
        )


class WQSampleForm(forms.ModelForm):
    water_temperature = forms.DecimalField(required=False)
    air_temperature = forms.DecimalField(required=False)
    dissolved_oxygen = forms.DecimalField(required=False)
    pH = forms.DecimalField(required=False)
    turbidity = forms.DecimalField(required=False)
    salinity = forms.DecimalField(required=False)

    class Meta:
        model = WQ_Sample
        widgets = {
            'water_temp_tool': forms.RadioSelect(),
            'air_temp_tool': forms.RadioSelect(),
            'oxygen_tool': forms.RadioSelect(),
            'pH_tool': forms.RadioSelect(),
            'turbid_tool': forms.RadioSelect(),
            'salt_tool': forms.RadioSelect()
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


class Canopy_Cover_Form(forms.ModelForm):
    weather = forms.CharField(required=False)
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    time = forms.TimeField(input_formats=['%I:%M'])
    ampm = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, label="AM/PM")

    class Meta:
        model = Canopy_Cover
        fields = ('date', 'time', 'ampm', 'weather',
                  'est_canopy_cover', 'north_cc', 'west_cc', 'east_cc',
                  'south_cc')


class TransectZoneForm(forms.ModelForm):
    # The following override is neccessary so that when the user chooses not to
    # fill in an individual zone form in a 5-zone inline formset, the zone form
    # is not ignored and is saved as a new zone object with its model-specified
    # default values of 0 (for the numerical fields) and '' (for the comments
    # field).
    def has_changed(self):
        return True

    class Meta:
        model = TransectZone
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = ('conifers', 'hardwoods', 'shrubs', 'comments')


class BaseZoneInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # still do regular formset cleaning...
        super(BaseZoneInlineFormSet, self).clean()
        if any(self.errors):
            return

        # ...plus custom cleaning to check for blank zones
        blank = 0
        for form in self.forms:
            # if form's conifers, hardwoods, shrubs ALL 0, inc. 'blank' count
            if (form.cleaned_data['conifers'] == 0 and
                    form.cleaned_data['hardwoods'] == 0 and
                    form.cleaned_data['shrubs'] == 0):
                blank += 1

        if blank == 5:
            raise forms.ValidationError(
                _('At least one zone must have at least '
                  + 'one value greater than 0.'))


class RiparianTransectForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    time = forms.TimeField(input_formats=['%I:%M'])
    ampm = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, label="AM/PM")

    class Meta:
        model = RiparianTransect
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = ('date', 'time', 'ampm',
                  'weather', 'slope', 'notes')


class PhotoPointImageForm(forms.ModelForm):
    date = forms.DateField(
        label="Photo Date",
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )

    class Meta:
        model = PhotoPointImage
        fields = ('image', 'date')


class PhotoPointForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'materialize-textarea'}),
        required=False,
    )

    class Meta:
        model = PhotoPoint
        fields = ('compass_bearing', 'distance', 'camera_height', 'notes')


class CameraPointForm(forms.ModelForm):
    cp_date = forms.DateField(
        label='Camera Point Date',
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'materialize-textarea'}),
        required=False
    )

    class Meta:
        model = CameraPoint
        fields = ('site', 'cp_date', 'location', 'map_datum',
                  'description')


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        widgets = {
            'site_name': forms.TextInput(
                attrs={'class': 'materialize-textarea, validate'}),
            'description': forms.Textarea(
                attrs={'class': 'materialize-textarea'})
        }
        fields = ('site_name', 'description', 'location', 'image')


class SoilSurveyForm(forms.ModelForm):
    weather = forms.CharField(required=False)
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    time = forms.TimeField(input_formats=['%I:%M'])
    ampm = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, label="AM/PM")

    class Meta:
        model = Soil_Survey
        widgets = {
            'landscape_pos': forms.RadioSelect(),
            'cover_type': forms.RadioSelect(),
            'land_use': forms.RadioSelect(),
            'site_char':
                forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'notes':
                forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
        fields = (
            'date', 'time', 'ampm', 'weather', 'landscape_pos',
            'cover_type', 'land_use', 'soil_type', 'distance', 'site_char',
            'notes'
        )


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('name', 'res_type', 'sort_order', 'downloadable',
                  'thumbnail')


class StatisticsForm(forms.Form):
    start = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label=_('starting from'), required=False
    )
    end = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label=_('ending on'), required=False
    )


class AdminPromotionForm(forms.Form):
    PERM_OPTIONS = (
        ('add_admin', _('Add to Admin group')),
        ('del_admin', _('Remove from Admin group')),
        ('add_stats', _('Grant permission to view the Statistics page')),
        ('add_upload', _('Grant permission to upload to the Resources page')),
        ('del_stats', _('Revoke permission to view the Statistics page')),
        ('del_upload', _('Revoke permission to upload to the Resources page')),
    )

    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=forms.SelectMultiple)
    perms = forms.ChoiceField(choices=PERM_OPTIONS)


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        widgets = {
            'school_type': forms.RadioSelect(attrs={'required': True}),
            'name': forms.TextInput(
                attrs={'class': 'materialize-textarea, validate',
                       'required': True}),
            'address': forms.TextInput(
                attrs={'class': 'materialize-textarea, validate',
                       'required': True}),
            'city': forms.TextInput(
                attrs={'class': 'materialize-textarea, validate',
                       'required': True}),
            'province': forms.TextInput(
                attrs={'class': 'materialize-textarea, validate',
                       'required': True}),
            'zipcode': forms.TextInput(
                attrs={'class': 'materialize-textarea, validate',
                       'required': True})
        }
        fields = ('name', 'school_type',
                  'address', 'city',
                  'province', 'zipcode')


class RipAquaForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    time = forms.TimeField(input_formats=['%I:%M'])
    ampm = forms.ChoiceField(choices=TIME_PERIOD_CHOICES, label="AM/PM")

    class Meta:
        model = RipAquaticSurvey
        widgets = {
            'weather': forms.TextInput(attrs={'required': False}),
            'silt': forms.RadioSelect(attrs={'required': False}),
            'sand': forms.RadioSelect(attrs={'required': False}),
            'gravel': forms.RadioSelect(attrs={'required': False}),
            'cobble': forms.RadioSelect(attrs={'required': False}),
            'boulders': forms.RadioSelect(attrs={'required': False}),
            'bedrock': forms.RadioSelect(attrs={'required': False}),
            'small_debris': forms.RadioSelect(attrs={'required': False}),
            'medium_debris': forms.RadioSelect(attrs={'required': False}),
            'large_debris': forms.RadioSelect(attrs={'required': False}),
            'coniferous_trees': forms.RadioSelect(attrs={'required': False}),
            'deciduous_trees': forms.RadioSelect(attrs={'required': False}),
            'shrubs': forms.RadioSelect(attrs={'required': False}),
            'small_plants': forms.RadioSelect(attrs={'required': False}),
            'ferns': forms.RadioSelect(attrs={'required': False}),
            'grasses': forms.RadioSelect(attrs={'required': False}),
            'comments': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'species1': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'species2': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'species3': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'species4': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'species5': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'species6': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'significance1': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'significance2': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'significance3': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'significance4': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'significance5': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'significance6': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_type1': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_type2': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_type3': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_type4': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_type5': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_type6': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_comments1': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_comments2': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_comments3': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_comments4': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_comments5': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'wildlife_comments6': forms.Textarea(
                attrs={'class': 'materialize-textarea', 'required': False}),
            'notes': forms.Textarea(attrs={'class': 'materialize-textarea'}),

        }
        fields = (
            'date', 'weather', 'riffle_count', 'pool_count', 'silt',
            'sand', 'gravel', 'cobble', 'boulders', 'bedrock', 'small_debris',
            'medium_debris', 'large_debris', 'comments', 'coniferous_trees',
            'deciduous_trees', 'shrubs', 'small_plants', 'ferns', 'grasses',
            'species1', 'species2', 'species3', 'species4', 'species5',
            'species6', 'significance1', 'significance2', 'significance3',
            'significance4', 'significance5', 'significance6',
            'wildlife_type1', 'wildlife_type2', 'wildlife_type3',
            'wildlife_type4', 'wildlife_type5', 'wildlife_type6',
            'wildlife_comments1', 'wildlife_comments2', 'wildlife_comments3',
            'wildlife_comments4', 'wildlife_comments5', 'wildlife_comments6',
            'time', 'ampm', 'stream_length', 'notes'
            )
