from __future__ import unicode_literals

import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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


def validate_UserProfile_school(school):
    if school not in dict(settings.SCHOOL_CHOICES):
        raise ValidationError('That school is not in the list.')


def validate_UserProfile_birthdate(birthdate):
    today = datetime.datetime.now()
    if birthdate.year > today.year - 13:
        raise ValidationError(
            'You must have been born before %s' % (today.year-13)
        )
    elif birthdate.year == today.year - 13:
        if birthdate.month > today.month:
            raise ValidationError('You are not yet 13 (month)')
        elif birthdate.month == today.month:
            if birthdate.day > today.day:
                raise ValidationError('You are not yet 13 (days)')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(
        max_length=1,
        choices=settings.SCHOOL_CHOICES,
        default='',
        validators=[validate_UserProfile_school]
    )
    birthdate = models.DateField(validators=[validate_UserProfile_birthdate])

    def __unicode__(self):
        return self.user.username
