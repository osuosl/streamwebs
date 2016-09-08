from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, Canopy_Cover, CC_Cardinal


class ViewCanopyCoverTestCase(TestCase):

    def test_data_sheet_view(self):
        site = Site.test_objects.create_site('Test')
        canopy = Canopy_Cover.objects.create(
            school='School Name', date_time='2016-09-01 11:54:00', 
            site=site, weather='Pleasant', est_canopy_cover=48
        )
        north = CC_Cardinal.test_objects.create_shade(
            'North', True, True, False, True, False, False, False, True, False,
            False, True, True, True, True, True, False, False, True, True,
            False, False, True, True, False, 13, canopy
        )
        east = CC_Cardinal.test_objects.create_shade(
            'East', False, False, False, True, True, False, False, True, False,
            False, True, True, True, False, True, True, False, True, True,
            False, False, True, True, False, 12, canopy
        )
        south =  CC_Cardinal.test_objects.create_shade(
            'South', True, True, False, True, False, False, False, True, False,
            False, True, False, True, True, True, False, False, True, True,
            False, False, False, False, False, 10, canopy
        )
        west = CC_Cardinal.test_objects.create_shade(
            'West', True, False, False, True, True, True, False, True, False,
            False, True, True, False, True, True, False, False, True, True,
            False, False, True, True, False, 13, canopy
        )
        response = self.client.get(
            reverse(
                'streamwebs:canopy_cover',
                kwargs={'data_id': canopy.id,
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
        canopy = Canopy_Cover.objects.create(
            school='School Name', date_time='2016-09-01 11:54:00', site=site,
            weather='Pleasant', est_canopy_cover=48
        )
        north = CC_Cardinal.test_objects.create_shade(
            'North', True, True, False, True, False, False, False, True, False,
            False, True, True, True, True, True, False, False, True, True,
            False, False, True, True, False, 13, canopy
        )
        east = CC_Cardinal.test_objects.create_shade(
            'East', False, False, False, True, True, False, False, True, False,
            False, True, True, True, False, True, True, False, True, True,
            False, False, True, True, False, 12, canopy
        )
        south =  CC_Cardinal.test_objects.create_shade(
            'South', True, True, False, True, False, False, False, True, False,
            False, True, False, True, True, True, False, False, True, True,
            False, False, False, False, False, 10, canopy
        )
        west = CC_Cardinal.test_objects.create_shade(
            'West', True, False, False, True, True, True, False, True, False,
            False, True, True, False, True, True, False, False, True, True,
            False, False, True, True, False, 13, canopy
        )

        response = self.client.get(
            reverse(
                'streamwebs:canopy_cover',
                kwargs={'data_id': canopy.id,
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
        #self.assertContains(response, 'North')
        #self.assertContains(response, 'East')
        #self.assertContains(response, 'South')
        #self.assertContains(response, 'West')
