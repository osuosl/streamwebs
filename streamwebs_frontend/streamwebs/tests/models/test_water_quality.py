from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from django.core.exceptions import ValidationError

from streamwebs.models import Site, SiteManager, validate_wq_site
from streamwebs.models import Water_Quality


class WaterQualityTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site': models.ForeignKey,
            'date': models.DateField,
            # 'time': models.TimeField,
            'school': models.CharField,
            'teacher': models.CharField,
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'fish_present': models.BooleanField,
            'live_fish': models.PositiveSmallIntegerField,
            'dead_fish': models.PositiveSmallIntegerField,
            'water_temp': models.DecimalField,
            'air_temp': models.DecimalField,
            'dissolved_O2': models.DecimalField,
            'pH': models.DecimalField,
            'turbidity': models.DecimalField,
            'salinity': models.DecimalField,
            'conductivity': models.DecimalField,
            'total_solids': models.DecimalField,
            'bod': models.DecimalField,
            'ammonia': models.DecimalField,
            'nitrite': models.DecimalField,
            'nitrate': models.DecimalField,
            'phosphates': models.DecimalField,
            'fecal_coliform': models.DecimalField,
            'notes': models.TextField,
            'id': models.AutoField
        }

        # Where does 'Vernier' and 'Manual' fit into the model?
        # Celcius and Fahrenheit?
        # Sample number??

        self.optional_fields = {
            'conductivity',
            'total_solids',
            'bod',
            'ammonia',
            'nitrite',
            'nitrate',
            'phosphate',
            'fecal_coliform',
            'notes',
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'water_quality')
        for field, field_type in self.expected_field.items():
            self.asserEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Water_Quality._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'site')
        for field in self.optional_fields:
            self.assertEqual(
                Water_Quality._meta.get_field(field).blank, True)

    def test_datasheet_OneToOne(self):
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        waterq = Water_Quality.objects.create(site=site, date='2016-06-01',
                                              school='a', teacher='teacher',
                                              latitude=123, longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp=45, air_temp=65,
                                              dissolved_O2=15, pH=6.7,
                                              turbidity=0, salinity=12)
        # waterq = apps.get_model('streamwebs', 'water_quality')
        self.assertEqual(waterq.site.site_name, 'test')
        # check for a match in lat and long?

    def test_datasheet_nonexistent_site(self):
        # site = Site.objects.create('test', 'some_type', 'some_slug')
        no_site_wq = Water_Quality.objects.create(site='nonexistent',
                                                  date='2016-06-01',
                                                  school='a',
                                                  teacher='teacher',
                                                  latitude=123, longitude=123,
                                                  fish_present='False',
                                                  live_fish=0, dead_fish=0,
                                                  water_temp=45, air_temp=65,
                                                  dissolved_O2=15, pH=6.7,
                                                  turbidity=0, salinity=12)
        with self.assertRaises(ValidationError):
            validate_wq_site(no_site_wq.site_name)

    def test_datasheet_bad_site(self):
        # site = Site.objects.create('test', 'some_type', 'some_slug')
        bad_site_wq = Water_Quality.objects.create(site='#@^%--&',
                                                   date='2016-06-01',
                                                   school='a',
                                                   teacher='teacher',
                                                   latitude=123, longitude=123,
                                                   fish_present='False',
                                                   live_fish=0, dead_fish=0,
                                                   water_temp=45, air_temp=65,
                                                   dissolved_O2=15, pH=6.7,
                                                   turbidity=0, salinity=12)
        with self.assertRaises(ValidationError):
            validate_wq_site(bad_site_wq.site_name)
