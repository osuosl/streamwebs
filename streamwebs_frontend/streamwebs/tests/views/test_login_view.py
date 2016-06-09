from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from streamwebs.models import UserProfile

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user(
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
        response_good = self.client.post(reverse('streamwebs:login'), {'username': 'john', 'password': 'johnpassword'})
        self.assertRedirects(response_good, reverse('streamwebs:index'), status_code=302, target_status_code=200)

    def test_good_username_bad_password(self):
        response_bad_pass = self.client.post(reverse('streamwebs:login'), {'username': 'john', 'password': 'badpassword'})
        self.assertContains(response_bad_pass, 'Invalid credentials')

    def test_bad_username_good_password(self):
        response_bad_name = self.client.post(reverse('streamwebs:login'), {'username': 'notjohn', 'password': 'johnpassword'})
        self.assertContains(response_bad_name, 'Invalid credentials')

    def test_bad_username_bad_password(self):
        response_both_bad = self.client.post(reverse('streamwebs:login'), {'username': 'notjohn', 'password': 'badpassword'})
        self.assertContains(response_both_bad, 'Invalid credentials')
