''' TODO
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'john@example.com',
            'johnpassword'
        )

    def test_not_logged_in_view(self):
        """
        When the user hasn't logged in yet, they should see a "Log In" message
        """
        response = self.client.get(reverse('streamwebs:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        self.assertTemplateUsed(response, 'streamwebs/login.html')

    def test_good_username_good_password(self):
        """
        A valid username and password should log the user in.
        """
        response_good = self.client.post(
            reverse('streamwebs:login'),
            {'username': 'john', 'password': 'johnpassword'}
        )
        self.assertRedirects(
            response_good,
            reverse('streamwebs:index'),
            status_code=302,
            target_status_code=200
        )

    def test_good_username_bad_password(self):
        """
        A valid username but invalid password shouldn't log the user in.
        """
        response_bad_pass = self.client.post(
            reverse('streamwebs:login'),
            {'username': 'john', 'password': 'badpassword'}
        )
        self.assertRedirects(
            response_bad_pass,
            reverse('streamwebs:login') + '?next=',
            status_code=302,
            target_status_code=200
        )

    def test_bad_username_good_password(self):
        """
        An invalid username and valid password shouldn't log the user in.
        """
        response_bad_name = self.client.post(
            reverse('streamwebs:login'),
            {'username': 'notjohn', 'password': 'johnpassword'}
        )
        self.assertRedirects(
            response_bad_name,
            reverse('streamwebs:login') + '?next=',
            status_code=302,
            target_status_code=200
        )

    def test_bad_username_bad_password(self):
        """
        An invalid username and password shouldn't log the user in.
        """
        response_both_bad = self.client.post(
            reverse('streamwebs:login'),
            {'username': 'notjohn', 'password': 'badpassword'}
        )
        self.assertRedirects(
            response_both_bad,
            reverse('streamwebs:login') + '?next=',
            status_code=302,
            target_status_code=200
        )

    def test_logout_when_logged_in(self):
        """
        A logged in user should be able to log out.
        """
        response_in = self.client.post(
            reverse('streamwebs:login'),
            {'username': 'john', 'password': 'johnpassword'}
        )
        self.assertRedirects(
            response_in,
            reverse('streamwebs:index'),
            status_code=302,
            target_status_code=200
        )
        response_out = self.client.get(reverse('streamwebs:logout'))
        self.assertRedirects(
            response_out,
            reverse('streamwebs:index'),
            status_code=302,
            target_status_code=200
        )

    def test_logout_when_not_logged_in(self):
        """
        A logout attempt from someone who isn't logged in should fail.
        """
        response_out_attempt = self.client.get(reverse('streamwebs:logout'))
        self.assertEqual(response_out_attempt.status_code, 302)
        self.assertTemplateNotUsed(
            response_out_attempt, 'streamwebs/index.html')
'''
