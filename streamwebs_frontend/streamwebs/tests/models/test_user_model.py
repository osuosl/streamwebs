from django.test import TestCase

import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import UserProfile

# Create your tests here.

class UserTestCase(TestCase):

    def setUp(self):
#        self.user = User.objects.create_user(username='testuser',
#                        email='testuser@example.com', password='2cool4U',
#                        school='School A', birthdate=datetime.date(1999, 4, 1))
        self.profile_fields = {
            #'username': models.CharField,
            #'password': models.CharField,
            #'email': models.EmailField,
            'school': models.CharField,
            'birthdate': models.DateField,
            'id': models.AutoField
        }

    def test_UserProfile_objs_exist(self):
        #profile = UserProfile.objects.create(school='School', birthdate=datetime.date(1999, 4, 1))
        #print profile.id, profile.school, profile.birthdate, profile.user_id
        #self.assertEqual(('profile' in locals()), True)
        profile = apps.get_model('streamwebs', 'userprofile')
        for field, field_type in self.profile_fields.items():
            self.assertEqual(field_type, type(profile._meta.get_field(field)))

#    def test_User_UserProfile_OneToOne(self):
#        django_user = User.objects.create_user('djangoUser','djangouser@gmail.com', 'imgeneric')
#        django_user.first_name = 'Django'
#        django_user.last_name = 'User'
#        django_user.save()
#
#        custom_user = UserProfile(school='Custom School', birthdate=datetime.date(1990, 5, 12))
#        custom_user = django_user
#        custom_user.save()
#
#        self.assertEqual(custom_user.username, 'djangoUser')
#        self.assertEqual(custom_user.email, 'djangouser@gmail.com')
#         
#        self.assertEqual(custom_user.first_name, 'Django')
#        self.assertEqual(custom_user.last_name, 'User')
#        
#        self.assertEqual(django_user.school, 'Custom School')
#        self.assertEqual(django_user.birthdate, datetime.date(1990, 5, 12))
#
#    def test_younger_than_13(self):
#        now = datetime.datetime.now()
#        bad_year_date = datetime.date(now.year-12, now.month, now.day)
#        user = UserProfile.objects.create(school='school', birthdate=bad_year_date)
#        self.assertEqual(user.is_valid_birthdate(), False)
#
#        bad_month_date = datetime.date(now.year-13, now.month + 1, now.day)
#        user2 = UserProfile.objects.create(school='school', birthdate=bad_month_date)
#
#        self.assertEqual(user2.is_valid_birthdate(), False)
#
#        bad_day_date = datetime.date(now.year-13, now.month, now.day+1)
#        user3 = UserProfile.objects.create(school='school', birthdate=bad_day_date)
#
#        self.assertEqual(user3.is_valid_birthdate(), False)
#
#    def test_13_or_older(self):
#        now = datetime.datetime.now()
#        thirteen_today = datetime.date(now.year-13, now.month, now.day)
#        user = UserProfile.objects.create(school='school', birthdate=thirteen_today)
#        user.save()
#        self.assertEqual(user.is_valid_birthdate(), True)
#
#        older_than_13 = datetime.date(now.year-14, now.month, now.day)
#        user2 = UserProfile.objects.create(school='school', birthdate=older_than_13)
#
#        self.assertEqual(user2.is_valid_birthdate(), True)

