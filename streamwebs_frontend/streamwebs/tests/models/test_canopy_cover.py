from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from django.utils import timezone

from streamwebs.models import Site
from streamwebs.models import Canopy_Cover
from streamwebs.models import CC_Cardinal


class CanopyCovTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'school': models.CharField,
            'date_time': models.DateTimeField,
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'weather': models.CharField,
            'north': models.ForeignKey,
            'east': models.ForeignKey,
            'south': models.ForeignKey,
            'west': models.ForeignKey,
            'est_canopy_cover': models.PositiveIntegerField,
            'id': models.AutoField,

            # Corresponding cardinal direction (id for CC_Cardinal)
            'north_id': models.ForeignKey,
            'east_id': models.ForeignKey,
            'south_id': models.ForeignKey,
            'west_id': models.ForeignKey
        }

    def test_fields_exist(self):
        """Checks that the expected fields have been created"""
        model = apps.get_model('streamwebs', 'canopy_cover')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        """Checks for discrepancies between the actual model and its expected
           fields"""
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Canopy_Cover._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.key()))

    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to is specified site"""
        default_dt = timezone.now()

        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        north = CC_Cardinal.objects.create_shade(True, True, False, False,
                                                 False, True, False, False,
                                                 True, True, True, False, True,
                                                 False, False, False, True,
                                                 False, True, True, False,
                                                 True, False, False, 11)

        east = CC_Cardinal.objects.create_shade(True, True, False, False,
                                                False, True, False, False,
                                                True, True, True, False, True,
                                                False, False, False, False,
                                                False, True, True, False,
                                                False, False, False, 8)

        south = CC_Cardinal.objects.create_shade(True, True, True, False,
                                                 False, True, False, False,
                                                 True, True, True, True, True,
                                                 False, False, False, True,
                                                 False, True, True, False,
                                                 True, False, True, 14)

        west = CC_Cardinal.objects.create_shade(True, True, False, True,
                                                False, True, True, False,
                                                True, True, True, True, True,
                                                False, False, True, True,
                                                False, True, True, True, True,
                                                True, False, 17)

        canopyc = Canopy_Cover.objects.create(school='School A',
                                              date_time=default_dt, site=site,
                                              weather='cloudy', north=north,
                                              east=east, south=south,
                                              west=west, est_canopy_cover=50)

        self.assertEqual(canopyc.site.site_name, 'test')
        self.assertEqual(canopyc.site.site_type, 'some_type')
        self.assertEqual(canopyc.site.site_slug, 'some_slug')

    def test_datasheet_CreateCanopyCover(self):
        """Tests that a Canopy Cover object is actually created, checks that
           the correct (shaded) value is received from the CC_Cardinal model"""
        default_dt = timezone.now()

        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        north = CC_Cardinal.objects.create_shade(True, True, False, False,
                                                 False, True, False, False,
                                                 True, True, True, False, True,
                                                 False, False, False, True,
                                                 False, True, True, False,
                                                 True, False, False, 11)

        east = CC_Cardinal.objects.create_shade(True, True, False, False,
                                                False, True, False, False,
                                                True, True, True, False, True,
                                                False, False, False, False,
                                                False, True, True, False,
                                                False, False, False, 8)

        south = CC_Cardinal.objects.create_shade(True, True, True, False,
                                                 False, True, False, False,
                                                 True, True, True, True, True,
                                                 False, False, False, True,
                                                 False, True, True, False,
                                                 True, False, True, 14)

        west = CC_Cardinal.objects.create_shade(True, True, False, True,
                                                False, True, True, False,
                                                True, True, True, True, True,
                                                False, False, True, True,
                                                False, True, True, True, True,
                                                True, False, 17)

        canopyc = Canopy_Cover.objects.create(school='School A',
                                              date_time=default_dt, site=site,
                                              weather='cloudy', north=north,
                                              east=east, south=south,
                                              west=west, est_canopy_cover=50)

        self.assertEqual(canopyc.school, 'School A')
        self.assertEqual(canopyc.date_time, default_dt)
        self.assertEqual(canopyc.weather, 'cloudy')
        self.assertEqual(canopyc.north.shaded, 11)
        self.assertEqual(canopyc.east.shaded, 8)
        self.assertEqual(canopyc.south.shaded, 14)
        self.assertEqual(canopyc.west.shaded, 17)
        self.assertEqual(canopyc.est_canopy_cover, 50)
