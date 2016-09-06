from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, CameraPoint, PhotoPoint, PhotoPointImage


class AddCameraPointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_view_with_bad_blank_data(self):
        """If user submits bad (blank) form, form errors displayed"""
        site = Site.test_objects.create_site('site name', 'Site Type')
        response = self.client.post(
            reverse('streamwebs:camera_point_add',
                    kwargs={'site_slug': site.site_slug}
                    ), {
                'camera_point-TOTAL_FORMS': '3',  # 3 for now
                'camera_point-INITIAL_FORMS': '0',  # none are prefilled
                'camera_point-MAX_NUM_FORMS': ''  # unlimited
                }
        )
        self.assertFormError(response, 'camera_form', 'cp_date',
                             'This field is required.')
        self.assertFormError(response, 'camera_form', 'location',
                             'No geometry value provided.')
        self.assertFalse(response.context['added'])

    def test_view_with_good_data(self):
        """If user submits form with good data, success message displayed"""
        site = Site.test_objects.create_site('site name', 'Site Type')
        response = self.client.post(
            reverse('streamwebs:camera_point_add',
                    kwargs={'site_slug': site.site_slug}), {
                        'site': site.id,
                        'cp_date': '2016-09-01',
                        'location': 'POINT(-121.3846841 44.0612385)',
                        'map_datum': 'WGS84',
                        'description': 'aay',

                        'camera_point-TOTAL_FORMS': '3',  # 3 for now
                        'camera_point-INITIAL_FORMS': '0',  # none prefilled
                        'camera_point-MAX_NUM_FORMS': '',  # unlimited
                        
                        'camera_point-0-pp_date': '2016-09-01',
                        'camera_point-0-compass_bearing': 45,
                        'camera_point-0-distance': 5,
                        'camera_point-0-camera_height': 3,
                        'camera_point-0-notes': 'first pp',

                        'camera_point-1-pp_date': '2016-09-01',
                        'camera_point-1-compass_bearing': 46,
                        'camera_point-1-distance': 4,
                        'camera_point-1-camera_height': 3,
                        'camera_point-1-notes': 'second pp',

                        'camera_point-2-pp_date': '2016-09-01',
                        'camera_point-2-compass_bearing': 24,
                        'camera_point-2-distance': 6,
                        'camera_point-2-camera_height': 3,
                        'camera_point-2-notes': 'third pp'
                    }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/camera_point_add.html'
        )

        self.assertTrue(response.context['added'])
        self.assertEqual(response.status_code, 200)

    def test_view_with_not_logged_in_user(self):
        """If not logged in, user can't view data entry page"""
        site = Site.test_objects.create_site('site name', 'Site Type')
        self.client.logout()
        response = self.client.get(
            reverse('streamwebs:camera_point_add',
                    kwargs={'site_slug': site.site_slug}))
        self.assertContains(response, 'You must be logged in to submit data.')
        self.assertEqual(response.status_code, 200)
