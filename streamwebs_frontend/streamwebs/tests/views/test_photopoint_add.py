from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, CameraPoint
from streamwebs.util.temp_img import get_temporary_image


class AddPhotoPointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')
        site = Site.test_objects.create_site('test site')
        self.cp = CameraPoint.test_objects.create_camera_point(
            site, '2016-09-21', 'POINT(-121.3846841 44.0612385)')

    def test_view_with_bad_blank_data(self):
        """If user submits bad (blank) form, form errors displayed"""
        response = self.client.post(
            reverse('streamwebs:photo_point_add',
                    kwargs={'site_slug': self.cp.site.site_slug,
                            'cp_id': self.cp.id}
                    ), {
                'photo_point-TOTAL_FORMS': '1',
                'photo_point-INITIAL_FORMS': '0',
                'photo_point-MAX_NUM_FORMS': '1',
                'photo_point-MIN_NUM_FORMS': '1'
                }
        )
        self.assertFormError(response, 'pp_form', 'camera_point',
                             'This field is required.')
        self.assertFormError(response, 'pp_form', 'pp_date',
                             'This field is required.')
        self.assertFormError(response, 'pp_form', 'compass_bearing',
                             'This field is required.')
        self.assertFormError(response, 'pp_form', 'distance',
                             'This field is required.')
        self.assertFormError(response, 'pp_form', 'camera_height',
                             'This field is required.')
        self.assertFalse(response.context['added'])

    def test_view_with_good_data(self):
        """User submits good data: """
        img = get_temporary_image()

        response = self.client.post(
            reverse('streamwebs:photo_point_add',
                    kwargs={'site_slug': self.cp.site.site_slug,
                            'cp_id': self.cp.id}), {
                        # photo point form
                        'camera_point': self.cp.id,
                        'pp_date': '2016-09-21',
                        'compass_bearing': 90,
                        'distance': 80,
                        'camera_height': 3,
                        'notes': 'hmm',

                        # pp image formset
                        'photo_point-TOTAL_FORMS': '1',
                        'photo_point-INITIAL_FORMS': '0',
                        'photo_point-MAX_NUM_FORMS': '1',
                        'photo_point-MIN_NUM_FORMS': '1',

                        'photo_point-0-image': img,
                        'photo_point-0-date': '2016-09-21',
                    }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/photo_point_add.html'
        )
        self.assertTrue(response.context['added'])
        self.assertEqual(response.status_code, 200)

    def test_view_with_not_logged_in_user(self):
        """If not logged in, user can't view data entry"""
        self.client.logout()
        response = self.client.get(
            reverse('streamwebs:photo_point_add',
                    kwargs={'site_slug': self.cp.site.site_slug,
                            'cp_id': self.cp.id}))

        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:photo_point_add',
                        kwargs={'site_slug': self.cp.site.site_slug,
                                'cp_id': self.cp.id})),
            status_code=302,
            target_status_code=200)
