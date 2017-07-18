from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class UserAccountTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('boss', 'boss@email.com',
                                             'BossBoss')
        self.client.login(username='boss', password='BossBoss')

    def test_account_view(self):
        """View should contain user info"""
        response = self.client.get(reverse(
            'streamwebs:account',
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/account.html')
        self.assertContains(response, 'Edit Account')
        self.assertContains(response, 'Email: boss@email.com')
        self.assertContains(response, 'Username: boss')
        self.assertContains(response, 'Change Email')
        self.assertContains(response, 'Change Password')


class UserChangeEmailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('boss', 'boss@email.com',
                                             'BossBoss')
        self.client.login(username='boss', password='BossBoss')

    def test_change_email_empty_post_data(self):
        new_email = ''
        response1 = self.client.post(reverse(
            'streamwebs:update_email'),
            {'email': new_email}
        )
        self.assertTemplateUsed(response1, 'streamwebs/update_email.html')
        self.assertFormError(response1, 'user_form', 'email',
                             'This field is required.')
        new_user_email = User.objects.get(username='boss').email
        self.assertEqual(new_user_email, 'boss@email.com')

    def test_change_email_bad_post_data(self):
        new_email = 'notAnEmail'
        response2 = self.client.post(reverse(
            'streamwebs:update_email'),
            {'email': new_email}
        )
        self.assertTemplateUsed(response2, 'streamwebs/update_email.html')
        self.assertFormError(response2, 'user_form', 'email',
                             'Enter a valid email address.')
        new_user_email = User.objects.get(username='boss').email
        self.assertEqual(new_user_email, 'boss@email.com')

    def test_change_email_good_post_data(self):
        new_email = 'boss2@gmail.com'
        response3 = self.client.post(reverse(
            'streamwebs:update_email'),
            {'email': new_email}
        )
        new_user_email = User.objects.get(username='boss').email
        self.assertEqual(new_user_email, 'boss2@gmail.com')
        self.assertRedirects(
            response3,
            reverse('streamwebs:account'),
            status_code=302,
            target_status_code=200
        )


class UserChangePasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('boss', 'boss@email.com',
                                             'BossBoss')
        self.client.login(username='boss', password='BossBoss')

    def test_change_password_empty_post_data(self):
        response1 = self.client.post(reverse(
            'streamwebs:update_password'),
            {
                'old_password': '',
                'password': '',
                'password_check': ''
            }
        )
        self.assertTemplateUsed(response1, 'streamwebs/update_password.html')
        self.assertFormError(response1, 'user_form', 'old_password',
                             'This field is required.')
        self.assertFormError(response1, 'user_form', 'password',
                             'This field is required.')
        self.assertFormError(response1, 'user_form', 'password_check',
                             'This field is required.')
        self.client.logout()
        self.client.login(username='boss', password='bossBoss')
        self.assertTrue(response1.context['user'].is_authenticated)

    def test_bad_old_password(self):
        response2 = self.client.post(reverse(
            'streamwebs:update_password'),
            {
                'old_password': 'wrong_password',
                'password': 'newPW',
                'password_check': 'newPW'
            }
        )
        self.assertTemplateUsed(response2, 'streamwebs/update_password.html')
        self.assertContains(response2, 'Your old password is incorrect.')
        self.client.logout()
        self.client.login(username='boss', password='BossBoss')
        self.assertTrue(response2.context['user'].is_authenticated)

    def test_new_passwords_not_match(self):
        response3 = self.client.post(reverse(
            'streamwebs:update_password'),
            {
                'old_password': 'BossBoss',
                'password': 'pw1',
                'password_check': 'pw2'
            }
        )
        self.assertTemplateUsed(response3, 'streamwebs/update_password.html')
        self.assertFormError(response3, 'user_form', 'password',
                             'New Passwords did not match.')
        self.client.logout()
        self.client.login(username='boss', password='BossBoss')
        self.assertTrue(response3.context['user'].is_authenticated)

    def test_old_new_same_passwords(self):
        response4 = self.client.post(reverse(
            'streamwebs:update_password'),
            {
                'old_password': 'BossBoss',
                'password': 'BossBoss',
                'password_check': 'BossBoss'
            }
        )
        self.assertTemplateUsed(response4, 'streamwebs/update_password.html')
        self.assertFormError(response4, 'user_form', 'password',
                             'Your old password and new password ' +
                             'cannot be the same.')
        self.client.logout()
        self.client.login(username='boss', password='BossBoss')
        self.assertTrue(response4.context['user'].is_authenticated)

    def test_good_passwords(self):
        response5 = self.client.post(reverse(
            'streamwebs:update_password'),
            {
                'old_password': 'BossBoss',
                'password': 'newPW',
                'password_check': 'newPW'
            }
        )
        self.assertRedirects(
            response5,
            reverse('streamwebs:account'),
            status_code=302,
            target_status_code=200
        )
        self.client.logout()
        self.client.login(username='boss', password='newPW')
        response6 = self.client.get(reverse(
            'streamwebs:update_password'),
        )
        self.assertTrue(response6.context['user'].is_authenticated)
