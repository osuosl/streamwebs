from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site


class UpdateSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.site = Site.test_objects.create_site('Creaky Creek', 'SS', 'slug')

    def test_prepopulate_siteform(self):
        """View should first contain form prepopulated w requested site info"""
        response = self.client.get(reverse('streamwebs:update_site',
                                           kwargs={'site_slug': self.site.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/update_site.html')
        self.assertContains(response, 'Creaky Creek')
        self.assertContains(response, 'SS')
        self.assertContains(response, self.site.id)

    def test_successful_site_update(self):
        """Tests that update is successful if all data valid"""
        response = self.client.post(reverse(
            'streamwebs:update_site', kwargs={'site_slug': self.site.id}), {
                'site_name': 'Shrieky Creek',
                'site_type': 'SS',
                'description': 'some description',
                'location': 'POINT(44.0612385 -121.3846841)'})

        self.assertTrue(response.context['updated'])
        self.assertNotEqual(self.site.modified, response.context['modified'])
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_site_update(self):
        """Tests that update is unsuccessful if some/all data invalid"""
        response = self.client.post(reverse(
            'streamwebs:update_site', kwargs={'site_slug': self.site.id}), {})
        self.assertFormError(response, 'site_form', 'site_name',
                             'This field is required.')
        self.assertFalse(response.context['updated'])

    def test_passive_update(self):
        """Tests that submitting prepopulated form as-is changes nothing"""
        response = self.client.post(reverse(
            'streamwebs:update_site', kwargs={'site_slug': self.site.id}), {
                'site_name': 'Creaky Creek',
                'site_type': 'SS',
                'location': 'POINT(44.0612385 -121.3846841)'})

        self.assertTrue(response.context['updated'])
        self.assertEqual(self.site.modified, response.context['modified'])
        self.assertEqual(response.status_code, 200)

    def test_view_with_not_logged_in_user(self):
        """Tests that the user can't update site if they're not logged in"""
        self.client.logout()
        response = self.client.get(reverse('streamwebs:update_site',
                                   kwargs={'site_slug': self.site.id}))

        self.assertContains(response, 'You must be logged in to edit a site.')
        self.assertEqual(response.status_code, 200)
