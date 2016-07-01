from django.test import TestCase
from streamwebs.forms import UserForm, UserProfileForm


class UserFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        )

    def test_UserForm_fields_exist(self):
        user_form = UserForm()
        self.assertEqual(set(user_form.Meta.fields), set(self.expected_fields))
        self.assertEqual(
            user_form.base_fields['password_check'].label,
            'Repeat your password'
        )
        self.assertEqual(
            str(type(user_form.base_fields['password_check'])),
            "<class 'django.forms.fields.CharField'>"
        )


class UserProfileFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('school', 'birthdate')

    def test_UserProfileForm_fields_exist(self):
        user_prof_form = UserProfileForm()
        self.assertEqual(
            set(user_prof_form.Meta.fields), set(self.expected_fields))
