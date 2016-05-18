from __future__ import unicode_literals

import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

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


class UserProfile(models.Model):
    SCHOOL_A = 'a'
    SCHOOL_B = 'b'
    SCHOOL_C = 'c'
    SCHOOL_CHOICES = (
      (SCHOOL_A, 'School A'),
      (SCHOOL_B, 'School B'),
      (SCHOOL_C, 'School C'),
    )

    user = models.OneToOneField(User, related_name='profile')
    #school = models.CharField(max_length=140, blank=True)
    school = models.CharField(max_length = 1, choices=SCHOOL_CHOICES)
    birthdate = models.DateField('birthdate')

#    def is_valid_birthdate(self):
#        if self.birthdate.year > 2003:
#            return False

    def __unicode__(self):
        return self.user.username
