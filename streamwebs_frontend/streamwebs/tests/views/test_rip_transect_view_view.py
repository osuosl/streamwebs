from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, TransectZone, RiparianTransect


class ViewTransectTestCase(TestCase):

    def test_data_sheet_view(self):
        site = Site.test_objects.create_site('site name')
        transect = RiparianTransect.test_objects.create_transect(
            'School Name', '2016-07-22 15:04:00', site
        )
        zone_1 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 1'
        )
        zone_2 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 2'
        )
        zone_3 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 3'
        )
        zone_4 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 4'
        )
        zone_5 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 5'
        )
        response = self.client.get(
                reverse(
                    'streamwebs:riparian_transect',
                    kwargs={'site_slug': transect.site.site_slug,
                            'data_id': transect.id}
                )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'streamwebs/datasheets/riparian_transect_view.html'
        )

    def test_data_sheet_view_content(self):
        site = Site.test_objects.create_site('Site Name')
        transect = RiparianTransect.test_objects.create_transect(
            'School Name', '2016-07-22 15:04:00', site
        )
        zone_1 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 1'
        )
        zone_2 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 2'
        )
        zone_3 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 3'
        )
        zone_4 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 4'
        )
        zone_5 = TransectZone.test_objects.create_zone(  # NOQA
            transect, 1, 2, 3, 'This is zone 5'
        )
        response = self.client.get(
                reverse(
                    'streamwebs:riparian_transect',
                    kwargs={'site_slug': transect.site.site_slug,
                            'data_id': transect.id}
                )
        )

        self.assertTemplateUsed(
            response, 'streamwebs/datasheets/riparian_transect_view.html'
        )
        self.assertContains(response, 'Riparian Area Transect')
        self.assertContains(response, 'School Name')
        self.assertContains(response, 'July 22, 2016, 3:04 p.m.')
        self.assertContains(response, 'Site Name')
        self.assertContains(response, 'This is zone 1')
        self.assertContains(response, 'This is zone 2')
        self.assertContains(response, 'This is zone 3')
        self.assertContains(response, 'This is zone 4')
        self.assertContains(response, 'This is zone 5')
