from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, School, Canopy_Cover


class ViewCanopyCoverTestCase(TestCase):

    def test_data_sheet_view(self):
        site = Site.test_objects.create_site('Test')
        school = School.test_objects.create_school('School Name')
        canopy = Canopy_Cover.objects.create(
            school=school, date_time='2016-09-01 11:54:00',
            site=site, weather='Pleasant', est_canopy_cover=48
        )
        response = self.client.get(
            reverse(
                'streamwebs:canopy_cover',
                kwargs={
                    'data_id': canopy.id,
                    'site_slug': canopy.site.site_slug
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'streamwebs/datasheets/canopy_cover_view.html'
        )

    def test_data_sheet_view_content(self):
        site = Site.test_objects.create_site('Test')
        school = School.test_objects.create_school('School Name')
        canopy = Canopy_Cover.objects.create(
            school=school, date_time='2016-09-01 11:54:00', site=site,
            weather='Pleasant', est_canopy_cover=48
        )
        response = self.client.get(
            reverse(
                'streamwebs:canopy_cover',
                kwargs={
                    'data_id': canopy.id,
                    'site_slug': site.site_slug
                }
            )
        )

        self.assertTemplateUsed(
            response, 'streamwebs/datasheets/canopy_cover_view.html'
        )

        self.assertContains(response, 'Canopy Cover Survey')
        self.assertContains(response, 'School Name')
        self.assertContains(response, 'Sept. 1, 2016, 11:54 a.m.')
        self.assertContains(response, 'Test')  # Site name
