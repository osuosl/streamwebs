from django.test import Client, TestCase, override_settings
from django.core.urlresolvers import reverse


@override_settings(SCHOOL_CHOICES=(
    ('a', 'School A'),
    ('b', 'School B'),
    ('c', 'School C'),))
class RegistrateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

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
        form, form errors should be displayed
        """
        response1 = self.client.post(reverse('streamwebs:register'), {})
        self.assertTemplateUsed(response1, 'streamwebs/register.html')
        self.assertFormError(
            response1,
            'user_form',
            'username',
            'This field is required.'
        )
        self.assertFormError(
            response1,
            'user_form',
            'password',
            'This field is required.'
        )

    def test_view_with_good_post_data(self):
        """
        When user submits a good form, the user should see a success message
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
