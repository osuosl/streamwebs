from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from streamwebs.models import Site, Macroinvertebrates


class DeactivateSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.site = Site.test_objects.create_site('Creaky Creek', 'slug')

    def test_successful_deactivate(self):
        """Tests that user can deactivate site if site has no data."""
        response = self.client.get(reverse('streamwebs:deactivate_site',
                                           kwargs={'site_slug': self.site.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.site.site_name)
        self.assertContains(response, ' has been successfully deleted.')
        self.assertNotEqual(self.site.modified,
                            response.context['modified_time'])
        self.assertTrue(response.context['deactivated'])

        # after deactivation, the user cannot view the site at its URL.
        with self.assertRaises(ObjectDoesNotExist):
            response = self.client.get(reverse(
                'streamwebs:site', kwargs={'site_slug': self.site.id}))

    def test_unsuccessful_deactivate(self):
        """Tests that user can't deactivate site if the site has data."""
        data = Macroinvertebrates.objects.create_macro(self.site)  # NOQA
        response = self.client.get(reverse('streamwebs:deactivate_site',
                                           kwargs={'site_slug': self.site.id}))

        self.assertContains(
            response,
            'This site has data and can only be deleted by an administrator.')
        self.assertEqual(self.site.modified, response.context['modified_time'])
        self.assertFalse(response.context['deactivated'])

    def test_view_with_not_logged_in_user(self):
        """Tests that user can't deactivate site if they're not logged in"""
        self.client.logout()
        response = self.client.get(reverse('streamwebs:deactivate_site',
                                           kwargs={'site_slug': self.site.id}))

        self.assertContains(response,
                            'You must be logged in to delete a site.')
        self.assertEqual(response.status_code, 200)
