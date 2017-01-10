from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import (Site, Water_Quality, Macroinvertebrates,
                               RiparianTransect, School)
import tempfile


class RetrieveSiteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        location = 'POINT(44.0612385 -121.3846841)'
        image = tempfile.NamedTemporaryFile(suffix='.jpg').name

        self.site = Site.test_objects.create_site('Test Site', location,
                                                  'Test site description',
                                                  image)

        self.school = School.test_objects.create_school('Test School')

        self.response = self.client.get(reverse(
            'streamwebs:site', kwargs={'site_slug': self.site.site_slug}))

    def test_site_view_status(self):
        """Tests that view's status is 200 and correct template is used"""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'streamwebs/site_detail.html')

    def test_site_view_site_content(self):
        """Tests that view's site info is present"""
        self.assertContains(self.response, 'Test Site')
        self.assertContains(self.response, 'Test site description')
        self.assertContains(self.response, 44.0612385000000017)
        self.assertContains(self.response, -121.3846841000000012)
        self.assertContains(self.response,
                            self.site.created.strftime('%m-%d-%Y %H:%M %Z'))
        self.assertContains(self.response,
                            self.site.modified.strftime('%m-%d-%Y %H:%M %Z'))

    def test_site_view_with_sheets(self):
        """Tests that site displays sheet links if sheets exist"""
        wq_sheet_1 = Water_Quality.test_objects.create_water_quality(  # NOQA
            self.site, '2016-08-25', self.school, 'E', 45, 45, 'False', 0, 0,
            'Fahrenheit', 'Fahrenheit')  # NOQA
        wq_sheet_2 = Water_Quality.test_objects.create_water_quality(  # NOQA
            self.site, '2016-07-25', self.school, 'E', 45, 45, 'False', 0, 0,
            'Fahrenheit', 'Fahrenheit')  # NOQA

        macro_sheet_1 = Macroinvertebrates.test_objects.create_macro(self.site)  # NOQA
        macro_sheet_2 = Macroinvertebrates.test_objects.create_macro(self.site)  # NOQA
        macro_sheet_2.date_time = '2016-08-11 14:09'  # NOQA

        transect_sheet_1 = RiparianTransect.test_objects.create_transect(  # NOQA
            'Test School', '2016-06-25 10:20', self.site)  # NOQA
        transect_sheet_2 = RiparianTransect.test_objects.create_transect(  # NOQA
            'Test School', '2016-05-25 10:20', self.site)  # NOQA

        new_response = self.client.get(reverse(
            'streamwebs:site', kwargs={'site_slug': self.site.site_slug}))

        self.assertContains(new_response, '08-25-2016')
        self.assertContains(new_response, '07-25-2016')
        self.assertContains(
            new_response, 'Macroinvertebrates data: 07-11-2016')
        self.assertContains(
            new_response, 'Riparian transect data: 06-25-2016')
        self.assertContains(
            new_response, 'Riparian transect data: 05-25-2016')
        self.assertNotContains(new_response, 'Canopy cover data')

    def test_site_view_without_sheets(self):
        """Tests that site doesn't display sheet links if no sheets exist"""
        new_response = self.client.get(reverse(
            'streamwebs:site', kwargs={'site_slug': self.site.site_slug}))
        self.assertNotContains(new_response, 'Water quality data')
        self.assertNotContains(new_response, 'Macroinvertebrates data')
        self.assertNotContains(new_response, 'Riparian transect data')
        self.assertNotContains(new_response, 'Canopy cover data')
