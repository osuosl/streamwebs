from __future__ import unicode_literals
from django.test import TestCase
import datetime
from django.contrib.auth.models import User
# from django.contrib.gis.db import models
# from django.apps import apps
# from itertools import chain
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _

from streamwebs.models import(
    UserProfile,
    validate_UserProfile_school,
    validate_UserProfile_birthdate
)


class UserTestCase(TestCase):

    def test_UserProfile_objs_exist(self):
        user = User.objects.create_user(
            'user',
            'example@gmail.com',
            'password'
        )
        profile = UserProfile.objects.create(
            user=user,
            school='a',
            birthdate=datetime.date(1999, 4, 1)
        )
        self.assertEqual(profile.school, 'a')
        self.assertEqual(profile.birthdate, datetime.date(1999, 4, 1))

    def test_User_UserProfile_OneToOne(self):
        user1 = User.objects.create_user(
            'user1',
            'user@example.com',
            'password'
        )
        profile1 = UserProfile.objects.create(
            user=user1,
            school='c',
            birthdate=datetime.date(1999, 4, 1)
        )
        self.assertEqual(profile1.user.username, 'user1')
        self.assertEqual(profile1.user.email, 'user@example.com')
        self.assertEqual(profile1.user.password, user1.password)

    def test_school_not_in_list(self):
        with self.settings(SCHOOL_CHOICES=(
            ('e', 'School E'),
            ('f', 'School F'),
            ('g', 'School G'),
        )):
            bad_sch_user = User.objects.create_user(
                'bad_sch',
                'user@example.com',
                'password'
            )
            bad_sch_prof = UserProfile.objects.create(
                user=bad_sch_user,
                school='d',
                birthdate=datetime.date(1999, 4, 2)
            )
            with self.assertRaises(ValidationError):
                validate_UserProfile_school(bad_sch_prof.school)

    def test_school_is_in_list(self):
        with self.settings(SCHOOL_CHOICES=(
            ('e', 'School E'),
            ('f', 'School F'),
            ('g', 'School G'),
        )):

            good_sch_user = User.objects.create_user(
                'good_sch',
                'user@example.com',
                'password'
            )
            good_sch_prof = UserProfile.objects.create(
                user=good_sch_user,
                school='e',
                birthdate=datetime.date(1999, 4, 2)
            )
            try:
                validate_UserProfile_school(good_sch_prof.school)
            except:
                self.fail('An exception was raised.')

    def test_bad_birth_year(self):
        today = datetime.datetime.now()
        bad_yr_user = User.objects.create_user(
            'bad_yr',
            'user@example.com',
            'password'
        )
        bad_yr_prof = UserProfile.objects.create(
            user=bad_yr_user,
            school='b',
            birthdate=datetime.date(today.year - 12, 4, 2)
        )
        with self.assertRaises(ValidationError):
            validate_UserProfile_birthdate(bad_yr_prof.birthdate)

    def test_edge_year_bad_month(self):
        today = datetime.datetime.now()
        bad_month_user = User.objects.create_user(
            'bad_month',
            'user@example.com',
            'password'
        )
        bad_month_prof = UserProfile.objects.create(
            user=bad_month_user,
            school='b',
            birthdate=datetime.date(today.year - 13, today.month + 1, 2)
        )
        with self.assertRaises(ValidationError):
            validate_UserProfile_birthdate(bad_month_prof.birthdate)

    def test_edge_year_edge_month_bad_day(self):
        today = datetime.datetime.now()
        bad_day_user = User.objects.create_user(
            'bad_day',
            'user@example.com',
            'password'
        )
        bad_day_prof = UserProfile.objects.create(
            user=bad_day_user,
            school='b',
            birthdate=datetime.date(today.year-13, today.month, today.day+1)
        )
        with self.assertRaises(ValidationError):
            validate_UserProfile_birthdate(bad_day_prof.birthdate)

    def test_thirteen_today(self):
        today = datetime.datetime.now()
        user13 = User.objects.create_user(
            'user13',
            'user@example.com',
            'password'
        )
        profile13 = UserProfile.objects.create(
            user=user13,
            school='a',
            birthdate=datetime.date(today.year-13, today.month, today.day)
        )
        try:
            validate_UserProfile_birthdate(profile13.birthdate)
        except:
            self.fail('An exception was raised.')
