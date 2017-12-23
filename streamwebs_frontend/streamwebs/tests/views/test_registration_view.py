from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import School
import os


class RegistrateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.school = School()
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_view_with_unregistered_user(self):
        """
        When the user has not been registered, they should see a register form
        """
        response = self.client.get(reverse('streamwebs:register'))
        self.assertEqual(response.status_code, 200)

    def test_view_with_bad_post_data(self):
        """
        When the user attempts to submit a bad (i.e., empty/fields missing)
        form, form errors should be displayed and the user will not be
        registered
        """
        response1 = self.client.post(reverse('streamwebs:register'), {})

        self.assertTemplateUsed(response1, 'streamwebs/register.html')
        self.assertFormError(response1, 'user_form', 'password',
                             'This field is required.')
        self.assertFormError(response1, 'user_form', 'password_check',
                             'This field is required.')
        self.assertFormError(response1, 'user_form', 'email',
                             'This field is required.')
        self.assertFormError(response1, 'profile_form', 'captcha',
                             'This field is required.')

    def test_view_with_good_post_data(self):
        """
        When user submits a good form, they should be able to register
        successfully
        """
        school = School()
        school.name = "Testyschool"
        school.school_type = "pro school"
        school.save()
        user_form_response = self.client.post(
            reverse('streamwebs:register'), {
                'email': 'john@example.com',
                'password': 'johniscool',
                'first_name': 'John',
                'last_name': 'Johnson',
                'password_check': 'johniscool',
                'school': school.id,
                'g-recaptcha-response': 'PASSED'
            }
        )
        # Redirect to register/confirm
        self.assertEqual(user_form_response.status_code, 302)

    def test_passwords_mismatch(self):
        bad_pw_response = self.client.post(
            reverse('streamwebs:register'), {
                'email': 'john@example.com',
                'password': 'johniscool',
                'first_name': 'John',
                'last_name': 'Johnson',
                'password_check': 'johnisnotcool',
                'school': 'a',
                'g-recaptcha-response': 'PASSED'
            }
        )
        self.assertFormError(
            bad_pw_response,
            'user_form',
            'password',
            'Passwords did not match'
        )

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']
