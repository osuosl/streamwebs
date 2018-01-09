from django.test import TestCase
from streamwebs.forms import UserProfileForm, UserFormEmailAsUsername


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
        user_form = UserFormEmailAsUsername()
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
        self.expected_fields = ('school',)

    def test_UserProfileForm_fields_exist(self):
        user_prof_form = UserProfileForm()
        self.assertEqual(set(user_prof_form.Meta.fields),
                         set(self.expected_fields))
        self.assertEqual(str(type(user_prof_form.base_fields['captcha'])),
                         "<class 'captcha.fields.ReCaptchaField'>")
