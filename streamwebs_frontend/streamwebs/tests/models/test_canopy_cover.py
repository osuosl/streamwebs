from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from django.utils import timezone
from django.core.exceptions import ValidationError

from streamwebs.models import Site
from streamwebs.models import Canopy_Cover
from streamwebs.models import CC_Cardinal
from streamwebs.models import validate_cover


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
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to is specified site"""
        default_dt = timezone.now()

        site = Site.test_objects.create_site('test')

        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 11)

        east = CC_Cardinal.objects.create_shade('East', True, True, False,
                                                False, False, True, False,
                                                False, True, True, True, False,
                                                True, False, False, False,
                                                False, False, True, True,
                                                False, False, False, False, 8)

        south = CC_Cardinal.objects.create_shade('South', True, True, True,
                                                 False, False, True, False,
                                                 False, True, True, True, True,
                                                 True, False, False, False,
                                                 True, False, True, True,
                                                 False, True, False, True, 14)

        west = CC_Cardinal.objects.create_shade('West', True, True, False,
                                                True, False, True, True, False,
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
        self.assertEqual(canopyc.site.site_slug, 'test')

    def test_datasheet_CreateCanopyCover(self):
        """Tests that a Canopy Cover object is actually created, checks that
           the correct (shaded) value is received from the CC_Cardinal model"""
        default_dt = timezone.now()

        site = Site.test_objects.create_site('test')

        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 11)

        east = CC_Cardinal.objects.create_shade('East', True, True, False,
                                                False, False, True, False,
                                                False, True, True, True, False,
                                                True, False, False, False,
                                                False, False, True, True,
                                                False, False, False, False, 8)

        south = CC_Cardinal.objects.create_shade('South', True, True, True,
                                                 False, False, True, False,
                                                 False, True, True, True, True,
                                                 True, False, False, False,
                                                 True, False, True, True,
                                                 False, True, False, True, 14)

        west = CC_Cardinal.objects.create_shade('West', True, True, False,
                                                True, False, True, True, False,
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
        self.assertEqual(canopyc.north.num_shaded, 11)
        self.assertEqual(canopyc.east.num_shaded, 8)
        self.assertEqual(canopyc.south.num_shaded, 14)
        self.assertEqual(canopyc.west.num_shaded, 17)
        self.assertEqual(canopyc.est_canopy_cover, 50)

    def test_datasheet_CC_CardinalInfo(self):
        """Tests that boolean values are correctly assigned in a
           cardinal box"""
        default_dt = timezone.now()

        north_bools = [True, True, False, False, False, True, False, False,
                       True, True, True, False, True, False, False, False,
                       True, False, True, True, False, True, False, False]

        east_bools = [True, True, False, False, False, True, False, False,
                      True, True, True, False, True, False, False, False,
                      False, False, True, True, False, False, False, False]

        south_bools = [True, True, True, False, False, True, False, False,
                       True, True, True, True, True, False, False, False, True,
                       False, True, True, False, True, False, True]

        west_bools = [True, True, False, True, False, True, True, False,
                      True, True, True, True, True, False, False, True, True,
                      False, True, True, True, True, True, False]

        site = Site.test_objects.create_site('test')

        north = CC_Cardinal.objects.create_shade('North',
                                                 *(north_bools + [11]))

        east = CC_Cardinal.objects.create_shade('East',
                                                *(east_bools + [8]))

        south = CC_Cardinal.objects.create_shade('South',
                                                 *(south_bools + [14]))

        west = CC_Cardinal.objects.create_shade('West',
                                                *(west_bools + [17]))

        canopyc = Canopy_Cover.objects.create(school='School A',
                                              date_time=default_dt, site=site,
                                              weather='cloudy', north=north,
                                              east=east, south=south,
                                              west=west, est_canopy_cover=50)

        for i in range(len(north_bools)):
            north_var = 'canopyc.' + 'north.' + str(chr(i + 65))
            self.assertEqual(eval(north_var), north_bools[i])

        for j in range(len(east_bools)):
            east_var = 'canopyc.' + 'east.' + str(chr(j + 65))
            self.assertEqual(eval(east_var), east_bools[j])

        for k in range(len(south_bools)):
            south_var = 'canopyc.' + 'south.' + str(chr(k + 65))
            self.assertEqual(eval(south_var), south_bools[k])

        for l in range(len(west_bools)):
            west_var = 'canopyc.' + 'west.' + str(chr(l + 65))
            self.assertEqual(eval(west_var), west_bools[l])

        # Check that the direction field is correct for each cardinal box
        self.assertEqual(canopyc.north.direction, 'North')
        self.assertEqual(canopyc.east.direction, 'East')
        self.assertEqual(canopyc.south.direction, 'South')
        self.assertEqual(canopyc.west.direction, 'West')

    def test_validate_cover_good(self):
        """Tests that est_canopy_cover is in between 0-96."""
        default_dt = timezone.now()

        site = Site.test_objects.create_site('test')

        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 11)

        east = CC_Cardinal.objects.create_shade('East', True, True, False,
                                                False, False, True, False,
                                                False, True, True, True, False,
                                                True, False, False, False,
                                                False, False, True, True,
                                                False, False, False, False, 9)

        south = CC_Cardinal.objects.create_shade('South', True, True, True,
                                                 False, False, True, False,
                                                 False, True, True, True, True,
                                                 True, False, False, False,
                                                 True, False, True, True,
                                                 False, True, False, True, 14)

        west = CC_Cardinal.objects.create_shade('West', True, True, False,
                                                True, False, True, True, False,
                                                True, True, True, True, True,
                                                False, False, True, True,
                                                False, True, True, True, True,
                                                True, False, 17)

        canopyc = Canopy_Cover.objects.create(school='School A',
                                              date_time=default_dt, site=site,
                                              weather='cloudy', north=north,
                                              east=east, south=south,
                                              west=west, est_canopy_cover=51)

        self.assertEqual(validate_cover(canopyc.est_canopy_cover), None)

    def test_validate_cover_too_large(self):
        """Tests that validation error is risen when est_canopy_cover
           is too large."""

        default_dt = timezone.now()

        site = Site.test_objects.create_site('test')

        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 11)

        east = CC_Cardinal.objects.create_shade('East', True, True, False,
                                                False, False, True, False,
                                                False, True, True, True, False,
                                                True, False, False, False,
                                                False, False, True, True,
                                                False, False, False, False, 8)

        south = CC_Cardinal.objects.create_shade('South', True, True, True,
                                                 False, False, True, False,
                                                 False, True, True, True, True,
                                                 True, False, False, False,
                                                 True, False, True, True,
                                                 False, True, False, True, 14)

        west = CC_Cardinal.objects.create_shade('West', True, True, False,
                                                True, False, True, True, False,
                                                True, True, True, True, True,
                                                False, False, True, True,
                                                False, True, True, True, True,
                                                True, False, 17)

        canopyc = Canopy_Cover.objects.create(school='School A',
                                              date_time=default_dt, site=site,
                                              weather='cloudy', north=north,
                                              east=east, south=south,
                                              west=west, est_canopy_cover=100)

        with self.assertRaises(ValidationError):
            validate_cover(canopyc.est_canopy_cover)
