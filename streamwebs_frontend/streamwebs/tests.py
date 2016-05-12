from django.test import TestCase
from django.contrib.auth.models import User

from streamwebs.models import UserProfile

# Create your tests here.

class UserTestCase(TestCase):

    def test_User_UserProfile_OneToOne(self):
        django_user = User.objects.create_user('djangoUser',
                'djangouser@gmail.com', 'imgeneric')
        django_user.first_name = 'Django'
        django_user.last_name = 'User'
        django_user.save()

        custom_user = UserProfile(school='Custom School', birthdate=date(1990,
            5, 12))
        custom_user = django_user
        custom_user.save()

        self.assertEqual(custom_user.username, 'djangoUser')
        self.assertEqual(custom_user.email, 'djangouser@gmail.com')
        self.assertEqual(custom_user.password, 'imgeneric')
        self.assertEqual(custom_user.first_name, 'Django')
        self.assertEqual(custom_user.last_name, 'User')
        
        self.assertEqual(django_user.school, 'Custom School')
        self.assertEqual(django_user.birthdate, date(1990, 5, 12))

