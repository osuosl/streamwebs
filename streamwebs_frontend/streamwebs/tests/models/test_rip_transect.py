from django.test import TestCase
from django.contrib.gis.db import models
from itertools import chain

from streamwebs.models import RiparianTransect, TransectZone, Site


class RiparianTransectTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'names': models.CharField,
            'school': models.CharField,
            'date_time': models.DateTimeField,
            'weather': models.CharField,
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'slope': models.DecimalField,
            'id': models.AutoField,
            'zone_1': models.ForeignKey,
            'zone_2': models.ForeignKey,
            'zone_3': models.ForeignKey,
            'zone_4': models.ForeignKey,
            'zone_5': models.ForeignKey,

            # Corresponding zone id
            'zone_1_id': models.ForeignKey,
            'zone_2_id': models.ForeignKey,
            'zone_3_id': models.ForeignKey,
            'zone_4_id': models.ForeignKey,
            'zone_5_id': models.ForeignKey,
        }

        self.optional_fields = {
            'weather': models.CharField,
            'slope': models.DecimalField,
            'notes': models.TextField,
        }

    def test_fields_exist(self):
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type,
                             type(RiparianTransect._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in RiparianTransect._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(RiparianTransect._meta.get_field(field).blank,
                             True)

    def test_Transect_ManyToOneSite(self):
        """
        A datasheet should correctly correspond to a single site.
        """
        site = Site.objects.create_site('test site', 'test site type',
                                        'test_site_slug')
        zone_1 = TransectZone.zones.create_zone(1, 1, 1, 'Comments on zone 1')
        zone_2 = TransectZone.zones.create_zone(2, 2, 2, 'Comments on zone 2')
        zone_3 = TransectZone.zones.create_zone(3, 3, 3, 'Comments on zone 3')
        zone_4 = TransectZone.zones.create_zone(4, 4, 4, 'Comments on zone 4')
        zone_5 = TransectZone.zones.create_zone(5, 5, 5, 'Comments on zone 5')
        transect = RiparianTransect.transects.create_transect(
            'School of Cool', '2016-07-11 14:09', site, zone_1, zone_2, zone_3,
            zone_4, zone_5)

        self.assertEqual(transect.site.site_name, 'test site')
        self.assertEqual(transect.site.site_type, 'test site type')
        self.assertEqual(transect.site.site_slug, 'test_site_slug')

    def test_datasheet_creation_req_fields(self):
        site = Site.objects.create_site('test site', 'test site type',
                                        'test_site_slug')
        zone_1 = TransectZone.zones.create_zone(1, 1, 1, 'Comments on zone 1')
        zone_2 = TransectZone.zones.create_zone(2, 2, 2, 'Comments on zone 2')
        zone_3 = TransectZone.zones.create_zone(3, 3, 3, 'Comments on zone 3')
        zone_4 = TransectZone.zones.create_zone(4, 4, 4, 'Comments on zone 4')
        zone_5 = TransectZone.zones.create_zone(5, 5, 5, 'Comments on zone 5')
        transect = RiparianTransect.transects.create_transect(
            'School of Cool', '2016-07-11 14:09', site, zone_1, zone_2, zone_3,
            zone_4, zone_5)

        # Required
        self.assertEqual(transect.school, 'School of Cool')
        self.assertEqual(transect.date_time, '2016-07-11 14:09')
        self.assertEqual(transect.site.site_name, 'test site')

        # Optional
        self.assertEqual(transect.names, '')
        self.assertEqual(transect.weather, '')
        self.assertEqual(transect.slope, None)
        self.assertEqual(transect.notes, '')

    def test_datasheet_creation_opt_fields(self):
        site = Site.objects.create_site('test site', 'test site type',
                                        'test_site_slug')
        zone_1 = TransectZone.zones.create_zone(1, 1, 1, 'Comments on zone 1')
        zone_2 = TransectZone.zones.create_zone(2, 2, 2, 'Comments on zone 2')
        zone_3 = TransectZone.zones.create_zone(3, 3, 3, 'Comments on zone 3')
        zone_4 = TransectZone.zones.create_zone(4, 4, 4, 'Comments on zone 4')
        zone_5 = TransectZone.zones.create_zone(5, 5, 5, 'Comments on zone 5')
        transect = RiparianTransect.transects.create_transect(
            'School of Cool', '2016-07-11 14:09', site, zone_1, zone_2, zone_3,
            zone_4, zone_5, 'Cloudy, no meatballs', 1.11, 'Notes on transect')

        # Required
        self.assertEqual(transect.school, 'School of Cool')
        self.assertEqual(transect.date_time, '2016-07-11 14:09')
        self.assertEqual(transect.site.site_name, 'test site')

        # Optional
        self.assertEqual(transect.weather, 'Cloudy, no meatballs')
        self.assertEqual(transect.slope, 1.11)
        self.assertEqual(transect.notes, 'Notes on transect')

    def test_datasheet_SetZonesInfo(self):
        site = Site.objects.create_site('test site', 'test site type',
                                        'test_site_slug')
        zone_1 = TransectZone.zones.create_zone(1, 2, 3, 'Comments on zone 1')
        zone_2 = TransectZone.zones.create_zone(2, 3, 1, 'Comments on zone 2')
        zone_3 = TransectZone.zones.create_zone(3, 2, 1, 'Comments on zone 3')
        zone_4 = TransectZone.zones.create_zone(4, 5, 6, 'Comments on zone 4')
        zone_5 = TransectZone.zones.create_zone(5, 2, 3, 'Comments on zone 5')
        transect = RiparianTransect.transects.create_transect(
            'School of Cool', '2016-07-11 14:09', site, zone_1, zone_2, zone_3,
            zone_4, zone_5)

        self.assertEqual(transect.zone_1.conifers, 1)
        self.assertEqual(transect.zone_1.hardwoods, 2)
        self.assertEqual(transect.zone_1.shrubs, 3)
        self.assertEqual(transect.zone_1.comments, 'Comments on zone 1')

        self.assertEqual(transect.zone_2.conifers, 2)
        self.assertEqual(transect.zone_2.hardwoods, 3)
        self.assertEqual(transect.zone_2.shrubs, 1)
        self.assertEqual(transect.zone_2.comments, 'Comments on zone 2')

        self.assertEqual(transect.zone_3.conifers, 3)
        self.assertEqual(transect.zone_3.hardwoods, 2)
        self.assertEqual(transect.zone_3.shrubs, 1)
        self.assertEqual(transect.zone_3.comments, 'Comments on zone 3')

        self.assertEqual(transect.zone_4.conifers, 4)
        self.assertEqual(transect.zone_4.hardwoods, 5)
        self.assertEqual(transect.zone_4.shrubs, 6)
        self.assertEqual(transect.zone_4.comments, 'Comments on zone 4')

        self.assertEqual(transect.zone_5.conifers, 5)
        self.assertEqual(transect.zone_5.hardwoods, 2)
        self.assertEqual(transect.zone_5.shrubs, 3)
        self.assertEqual(transect.zone_5.comments, 'Comments on zone 5')
