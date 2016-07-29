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
                    kwargs={'site_slug': site.id}
                    ), {
                'transect-TOTAL_FORMS': '5',
                'transect-INITIAL_FORMS': '0',
                'transect-MAX_NUM_FORMS': '5'
                }
        )
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
                    'school': 'School of cool',
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes',

                    'transect-TOTAL_FORMS': '5',
                    'transect-INITIAL_FORMS': '0',
                    'transect-MAX_NUM_FORMS': '5',

                    'transect-0-conifers': 1,
                    'transect-0-hardwoods': 2,
                    'transect-0-shrubs': 3,
                    'transect-0-comments': '1 comments',

                    'transect-1-conifers': 4,
                    'transect-1-hardwoods': 5,
                    'transect-1-shrubs': 6,
                    'transect-1-comments': '2 comments',

                    'transect-2-conifers': 7,
                    'transect-2-hardwoods': 8,
                    'transect-2-shrubs': 9,
                    'transect-2-comments': '3 comments',

                    'transect-3-conifers': 8,
                    'transect-3-hardwoods': 7,
                    'transect-3-shrubs': 6,
                    'transect-3-comments': '4 comments',

                    'transect-4-conifers': 5,
                    'transect-4-hardwoods': 4,
                    'transect-4-shrubs': 3,
                    'transect-4-comments': '5 comments'

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
