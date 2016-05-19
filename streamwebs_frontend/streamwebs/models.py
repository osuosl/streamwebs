from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    school = models.CharField(max_length=140, blank=True)
#    birthdate = models.DateField('birthdate')

#    def is_valid_birthdate(self):
#        if self.birthdate.year > 2003:
#            return False

    def __unicode__(self):
        return self.user.username

