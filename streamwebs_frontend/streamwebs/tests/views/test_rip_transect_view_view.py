from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, TransectZone, RiparianTransect


class ViewTransectTestCase(TestCase):
#    def setUp(self):

    def test_data_sheet_view(self):
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        transect = RiparianTransect.objects.create_transect(
            'School Name', '2016-07-22 15:04:00', site
        )
        zone_1 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 1')
        zone_2 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 2')
        zone_3 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 3')
        zone_4 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 4')
        zone_5 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 5')
        response = self.client.get(
                reverse(
                    'streamwebs:riparian_transect_view',
                    kwargs={'data_id': transect.id,
                            'site_slug': transect.site.id
                            }
                )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/riparian_transect_view.html'
        )

    def test_data_sheet_view_content(self):
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        transect = RiparianTransect.objects.create_transect(
            'School Name', '2016-07-22 15:04:00', site
        )
        zone_1 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 1')
        zone_2 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 2')
        zone_3 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 3')
        zone_4 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 4')
        zone_5 = TransectZone.objects.create_zone(transect, 1, 2, 3,
                                                  'This is zone 5')
        response = self.client.get(
                reverse(
                    'streamwebs:riparian_transect_view',
                    kwargs={'data_id': transect.id,
                            'site_slug': transect.site.id
                            }
                )
        )

        self.assertContains(response, 'Riparian Transect')
        self.assertContains(response, 'School Name')
        self.assertContains(response, 'July 22, 2016, 3:04 p.m.')
        self.assertContains(response, 'Site Name')
        self.assertContains(response, 'This is zone 1')
        self.assertContains(response, 'This is zone 2')
        self.assertContains(response, 'This is zone 3')
        self.assertContains(response, 'This is zone 4')
        self.assertContains(response, 'This is zone 5')
