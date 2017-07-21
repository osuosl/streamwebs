from django.test import TestCase
from streamwebs.forms import UserEmailForm, UserPasswordForm


class UserEmailFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'email',
        )
        self.required_fields = (
            'email',
        )

    def test_form_fields_exist(self):
        user_email_form = UserEmailForm()
        self.assertEqual(set(user_email_form.Meta.fields),
                         set(self.expected_fields))
        self.assertEqual(str(type(user_email_form.base_fields['email'])),
                         "<class 'django.forms.fields.CharField'>")

    def test_required_fields(self):
        user_email_form = UserEmailForm()
        for field in self.required_fields:
            self.assertEqual(user_email_form.base_fields[field].required, True)


class UserPasswordFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'old_password',
            'password',
            'password_check'
        )
        self.required_fields = (
            'old_password',
            'password',
            'password_check'
        )

        def test_form_fields_exist(self):
            user_password_form = UserPasswordForm()
            self.assertEqual(set(user_password_form.Meta.fields),
                             set(self.expected_fields))
            self.assertEqual(
                str(type(user_password_form.base_fields['old_password'])),
                "<class 'django.forms.fields.CharField'>"
            )
            self.assertEqual(
                str(type(user_password_form.base_fields['password'])),
                "<class 'django.forms.fields.CharField'>"
            )
            self.assertEqual(
                str(type(user_password_form.base_fields['password_check'])),
                "<class 'django.forms.fields.CharField'>"
            )

        def test_required_fields(self):
            user_pw_form = UserPasswordForm()
            for field in self.required_fields:
                self.assertEqual(user_pw_form.base_fields[field].required,
                                 True)
