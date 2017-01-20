from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, PhotoPointImage, PhotoPoint, CameraPoint
from streamwebs.util.temp_img import get_temporary_image


class ViewPhotoPointTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

        site = Site.test_objects.create_site('Paradise')

        cp = CameraPoint.test_objects.create_camera_point(
            site, '2016-08-13', 'POINT(-121.3846841 44.0612385)')

        self.pp = PhotoPoint.test_objects.create_photo_point(
            cp, '2016-08-13', 93, 6, 5)

        ppi_1 = PhotoPointImage.objects.create(  # NOQA
            photo_point=self.pp, image=get_temporary_image(),
            date='2016-09-13')
        ppi_2 = PhotoPointImage.objects.create(  # NOQA
            photo_point=self.pp, image=get_temporary_image(),
            date='2016-09-14')
        ppi_3 = PhotoPointImage.objects.create(  # NOQA
            photo_point=self.pp, image=get_temporary_image(),
            date='2016-09-15')

    def test_view_photo_point_info(self):
        """Requested photo point's information should be displayed"""
        response = self.client.get(
            reverse('streamwebs:photo_point',
                    kwargs={'site_slug': self.pp.camera_point.site.site_slug,
                            'cp_id': self.pp.camera_point.id,
                            'pp_id': self.pp.id}))
        self.assertContains(response, 'Paradise')
        self.assertContains(response, 'point A1')
        self.assertContains(response, '08-13-2016')
        self.assertContains(response, 93)
        self.assertContains(response, 6)
        self.assertContains(response, 5)
        self.assertContains(response, "<form id='ppi_form'")

    def test_submit_new_photo(self):
        img = get_temporary_image()

        response = self.client.post(
            reverse('streamwebs:photo_point',
                    kwargs={'site_slug': self.pp.camera_point.site.site_slug,
                            'cp_id': self.pp.camera_point.id,
                            'pp_id': self.pp.id}), {
                        'form-TOTAL_FORMS': '1',
                        'form-INITIAL_FORMS': '0',
                        'form-MAX_NUM_FORMS': '1',
                        'form-MIN_NUM_FORMS': '1',

                        'form-0-image': img,
                        'form-0-date': '2016-09-21',
                    }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/photo_point_view.html'
        )
        self.assertContains(response, "<form id='ppi_form'")
        self.assertTrue(response.context['added'])
        self.assertEqual(response.status_code, 200)

    def test_submit_photo_duplicate_date(self):
        img = get_temporary_image()

        response = self.client.post(
            reverse('streamwebs:photo_point',
                    kwargs={'site_slug': self.pp.camera_point.site.site_slug,
                            'cp_id': self.pp.camera_point.id,
                            'pp_id': self.pp.id}), {
                        'form-TOTAL_FORMS': '1',
                        'form-INITIAL_FORMS': '0',
                        'form-MAX_NUM_FORMS': '1',
                        'form-MIN_NUM_FORMS': '1',

                        'form-0-image': img,
                        'form-0-date': '2016-09-13',
                    }
        )
        self.assertFalse(response.context['added'])
        self.assertContains(response, "<form id='ppi_form'")

    def test_view_with_not_logged_in_user(self):
        """If not logged in, user can't view data entry"""
        self.client.logout()
        response = self.client.get(
            reverse('streamwebs:photo_point',
                    kwargs={'site_slug': self.pp.camera_point.site.site_slug,
                            'cp_id': self.pp.camera_point.id,
                            'pp_id': self.pp.id}))

        self.assertContains(response,
                            'Log in to add photos for this photo point.')
        self.assertNotContains(response, "<form id='ppi_form'")
        self.assertEqual(response.status_code, 200)
