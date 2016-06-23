from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Site
from streamwebs.models import Water_Quality
from streamwebs.models import Measurements


class WaterQualityTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'DEQ_wq_level': models.CharField,
            'date': models.DateField,
            'school': models.CharField,
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'fish_present': models.BooleanField,
            'live_fish': models.PositiveSmallIntegerField,
            'dead_fish': models.PositiveSmallIntegerField,
            'water_temp_unit': models.CharField,
            'air_temp_unit': models.CharField,
            'water_temp': models.DecimalField,
            'water_temp_info': models.ForeignKey,
            'air_temp': models.DecimalField,
            'air_temp_info': models.ForeignKey,
            'dissolved_oxygen': models.DecimalField,
            'oxygen_info': models.ForeignKey,
            'pH': models.DecimalField,
            'pH_info': models.ForeignKey,
            'turbidity': models.DecimalField,
            'turbid_info': models.ForeignKey,
            'salinity': models.DecimalField,
            'salt_info': models.ForeignKey,
            'conductivity': models.DecimalField,
            'conductivity_info': models.ForeignKey,
            'total_solids': models.DecimalField,
            'tot_solids_info': models.ForeignKey,
            'bod': models.DecimalField,
            'bod_info': models.ForeignKey,
            'ammonia': models.DecimalField,
            'ammonia_info': models.ForeignKey,
            'nitrite': models.DecimalField,
            'nitrite_info': models.ForeignKey,
            'nitrate': models.DecimalField,
            'nitrate_info': models.ForeignKey,
            'phosphates': models.DecimalField,
            'phosphate_info': models.ForeignKey,
            'fecal_coliform': models.DecimalField,
            'fecal_info': models.ForeignKey,
            'notes': models.TextField,
            'id': models.AutoField,

            # Corresponding measurement entry (id)
            'water_temp_info_id': models.ForeignKey,
            'air_temp_info_id': models.ForeignKey,
            'oxygen_info_id': models.ForeignKey,
            'pH_info_id': models.ForeignKey,
            'turbid_info_id': models.ForeignKey,
            'salt_info_id': models.ForeignKey,

            # Measurement entry ids for optional fields
            'conductivity_info_id': models.ForeignKey,
            'tot_solids_info_id': models.ForeignKey,
            'bod_info_id': models.ForeignKey,
            'ammonia_info_id': models.ForeignKey,
            'nitrite_info_id': models.ForeignKey,
            'nitrate_info_id': models.ForeignKey,
            'phosphate_info_id': models.ForeignKey,
            'fecal_info_id': models.ForeignKey
        }

        self.optional_fields = {
            'conductivity',
            'total_solids',
            'bod',
            'ammonia',
            'nitrite',
            'nitrate',
            'phosphates',
            'fecal_coliform',
            'notes'
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'water_quality')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Water_Quality._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'water_quality')
        for field in self.optional_fields:
            self.assertEqual(
                Water_Quality._meta.get_field(field).blank, True)

    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to a specified site"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        water_temp_info = Measurements.objects.create_measurement_info(
                          'Water Quality', 'Water Temperature', 1, 'Manual')
        air_temp_info = Measurements.objects.create_measurement_info(
                        'Water Quality', 'Air Temperature', 1, 'Manual')
        oxygen_info = Measurements.objects.create_measurement_info(
                      'Water Quality', 'Dissolved Oxygen', 1, 'Vernier')
        pH_info = Measurements.objects.create_measurement_info(
                  'Water Quality', 'pH', 1, 'Vernier')
        turbid_info = Measurements.objects.create_measurement_info(
                      'Water Quality', 'Turbidity', 1, 'Manual')
        salt_info = Measurements.objects.create_measurement_info(
                    'Water Quality', 'Salinity', 1, 'Vernier')
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              water_temp=45,
                                              water_temp_info=water_temp_info,
                                              air_temp=65,
                                              air_temp_info=air_temp_info,
                                              dissolved_oxygen=15,
                                              oxygen_info=oxygen_info,
                                              pH=6.7,
                                              pH_info=pH_info,
                                              turbidity=0,
                                              turbid_info=turbid_info,
                                              salinity=12,
                                              salt_info=salt_info)
        self.assertEqual(waterq.site.site_name, 'test')
        self.assertEqual(waterq.site.site_type, 'some_type')
        self.assertEqual(waterq.site.site_slug, 'some_slug')

    def test_datasheet_SetMeasurementInfo(self):
        """Tests that a datasheet correctly corresponds to a specified
           measurement entry - required fields"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        water_temp_info = Measurements.objects.create_measurement_info(
                          'Water Quality', 'Water Temperature', 1, 'Manual')
        air_temp_info = Measurements.objects.create_measurement_info(
                        'Water Quality', 'Air Temperature', 1, 'Manual')
        oxygen_info = Measurements.objects.create_measurement_info(
                      'Water Quality', 'Dissolved Oxygen', 1, 'Vernier')
        pH_info = Measurements.objects.create_measurement_info(
                  'Water Quality', 'pH', 1, 'Vernier')
        turbid_info = Measurements.objects.create_measurement_info(
                      'Water Quality', 'Turbidity', 1, 'Manual')
        salt_info = Measurements.objects.create_measurement_info(
                    'Water Quality', 'Salinity', 1, 'Vernier')
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              water_temp=45,
                                              water_temp_info=water_temp_info,
                                              air_temp=65,
                                              air_temp_info=air_temp_info,
                                              dissolved_oxygen=15,
                                              oxygen_info=oxygen_info,
                                              pH=6.7,
                                              pH_info=pH_info,
                                              turbidity=0,
                                              turbid_info=turbid_info,
                                              salinity=12,
                                              salt_info=salt_info)
        # Assert that each field (and its additional measurement info) has been
        # properly set
        self.assertEqual(waterq.water_temp_info.datasheet_type,
                         'Water Quality')
        self.assertEqual(waterq.water_temp_info.measuring, 'Water Temperature')
        self.assertEqual(waterq.water_temp_info.sample_number, 1)
        self.assertEqual(waterq.water_temp_info.tool, 'Manual')

        self.assertEqual(waterq.air_temp_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.air_temp_info.measuring, 'Air Temperature')
        self.assertEqual(waterq.air_temp_info.sample_number, 1)
        self.assertEqual(waterq.air_temp_info.tool, 'Manual')

        self.assertEqual(waterq.oxygen_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.oxygen_info.measuring, 'Dissolved Oxygen')
        self.assertEqual(waterq.oxygen_info.sample_number, 1)
        self.assertEqual(waterq.oxygen_info.tool, 'Vernier')

        self.assertEqual(waterq.pH_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.pH_info.measuring, 'pH')
        self.assertEqual(waterq.pH_info.sample_number, 1)
        self.assertEqual(waterq.pH_info.tool, 'Vernier')

        self.assertEqual(waterq.turbid_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.turbid_info.measuring, 'Turbidity')
        self.assertEqual(waterq.turbid_info.sample_number, 1)
        self.assertEqual(waterq.turbid_info.tool, 'Manual')

        self.assertEqual(waterq.salt_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.salt_info.measuring, 'Salinity')
        self.assertEqual(waterq.salt_info.sample_number, 1)
        self.assertEqual(waterq.salt_info.tool, 'Vernier')

    def test_datasheet_AdditionalMeasurementInfo(self):
        """Tests that a datasheet correctly corresponds to a specified
           measurement entry - additional fields"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        # The following fields are required
        water_temp_info = Measurements.objects.create_measurement_info(
                          'Water Quality', 'Water Temperature', 1, 'Manual')
        air_temp_info = Measurements.objects.create_measurement_info(
                        'Water Quality', 'Air Temperature', 1, 'Manual')
        oxygen_info = Measurements.objects.create_measurement_info(
                      'Water Quality', 'Dissolved Oxygen', 1, 'Vernier')
        pH_info = Measurements.objects.create_measurement_info(
                  'Water Quality', 'pH', 1, 'Vernier')
        turbid_info = Measurements.objects.create_measurement_info(
                      'Water Quality', 'Turbidity', 1, 'Manual')
        salt_info = Measurements.objects.create_measurement_info(
                    'Water Quality', 'Salinity', 1, 'Vernier')

        # The following fields are additional/optional
        conduct_info = Measurements.objects.create_additional_info(
                       'Water Quality', 'Conductivity', 1)
        tot_solids_info = Measurements.objects.create_additional_info(
                          'Water Quality', 'Total Solids', 1)
        bod_info = Measurements.objects.create_additional_info(
                   'Water Quality', 'Bod', 1)
        ammonia_info = Measurements.objects.create_additional_info(
                       'Water Quality', 'Ammonia', 1)
        nitrite_info = Measurements.objects.create_additional_info(
                       'Water Quality', 'Nitrite', 1)
        nitrate_info = Measurements.objects.create_additional_info(
                       'Water Quality', 'Nitrate', 1)
        phosphate_info = Measurements.objects.create_additional_info(
                        'Water Quality', 'Phosphates', 1)
        fecal_info = Measurements.objects.create_additional_info(
                     'Water Quality', 'Fecal Coliform', 1)

        # Creating a test datasheet, this time w/ additional parameters defined
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              water_temp=45,
                                              water_temp_info=water_temp_info,
                                              air_temp=65,
                                              air_temp_info=air_temp_info,
                                              dissolved_oxygen=15,
                                              oxygen_info=oxygen_info,
                                              pH=6.7,
                                              pH_info=pH_info,
                                              turbidity=0,
                                              turbid_info=turbid_info,
                                              salinity=12,
                                              salt_info=salt_info,
                                              conductivity=7,
                                              conductivity_info=conduct_info,
                                              total_solids=20,
                                              tot_solids_info=tot_solids_info,
                                              bod=3,
                                              bod_info=bod_info,
                                              ammonia=0.075,
                                              ammonia_info=ammonia_info,
                                              nitrite=2.3,
                                              nitrite_info=nitrite_info,
                                              nitrate=2.25,
                                              nitrate_info=nitrate_info,
                                              phosphates=1.2,
                                              phosphate_info=phosphate_info,
                                              fecal_coliform=0.75,
                                              fecal_info=fecal_info)

        self.assertEqual(
            waterq.conductivity_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.conductivity_info.measuring, 'Conductivity')
        self.assertEqual(waterq.conductivity_info.sample_number, 1)

        self.assertEqual(
            waterq.tot_solids_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.tot_solids_info.measuring, 'Total Solids')
        self.assertEqual(waterq.tot_solids_info.sample_number, 1)

        self.assertEqual(waterq.bod_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.bod_info.measuring, 'Bod')
        self.assertEqual(waterq.bod_info.sample_number, 1)

        self.assertEqual(waterq.ammonia_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.ammonia_info.measuring, 'Ammonia')
        self.assertEqual(waterq.ammonia_info.sample_number, 1)

        self.assertEqual(waterq.nitrite_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.nitrite_info.measuring, 'Nitrite')
        self.assertEqual(waterq.nitrite_info.sample_number, 1)

        self.assertEqual(waterq.nitrate_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.nitrate_info.measuring, 'Nitrate')
        self.assertEqual(waterq.nitrate_info.sample_number, 1)

        self.assertEqual(waterq.phosphate_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.phosphate_info.measuring, 'Phosphates')
        self.assertEqual(waterq.phosphate_info.sample_number, 1)

        self.assertEqual(waterq.fecal_info.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.fecal_info.measuring, 'Fecal Coliform')
        self.assertEqual(waterq.fecal_info.sample_number, 1)

# Note: Not of high priority (since Django probably doesn't allow it in the
#       first place), but may want to eventually add tests that assert
#       datasheet creation fails when given a nonexistent or bad site
#           * def test_datasheet_nonexistent_site(self):
#           * def test_datasheet_bad_site(self):
