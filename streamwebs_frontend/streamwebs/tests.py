import datetime
from django.test import TestCase
from django.contrib.auth.models import User


#from streamwebs.models import UserProfile

# Create your tests here.

class UserTestCase(TestCase):

    def test_UserProfile_objs_exist(self):
        profile = UserProfile.objects.create('School',
                birthdate=datetime.date(1999, 4, 1))
        self.assertEqual(('profile' in locals()), True)
        
    def test_User_UserProfile_OneToOne(self):
        django_user = User.objects.create_user('djangoUser',
                'djangouser@gmail.com', 'imgeneric')
        django_user.first_name = 'Django'
        django_user.last_name = 'User'
        django_user.save()

        custom_user = UserProfile(school='Custom School',
                birthdate=datetime.date(1990, 5, 12))
        custom_user = django_user
        custom_user.save()

        self.assertEqual(custom_user.username, 'djangoUser')
        self.assertEqual(custom_user.email, 'djangouser@gmail.com')
        self.assertEqual(custom_user.password, 'imgeneric')
        self.assertEqual(custom_user.first_name, 'Django')
        self.assertEqual(custom_user.last_name, 'User')
        
        self.assertEqual(django_user.school, 'Custom School')
        self.assertEqual(django_user.birthdate, datetime.date(1990, 5, 12))

    def test_younger_than_13(self):
        now = datetime.datetime.now()
        bad_year_date = datetime.date(now.year - 12, now.month, now.day)
        self.assertEqual(is_valid_birthdate(bad_year_date), False)

        bad_month_date = datetime.date(now.year - 13, now.month + 1, now.day)
        self.assertEqual(is_valid_birthdate(bad_month_date), False)

        bad_day_date = datetime.date(now.year - 13, now.month, now.day+1)
        self.assertEqual(is_valid_birthdate(bad_day_date), False)

    def test_13_or_older(self):
        now = datetime.datetime.now()
        thirteen_today = datetime.date(now.year-13, now.month, now.day)
        self.assertEqual(is_valid_birthdate(thirteen_today), True)

        older_than_13 = datetime.date(now.year - 14, now.month, now.day)
        self.assertEqual(is_valid_birthdate(older_than_13), True)
