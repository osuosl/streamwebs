from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group, Permission


class AdminPromoTestCase(TestCase):
    fixtures = ['sample_users.json']

    def setUp(self):
        self.client = Client()
        admins = Group.objects.get(name='admin')
        can_promo = Permission.objects.get(codename='can_promote_users')

        # super admin (level: Renee) with promotion permission
        self.superAdmin = User.objects.create_user('superAdmin',
                                                   'super@example.com',
                                                   'superpassword')
        self.superAdmin.groups.add(admins)
        self.superAdmin.user_permissions.add(can_promo)

        # regular admin (level: Renee's colleague) without promotion permission
        self.regAdmin = User.objects.create_user('regAdmin', 'reg@example.com',
                                                 'regpassword')
        self.regAdmin.groups.add(admins)

    def test_data_loaded_and_usable(self):
        """Check users exist in test db and that admins have correct perms"""
        self.assertEquals(User.objects.count(), 9)
        self.assertTrue(self.superAdmin.has_perms(
            ['streamwebs.can_view_stats', 'streamwebs.can_upload_resources',
             'streamwebs.can_promote_users']))
        self.assertTrue(self.regAdmin.has_perms(
            ['streamwebs.can_view_stats', 'streamwebs.can_upload_resources']))
        self.assertFalse(self.regAdmin.has_perm(
            'streamwebs.can_promote_users'))
        self.assertTrue(self.regAdmin.groups.filter(name='admin').exists())
        self.assertTrue(self.superAdmin.groups.filter(name='admin').exists())

    def test_not_logged_in_user(self):
        """If user not logged in, can't view page, period."""
        response = self.client.get(reverse('streamwebs:user_promo'))

        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:user_promo')),
            status_code=302,
            target_status_code=200)
        self.assertTemplateNotUsed(
            response, 'streamwebs/admin/user_promo.html')

    def test_superAdmin_can_view(self):
        """Admin with promo perm should be able to view the page"""
        self.client.login(username='superAdmin', password='superpassword')
        response = self.client.get(reverse('streamwebs:user_promo'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/admin/user_promo.html')

        self.client.logout()

    def test_regAdmin_cannot_view(self):
        """Admin w/o promo perm should be denied access to the page"""
        self.client.login(username='regAdmin', password='regpassword')
        response = self.client.get(reverse('streamwebs:user_promo'))

        self.assertRaises(PermissionDenied)
        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(response,
                                   'streamwebs/admin/user_promo.html')
        self.client.logout()
