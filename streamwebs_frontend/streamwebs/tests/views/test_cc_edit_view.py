from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site


class AddCanopyCoverTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joe', 'joe@example.com',
                                             'notsoaveragejoe')
        self.client.login(username='joe', password='notsoaveragejoe')

    def test_view_with_bad_blank_data(self):
        """
        Display form errors when the user submits a (completely) blank form
        """
        site = Site.test_objects.create_site('Test', 'Type')
        response = self.client.post(
            reverse('streamwebs:canopy_cover_edit',
                    kwargs={'site_slug': site.site_slug}
            ), {
                'canopy_cover-TOTAL_FORMS': '4',
                'canopy_cover-INITIAL_FORMS': '0',
                'canopy_cover-MAX_NUM_FORMS': '4'
               }
        )
        # At least one field should raise an error
        self.assertFormError(
            response, 'canopy_cover_form', 'school', 'This field is required.'
        )
        self.assertFalse(response.context['added'])

    def test_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, return a success message
        """
        site = Site.test_objects.create_site('Test', 'Type')
        response = self.client.post(
            reverse(
                'streamwebs:canopy_cover_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                'school': 'School of Cool',
                'date_time': '2016-08-31 12:30:00',
                'site': site.id,
                'weather': 'Gray',

                'canopy_cover-TOTAL-FORMS': '4',
                'canopy_cover-INITIAL-FORMS': '0',
                'canopy_cover-MAX_NUM_FORMS': '4',

                #'canopy_cover-0-direction': 'North',
                #'canopy_cover-0-A': True,
                #'canopy_cover-0-B': True,
                #'canopy_cover-0-C': False,
                #'canopy_cover-0-D': True,
                #'canopy_cover-0-E': False,
                #'canopy_cover-0-F': False,
                #'canopy_cover-0-G': False,
                #'canopy_cover-0-H': True,
                #'canopy_cover-0-I': False,
                #'canopy_cover-0-J': False,
                #'canopy_cover-0-K': True,
                #'canopy_cover-0-L': True,
                #'canopy_cover-0-M': True,
                #'canopy_cover-0-N': True,
                #'canopy_cover-0-O': True,
                #'canopy_cover-0-P': False,
                #'canopy_cover-0-Q': False,
                #'canopy_cover-0-R': True,
                #'canopy_cover-0-S': True,
                #'canopy_cover-0-T': False,
                #'canopy_cover-0-U': False,
                #'canopy_cover-0-V': True,
                #'canopy_cover-0-W': True,
                #'canopy_cover-0-X': False,
                #'canopy_cover-0-num_shaded': 13,

                #'canopy_cover-1-direction': 'East',
                #'canopy_cover-1-A': False,
                #'canopy_cover-1-B': False,
                #'canopy_cover-1-C': False,
                #'canopy_cover-1-D': True,
                #'canopy_cover-1-E': True,
                #'canopy_cover-1-F': False,
                #'canopy_cover-1-G': False,
                #'canopy_cover-1-H': True,
                #'canopy_cover-1-I': False,
                #'canopy_cover-1-J': False,
                #'canopy_cover-1-K': True,
                #'canopy_cover-1-L': True,
                #'canopy_cover-1-M': True,
                #'canopy_cover-1-N': False,
                #'canopy_cover-1-O': True,
                #'canopy_cover-1-P': True,
                #'canopy_cover-1-Q': False,
                #'canopy_cover-1-R': True,
                #'canopy_cover-1-S': True,
                #'canopy_cover-1-T': False,
                #'canopy_cover-1-U': False,
                #'canopy_cover-1-V': True,
                #'canopy_cover-1-W': True,
                #'canopy_cover-1-X': False,
                #'canopy_cover-1-num_shaded': 12,

                #'canopy_cover-2-direction': 'South',
                #'canopy_cover-2-A': True,
                #'canopy_cover-2-B': True,
                #'canopy_cover-2-C': False,
                #'canopy_cover-2-D': True,
                #'canopy_cover-2-E': False,
                #'canopy_cover-2-F': False,
                #'canopy_cover-2-G': False,
                #'canopy_cover-2-H': True,
                #'canopy_cover-2-I': False,
                #'canopy_cover-2-J': False,
                #'canopy_cover-2-K': True,
                #'canopy_cover-2-L': False,
                #'canopy_cover-2-M': True,
                #'canopy_cover-2-N': True,
                #'canopy_cover-2-O': True,
                #'canopy_cover-2-P': False,
                #'canopy_cover-2-Q': False,
                #'canopy_cover-2-R': True,
                #'canopy_cover-2-S': True,
                #'canopy_cover-2-T': False,
                #'canopy_cover-2-U': False,
                #'canopy_cover-2-V': False,
                #'canopy_cover-2-W': False,
                #'canopy_cover-2-X': False,
                #'canopy_cover-2-num_shaded': 10,

                #'canopy_cover-3-direction': 'West',
                #'canopy_cover-3-A': True,
                #'canopy_cover-3-B': False,
                #'canopy_cover-3-C': False,
                #'canopy_cover-3-D': True,
                #'canopy_cover-3-E': True,
                #'canopy_cover-3-F': True,
                #'canopy_cover-3-G': False,
                #'canopy_cover-3-H': True,
                #'canopy_cover-3-I': False,
                #'canopy_cover-3-J': False,
                #'canopy_cover-3-K': True,
                #'canopy_cover-3-L': True,
                #'canopy_cover-3-M': False,
                #'canopy_cover-3-N': True,
                #'canopy_cover-3-O': True,
                #'canopy_cover-3-P': False,
                #'canopy_cover-3-Q': False,
                #'canopy_cover-3-R': True,
                #'canopy_cover-3-S': True,
                #'canopy_cover-3-T': False,
                #'canopy_cover-3-U': False,
                #'canopy_cover-3-V': True,
                #'canopy_cover-3-W': True,
                #'canopy_cover-3-X': True,
                #'canopy_cover-3-num_shaded': 14
               }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/canopy_cover_edit.html'
        )
        self.assertTrue(response.context['added'])
        self.assertEqual(response.status_code, 200)

    def test_view_with_not_logged_in_user(self):
        """
        When the user isn't logged in, don't display the the data entry page
        """
        self.client.logout()
        site = Site.test_objects.create_site('Test', 'Type')
        response = self.client.get(
            reverse('streamwebs:canopy_cover_edit',
                    kwargs={'site_slug': site.site_slug}
            )
        )
        self.assertContains(
            response, 'You must be logged in to submit data.'
        )
        self.assertEqual(response.status_code, 200)
