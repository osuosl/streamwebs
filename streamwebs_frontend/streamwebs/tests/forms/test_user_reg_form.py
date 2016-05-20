from django.test import TestCase

from streamwebs.forms import UserForm, UserProfileForm


class UserFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def test_UserForm_fields_exist(self): 
        user_form = UserForm()
        for i in range(len(self.expected_fields)):
            self.assertEqual(user_form.Meta.fields[i], self.expected_fields[i])

class UserProfileFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('school', 'birthdate')

    def test_UserProfileForm_fields_exist(self):
        user_prof_form = UserProfileForm()
        for i in range(len(self.expected_fields)):
            self.assertEqual(user_prof_form.Meta.fields[i], self.expected_fields[i])
