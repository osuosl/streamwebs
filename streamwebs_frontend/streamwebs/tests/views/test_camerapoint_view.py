from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, PhotoPointImage, PhotoPoint, CameraPoint
from streamwebs.util.create_dummy_files import get_temporary_image


class ViewCameraPointTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        site = Site.test_objects.create_site('Rainbows')

        cp = CameraPoint.test_objects.create_camera_point(
            site, '2016-08-13', 'POINT(-121.3846841 44.0612385)')

        pp_1 = PhotoPoint.test_objects.create_photo_point(
            cp, '2016-08-13', 91, 4, 3)
        pp_2 = PhotoPoint.test_objects.create_photo_point(
            cp, '2016-08-13', 92, 5, 4)
        pp_3 = PhotoPoint.test_objects.create_photo_point(
            cp, '2016-08-13', 93, 6, 5)

        ppi_1 = PhotoPointImage.objects.create(  # NOQA
            photo_point=pp_1, image=get_temporary_image(), date='2016-09-13')
        ppi_2 = PhotoPointImage.objects.create(  # NOQA
            photo_point=pp_2, image=get_temporary_image(), date='2016-09-14')
        ppi_3 = PhotoPointImage.objects.create(  # NOQA
            photo_point=pp_3, image=get_temporary_image(), date='2016-09-15')

        self.response = self.client.get(
            reverse('streamwebs:camera_point',
                    kwargs={'site_slug': site.site_slug,
                            'cp_id': cp.id}))

    def test_CameraPoint_view(self):
        """Tests that request for given CP is fulfilled"""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response,
                                'streamwebs/datasheets/camera_point_view.html')

    def test_CameraPoint_data(self):
        """Tests that the view displays the CP's data"""
        # Site data present
        self.assertContains(self.response, 'Rainbows')

        # CP data present
        self.assertContains(self.response, 'Camera Point A')

        # PP data present
        self.assertContains(self.response, 'Photo point 1')
        self.assertContains(self.response, 'Photo point 2')
        self.assertContains(self.response, 'Photo point 3')

        # PPI dates present
        self.assertContains(self.response, '09-13-2016')
        self.assertContains(self.response, '09-14-2016')
        self.assertContains(self.response, '09-15-2016')
