from __future__ import unicode_literals

import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class Site(models.Model):
    """
    The Sites model holds the information of a site, including the geographic
    location as a pair of latitudinal/longitudinal coordinates and an optional
    text description of entry.
    """

    site_name = models.CharField(max_length=250, blank=True)
    site_type = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    site_slug = models.SlugField(blank=True)

    # Geo Django fields to store a point
    location = models.PointField(null=True, blank=True)
    objects = models.GeoManager()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def validate_UserProfile_school(profile):
    if not profile.school in dict(profile.SCHOOL_CHOICES):
        raise ValidationError('That school is not in the list.')

def validate_UserProfile_birthdate(profile):
    today = datetime.datetime.now() 
    if profile.birthdate.year > today.year - 13:
        raise ValidationError('You must have been born before %s' % (today.year-13))
    elif profile.birthdate.year == today.year - 13:
        if profile.birthdate.month > today.month: 
            raise ValidationError('You are not yet 13 (month)')
        elif profile.birthdate.month == today.month:
            if profile.birthdate.day > today.day:
                raise ValidationError('You are not yet 13 (days)')
            
class UserProfile(models.Model):
    SCHOOL_A = 'a'
    SCHOOL_B = 'b'
    SCHOOL_C = 'c'
    SCHOOL_CHOICES = (
      (SCHOOL_A, 'School A'),
      (SCHOOL_B, 'School B'),
      (SCHOOL_C, 'School C'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length = 1, choices=SCHOOL_CHOICES, default='', validators=[validate_UserProfile_school])
    birthdate = models.DateField(validators=[validate_UserProfile_birthdate])

    def __unicode__(self):
        return self.user.username
