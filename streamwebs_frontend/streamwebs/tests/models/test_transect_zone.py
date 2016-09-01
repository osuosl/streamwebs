from django.test import TestCase
from django.contrib.gis.db import models
from itertools import chain

from streamwebs.models import TransectZone, RiparianTransect, Site


class TransectZoneTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'conifers': models.PositiveSmallIntegerField,
            'hardwoods': models.PositiveSmallIntegerField,
            'shrubs': models.PositiveSmallIntegerField,
            'comments': models.TextField,
            'id': models.AutoField,

            'transect': models.ForeignKey,
            'transect_id': models.ForeignKey,
        }

        self.optional_fields = {
            'comments': models.TextField,
        }

        site = Site.test_objects.create_site('test site', 'test site type')
        self.transect = RiparianTransect.objects.create_transect(
            'School of Cool', '2016-07-27 10:14', site)

    def test_fields_exist(self):
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type,
                             type(TransectZone._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in TransectZone._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(TransectZone._meta.get_field(field).blank,
                             True)

    def test_Zone_ManyToOneTransect(self):
        zone_1 = TransectZone.objects.create_zone(self.transect)
        zone_2 = TransectZone.objects.create_zone(self.transect, 1, 1, 1,
                                                  'Second zone')

        self.assertEqual(zone_1.transect.school, 'School of Cool')
        self.assertEqual(zone_1.transect.date_time, '2016-07-27 10:14')
        self.assertEqual(zone_1.transect.site.site_name, 'test site')

        self.assertEqual(zone_2.transect.school, 'School of Cool')
        self.assertEqual(zone_2.transect.date_time, '2016-07-27 10:14')
        self.assertEqual(zone_2.transect.site.site_name, 'test site')

    def test_zone_creation_req_fields(self):
        zone = TransectZone.objects.create_zone(self.transect)

        # Required
        self.assertEqual(zone.transect.site.site_name, 'test site')
        self.assertEqual(zone.conifers, 0)
        self.assertEqual(zone.hardwoods, 0)
        self.assertEqual(zone.shrubs, 0)

        # Optional
        self.assertEqual(zone.comments, '')

    def test_zone_creation_opt_fields(self):
        zone = TransectZone.objects.create_zone(self.transect, 1, 2, 3,
                                                'zone comment')
        # Required
        self.assertEqual(zone.transect.site.site_name, 'test site')
        self.assertEqual(zone.conifers, 1)
        self.assertEqual(zone.hardwoods, 2)
        self.assertEqual(zone.shrubs, 3)

        # Optional
        self.assertEqual(zone.comments, 'zone comment')
