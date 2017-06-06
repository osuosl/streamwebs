from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site


class UpdateSiteTestCase(TestCase):
    def setUp(self):
        self.site = Site.test_objects.create_site('Creaky Creek')

        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_prepopulate_siteform(self):
        """View should first contain form prepopulated w requested site info"""
        response = self.client.get(reverse(
            'streamwebs:update_site',
            kwargs={'site_slug': self.site.site_slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/update_site.html')
        self.assertContains(response, 'Creaky Creek')
        self.assertContains(response, self.site.site_slug)

    def test_successful_site_update(self):
        """Tests that update is successful if all data valid"""
        site = Site.test_objects.create_site('Creaky Creek')
        modified = site.modified

        response = self.client.post(reverse(
            'streamwebs:update_site',
            kwargs={'site_slug': site.site_slug}), {
                'site_name': 'Shrieky Creek',
                'description': 'some description',
                'location': 'POINT(-121.3846841 44.0612385)'})

        self.assertRedirects(
            response,
            reverse('streamwebs:site',
                    kwargs={'site_slug': Site.test_objects.last().site_slug}),
            status_code=302,
            target_status_code=200)
        self.assertNotEqual(modified, Site.test_objects.last().modified)

    def test_unsuccessful_site_update(self):
        """Tests that update is unsuccessful if some/all data invalid"""
        response = self.client.post(reverse(
            'streamwebs:update_site',
            kwargs={'site_slug': self.site.site_slug}), {})
        self.assertFormError(response, 'site_form', 'site_name',
                             'This field is required.')

    def test_passive_update(self):
        """Tests that submitting prepopulated form as-is changes nothing"""
        site = Site.test_objects.create_site('reaky Creek')
        modified = site.modified

        response = self.client.post(reverse(
            'streamwebs:update_site',
            kwargs={'site_slug': site.site_slug}), {
                'site_name': 'reaky Creek',
                'location': 'POINT(-121.3846841 44.0612385)'})

        self.assertRedirects(
            response,
            reverse('streamwebs:site',
                    kwargs={'site_slug': Site.test_objects.last().site_slug}),
            status_code=302,
            target_status_code=200)
        self.assertEqual(site.modified, modified)

    def test_view_with_not_logged_in_user(self):
        """Tests that user is redirected to login if they're not logged in"""
        self.client.logout()
        response = self.client.get(reverse('streamwebs:update_site',
                                   kwargs={'site_slug': self.site.site_slug}))
        self.assertRedirects(
            response, reverse('streamwebs:login') + '?next=' + reverse(
                'streamwebs:update_site',
                kwargs={'site_slug': self.site.site_slug}), status_code=302,
            target_status_code=200)
