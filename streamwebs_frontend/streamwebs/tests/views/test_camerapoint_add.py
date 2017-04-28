from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, CameraPoint
from streamwebs.util.create_dummy_files import get_temporary_image


class AddCameraPointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_view_with_bad_blank_data(self):
        """If user submits bad (blank) form, form errors displayed"""
        site = Site.test_objects.create_site('site name')
        response = self.client.post(
            reverse('streamwebs:camera_point_add',
                    kwargs={'site_slug': site.site_slug}
                    ), {
                'camera_point-TOTAL_FORMS': '3',  # 3 for now
                'camera_point-INITIAL_FORMS': '0',  # none are prefilled
                'camera_point-MAX_NUM_FORMS': '3',
                'camera_point-MIN_NUM_FORMS': '3',

                'form-TOTAL_FORMS': '3',  # 3 for now
                'form-INITIAL_FORMS': '0',  # none are prefilled
                'form-MAX_NUM_FORMS': '3',
                'form-MIN_NUM_FORMS': '3',
                }
        )
        self.assertFormError(response, 'camera_form', 'cp_date',
                             'This field is required.')
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/camera_point_add.html'
        )

    def test_view_with_good_data(self):
        """If user submits form with good data, success message displayed"""
        site = Site.test_objects.create_site('site name')

        img_1 = get_temporary_image()
        img_2 = get_temporary_image()
        img_3 = get_temporary_image()

        response = self.client.post(
            reverse('streamwebs:camera_point_add',
                    kwargs={'site_slug': site.site_slug}), {
                        # camera point form
                        'site': site.id,
                        'cp_date': '2016-09-01',
                        'location': 'POINT(-121.3846841 44.0612385)',
                        'map_datum': 'WGS84',
                        'description': 'aay',
                        'lat': '-121.3846841',
                        'lng': '44.0612385',

                        # photo point formset
                        'camera_point-TOTAL_FORMS': '3',  # 3 for now
                        'camera_point-INITIAL_FORMS': '0',  # none prefilled
                        'camera_point-MAX_NUM_FORMS': '3',
                        'camera_point-MIN_NUM_FORMS': '3',

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
                        'camera_point-2-notes': 'third pp',

                        # photo point image formset
                        'form-TOTAL_FORMS': '3',  # 3 for now
                        'form-INITIAL_FORMS': '0',  # none prefilled
                        'form-MAX_NUM_FORMS': '3',
                        'form-MIN_NUM_FORMS': '3',

                        'form-0-image': img_1,
                        'form-0-date': '2016-09-06',

                        'form-1-image': img_2,
                        'form-1-date': '2016-09-05',

                        'form-2-image': img_3,
                        'form-2-date': '2016-09-04',
                    }
        )
        self.assertTemplateNotUsed(
            response,
            'streamwebs/datasheets/camera_point_add.html'
        )
        self.assertRedirects(
            response,
            reverse('streamwebs:camera_point',
                    kwargs={'site_slug': site.site_slug,
                            'cp_id': CameraPoint.test_objects.last().id}
                    ),
            status_code=302,
            target_status_code=200)

    def test_view_with_not_logged_in_user(self):
        """If not logged in, user can't view data entry page"""
        site = Site.test_objects.create_site('site name')
        self.client.logout()
        response = self.client.get(
            reverse('streamwebs:camera_point_add',
                    kwargs={'site_slug': site.site_slug}))

        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:camera_point_add',
                        kwargs={'site_slug': site.site_slug})),
            status_code=302,
            target_status_code=200)
