from django.test import Client, TestCase
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse


# Create your tests here.
class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.reg_user = User.objects.create_user(
            'reg',
            'reg@example.com',
            'regpassword'
        )
        self.admin = User.objects.create_user(
            'admin',
            'admin@example.com',
            'adminpassword'
        )
        self.superAdmin = User.objects.create_superuser(
            'superadmin',
            'super@example.com',
            'superpassword'
        )
        admins = Group.objects.get(name='org_admin')
        self.admin.groups.add(admins)

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/index.html')

    def test_regular_navigation_menu(self):
        """When regular user logged in, can see standard tabs but not Admin."""
        self.client.login(username='reg', password="regpassword")
        response = self.client.get(reverse('streamwebs:index'))
        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Sites')
        self.assertContains(response, 'Resources')
        self.assertContains(response, 'Logout')
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Create Account')
        self.assertNotContains(response, 'Manage Users')
        self.assertNotContains(response, 'View Site Statistics')

        # can't see stats, can't see users
        self.client.logout()

    def test_admin_navigation_menu(self):
        """When admin user logged in, can see standard tabs and Admin tab."""
        self.client.login(username='admin', password="adminpassword")
        response = self.client.get(reverse('streamwebs:index'))
        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Sites')
        self.assertContains(response, 'Resources')
        self.assertContains(response, 'Logout')
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Create Account')
        # can see stats, can't see users
        self.assertNotContains(response, 'Manage Users')
        self.assertNotContains(response, 'View Site Statistics')

        self.client.logout()

    def test_anon_navigation_menu(self):
        """When user not logged in, has Create Acct tab but no Admin tab."""
        response = self.client.get(reverse('streamwebs:index'))
        self.assertContains(response, 'Sites')
        self.assertContains(response, 'Resources')
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Logout')
        self.assertContains(response, 'Create Account')
        # can't see stats, can't see users
        self.assertNotContains(response, 'Manage Users')
        self.assertNotContains(response, 'View Site Statistics')
        self.client.logout()

    def test_can_manage_users(self):
        """When user logged in with user promo perm, can see that tab"""
        self.client.login(username='superadmin', password='superpassword')
        response = self.client.get(reverse('streamwebs:index'))
        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Sites')
        self.assertContains(response, 'Resources')
        self.assertContains(response, 'Logout')
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Create Account')
        self.assertContains(response, 'View Site Statistics')
        self.assertContains(response, 'Manage Users')
        self.client.logout()
