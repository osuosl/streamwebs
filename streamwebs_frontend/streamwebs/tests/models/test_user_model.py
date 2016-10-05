from __future__ import unicode_literals
from django.test import TestCase
import datetime
import calendar
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from streamwebs.models import (
    UserProfile,
    School,
    validate_UserProfile_birthdate
)


class UserTestCase(TestCase):

    def setUp(self):
        self.school = School()
        self.school.name = "testSchool"
        self.school.school_type = "basics"
        self.school.save()

    def test_UserProfile_objs_exist(self):
        """
        Tests that User and UserProfile objects are created correctly
        """
        user = User.objects.create_user(
            'user',
            'example@gmail.com',
            'password'
        )
        profile = UserProfile.objects.create(
            user=user,
            school=self.school,
            birthdate=datetime.date(1999, 4, 1)
        )
        self.assertEqual(profile.school.name, 'testSchool')
        self.assertEqual(profile.birthdate, datetime.date(1999, 4, 1))

    def test_User_UserProfile_OneToOne(self):
        """
        Tests that User and UserProfile have a one-to-one relationship
        """
        user1 = User.objects.create_user(
            'user1',
            'user@example.com',
            'password'
        )
        profile1 = UserProfile.objects.create(
            user=user1,
            school=self.school,
            birthdate=datetime.date(1999, 4, 1)
        )
        self.assertEqual(profile1.user.username, 'user1')
        self.assertEqual(profile1.user.email, 'user@example.com')
        self.assertEqual(profile1.user.password, user1.password)

    def test_bad_birth_year(self):
        """
        Creating a UserProfile with a birth year greater than the current year:
        minus 13 should raise a ValidationError
        """

        today = datetime.datetime.now()
        bad_yr_user = User.objects.create_user(
            'bad_yr',
            'user@example.com',
            'password'
        )
        bad_yr_prof = UserProfile.objects.create(
            user=bad_yr_user,
            school=self.school,
            birthdate=datetime.date(today.year - 12, 4, 2)
        )
        with self.assertRaises(ValidationError):
            validate_UserProfile_birthdate(bad_yr_prof.birthdate)

    def test_edge_year_bad_month(self):
        """
        If the birth year is from 13 years ago but the birth month is greater
        than the current month, a ValidationError should be raised
        """
        today = datetime.datetime.now()
        bad_month_user = User.objects.create_user(
            'bad_month',
            'user@example.com',
            'password'
        )
        bad_month_prof = UserProfile.objects.create(
            user=bad_month_user,
            school=self.school,
            birthdate=datetime.date(today.year - 13, today.month + 1, 2)
        )
        with self.assertRaises(ValidationError):
            validate_UserProfile_birthdate(bad_month_prof.birthdate)

    def test_edge_year_edge_month_bad_day(self):
        """
        If the birth year is from 13 years ago and the birth month is the
        current month, but the birth day is greater than the current day, a
        ValidationError should be raised
        """
        today = datetime.datetime.now()

        bad_day_user = User.objects.create_user(
            'bad_day',
            'user@example.com',
            'password'
        )

        # If today is the last day of the month,
        if today.day == calendar.monthrange(today.year, today.month)[1]:
            # and the next month is January,
            if today.month == 12:
                month = 1
            else:
                month = today.month + 1
            birthdate = datetime.date(today.year-13, month, 1)

        else:
            birthdate = datetime.date(today.year-13, today.month, today.day+1)

        bad_day_prof = UserProfile.objects.create(
            user=bad_day_user,
            school=self.school,
            birthdate=birthdate
        )
        with self.assertRaises(ValidationError):
            validate_UserProfile_birthdate(bad_day_prof.birthdate)

    def test_thirteen_today(self):
        """
        A UserProfile representing a user who turns 13 today should not raise
        an exception.
        """
        today = datetime.datetime.now()
        user13 = User.objects.create_user(
            'user13',
            'user@example.com',
            'password'
        )
        profile13 = UserProfile.objects.create(
            user=user13,
            school=self.school,
            birthdate=datetime.date(today.year-13, today.month, today.day)
        )
        try:
            validate_UserProfile_birthdate(profile13.birthdate)
        except:
            self.fail('An exception was raised.')
