from django.test import Client, TestCase
from django.core.urlresolvers import reverse
import os


class RegistrateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_view_with_unregistered_user(self):
        """
        When the user has not been registered, they should see a "Create your
        acct" message
        """
        response = self.client.get(reverse('streamwebs:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account.')

    def test_view_with_bad_post_data(self):
        """
        When the user attempts to submit a bad (i.e., empty/fields missing)
        form, form errors should be displayed and the user will not be
        registered
        """
        response1 = self.client.post(reverse('streamwebs:register'), {})

        self.assertTemplateUsed(response1, 'streamwebs/register.html')
        self.assertFormError(response1, 'user_form', 'username',
                             'This field is required.')
        self.assertFormError(response1, 'user_form', 'password',
                             'This field is required.')
        self.assertFormError(response1, 'user_form', 'email',
                             'This field is required.')
        self.assertFormError(response1, 'profile_form', 'birthdate',
                             'This field is required.')
        self.assertFormError(response1, 'profile_form', 'captcha',
                             'This field is required.')

        self.assertFalse(response1.context['registered'])

    def test_view_with_good_creds_bad_captcha(self):
        """
        When fields are filled but a bad captcha is submitted,
        the 'user' should be unable to register.
        """
        response = self.client.post(
            reverse('streamwebs:register'), {
                'username': 'john',
                'email': 'john@example.com',
                'password': 'johniscool',
                'first_name': 'John',
                'last_name': 'Johnson',
                'school': 'a',
                'birthdate': '1995-11-10',
                'g-recaptcha-response': 'NOPE'
            }
        )
        self.assertFalse(response.context['registered'])

    def test_view_with_good_post_data(self):
        """
        When user submits a good form, they should be able to register
        successfully
        """
        user_form_response = self.client.post(
            reverse('streamwebs:register'), {
                'username': 'john',
                'email': 'john@example.com',
                'password': 'johniscool',
                'first_name': 'John',
                'last_name': 'Johnson',
                'password_check': 'johniscool',
                'school': 'a',
                'birthdate': '1995-11-10'
            }
        )
        self.assertEqual(user_form_response.status_code, 200)
        self.assertTrue(user_form_response.context['registered'])

    def test_passwords_mismatch(self):
        bad_pw_response = self.client.post(
            reverse('streamwebs:register'), {
                'username': 'john',
                'email': 'john@example.com',
                'password': 'johniscool',
                'first_name': 'John',
                'last_name': 'Johnson',
                'password_check': 'johnisnotcool',
                'school': 'a',
                'birthdate': '1995-11-10'
            }
        )
        self.assertFormError(
            bad_pw_response,
            'user_form',
            'password',
            'Passwords do not match'
        )
        self.assertFalse(bad_pw_response.context['registered'])
        with self.settings(SCHOOL_CHOICES=(
            ('a', 'School A'),
            ('b', 'School B'),
            ('c', 'School C'),
        )):
            user_form_response = self.client.post(
                reverse('streamwebs:register'), {
                    'username': 'john',
                    'email': 'john@example.com',
                    'password': 'johniscool',
                    'first_name': 'John',
                    'last_name': 'Johnson',
                    'school': 'a',
                    'birthdate': '1995-11-10',
                    'g-recaptcha-response': 'PASSED'
                }
            )

            self.assertEqual(user_form_response.status_code, 200)
            self.assertTrue(user_form_response.context['registered'])

    def test_view_with_captcha_mode_false(self):
        """
        Bonus test to make sure that django-recaptcha's test mode works as
        advertised. When RECAPTCHA_TESTING is False, sending 'PASSED' for the
        captcha field should no longer successfully validate the form, and thus
        the user should not be able to register. This test passes (7/14/2016).
        """
        os.environ['RECAPTCHA_TESTING'] = 'False'
        response = self.client.post(
            reverse('streamwebs:register'), {
                'username': 'john',
                'email': 'john@example.com',
                'password': 'johniscool',
                'first_name': 'John',
                'last_name': 'Johnson',
                'school': 'a',
                'birthdate': '1995-11-10',
                'g-recaptcha-response': 'PASSED'
            }
        )
        self.assertFalse(response.context['registered'])

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']
