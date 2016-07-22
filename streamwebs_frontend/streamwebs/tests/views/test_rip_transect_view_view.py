from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, TransectZone, RiparianTransect


class ViewTransectTestCase(TestCase):
    def test_data_sheet_view(self):
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        zone_1 = TransectZone.zones.create_zone(1, 2, 3, 'This is zone 1')
        zone_2 = TransectZone.zones.create_zone(1, 2, 3, 'This is zone 2')
        zone_3 = TransectZone.zones.create_zone(1, 2, 3, 'This is zone 3')
        zone_4 = TransectZone.zones.create_zone(1, 2, 3, 'This is zone 4')
        zone_5 = TransectZone.zones.create_zone(1, 2, 3, 'This is zone 5')
        transect = RiparianTransect.transects.create_transect(
            'School Name',
            '2016-07-22 15:04:00',
            site,
            zone_1, zone_2, zone_3, zone_4, zone_5
        )

        response = self.client.get(
                reverse(
                    'streamwebs:riparian_transect_view',
                    kwargs={'site_slug': site.id, 'data_id': transect.id}
                )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/riparian_transect_view.html'
        )
        self.assertContains(response, 'Riparian Transect')
