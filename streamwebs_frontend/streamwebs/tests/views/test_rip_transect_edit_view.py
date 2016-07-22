from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site


class AddTransectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_view_with_bad_blank_data(self):
        """
        When the user tries to submit a bad (blank) form, the form errors
        should be displayed
        """
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        response = self.client.post(
            reverse('streamwebs:riparian_transect_edit',
                    kwargs={'site_slug': site.id}), {})
        self.assertFormError(response, 'transect_form', 'school',
                             'This field is required.')
        self.assertFalse(response.context['added'])

    def test_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        response = self.client.post(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.id}
            ), {
                    'conifers': 1,
                    'hardwoods': 1,
                    'shrubs': 1,
                    'comments': 'comments',
                    'conifers': 1,
                    'hardwoods': 1,
                    'shrubs': 1,
                    'comments': 'comments',
                    'conifers': 1,
                    'hardwoods': 1,
                    'shrubs': 1,
                    'comments': 'comments',
                    'school': 'School of cool',
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes'
                }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/riparian_transect_edit.html'
        )
        self.assertTrue(response.context['added'])
        self.assertEqual(response.status_code, 200)

    def test_view_with_not_logged_in_user(self):
        """
        When the user is not logged in, they cannot view the data entry page
        """
        self.client.logout()
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        response = self.client.get(
            reverse('streamwebs:riparian_transect_edit',
                    kwargs={'site_slug': site.id})
        )
        self.assertContains(response, 'You must be logged in to submit data.')
        self.assertEqual(response.status_code, 200)