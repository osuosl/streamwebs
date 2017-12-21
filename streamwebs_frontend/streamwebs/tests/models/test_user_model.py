from __future__ import unicode_literals
from django.test import TestCase
import datetime
import calendar
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from streamwebs.models import (
    UserProfile,
    School
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
            school=self.school
        )
        self.assertEqual(profile.school.name, 'testSchool')

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
            school=self.school
        )
        self.assertEqual(profile1.user.username, 'user1')
        self.assertEqual(profile1.user.email, 'user@example.com')
        self.assertEqual(profile1.user.password, user1.password)

