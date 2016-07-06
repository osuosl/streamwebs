from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Site
from streamwebs.models import Rip_Aqua_Survey
from streamwebs.models import Rip_Aqua_Survey_Plants
from streamwebs.models import Rip_Aqua_Survey_Wildlife

class RipAquaSurveyPlantTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            'species': models.CharField,
            'significance': models.CharField,
        }
        self.optional_fields = {
            'species',
            'significance',
        }

class RipAquaSurveyWildLifeTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            'track': models.CharField,
            'comments': models.CharField,
        }
        self.optional_fields = {
            'track',
            'comments',
        }

class RipAquaSurveyTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            # Form header
            'date': models.DateField,
            'school': models.CharField,
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'weather': models.CharField,
            # Survey Area
            'stream_length': models.PositiveSmallIntegerField,
            'riffle_count': models.PositiveSmallIntegerField,
            'pool_count': models.PositiveSmallIntegerField,
            # Substrate
            'silt': models.CharField,
            'sand': models.CharField,
            'gravel': models.CharField,
            'cobble': models.CharField,
            'boulders': models.CharField,
            'bedrock': models.CharField,
            # Instream Woody Debris
            'wood_debris_small': models.CharField,
            'wood_debris_med': models.CharField,
            'wood_debris_lrg': models.CharField,
            'comments': models.CharField,
            # Vegetation Types
            'conif_trees': models.CharField,
            'decid_trees': models.CharField,
            'shrubs': models.CharField,
            'small_plants': models.CharField,
            'ferns': models.CharField,
            'grasses': models.CharField,
            # Plants Identified
            'plants_1': models.ForeignKey,
            'plants_2': models.ForeignKey,
            'plants_3': models.ForeignKey,
            'plants_4': models.ForeignKey,
            'plants_5': models.ForeignKey,
            'plants_6': models.ForeignKey,
            # Wildlife & Birds Identified
            'wildlife_1': models.ForeignKey,
            'wildlife_2': models.ForeignKey,
            'wildlife_3': models.ForeignKey,
            'wildlife_4': models.ForeignKey,
            'wildlife_5': models.ForeignKey,
            'wildlife_6': models.ForeignKey,
            # Plants & wildlife IDs
            'plants_1_id': models.ForeignKey,
            'plants_2_id': models.ForeignKey,
            'plants_3_id': models.ForeignKey,
            'plants_4_id': models.ForeignKey,
            'plants_5_id': models.ForeignKey,
            'plants_6_id': models.ForeignKey,
            'wildlife_1_id': models.ForeignKey,
            'wildlife_2_id': models.ForeignKey,
            'wildlife_3_id': models.ForeignKey,
            'wildlife_4_id': models.ForeignKey,
            'wildlife_5_id': models.ForeignKey,
            'wildlife_6_id': models.ForeignKey,

        }
        self.optional_fields = {
           'comments',
           'plants_1',
           'plants_2',
           'plants_3',
           'plants_4',
           'plants_5',
           'plants_6',
           'wildlife_1',
           'wildlife_2',
           'wildlife_3',
           'wildlife_4',
           'wildlife_5',
           'wildlife_6',
           # Plants Identified
           'plants_1_id',
           'plants_2_id',
           'plants_3_id',
           'plants_4_id',
           'plants_5_id',
           'plants_6_id',
           # Wildlife & Birds Identified
           'wildlife_1_id',
           'wildlife_2_id',
           'wildlife_3_id',
           'wildlife_4_id',
           'wildlife_5_id',
           'wildlife_6_id',
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'rip_aqua_survey')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        model = Rip_Aqua_Survey
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in model._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to a specified site"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        plant_1 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus1", "not really")
        plant_2 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus2", "dope")
        plant_3 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus3", "asdfasdf")
        plant_4 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus4", "sorta")
        plant_5 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus5", "kinda")
        plant_6 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus6", "gottacatchemall")

        wl_1 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog", "not really")
        wl_2 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog1", "not really")
        wl_3 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog2", "not really")
        wl_4 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog3", "not really")
        wl_5 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog4", "not really")
        wl_6 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog5", "not really")

        survey = Rip_Aqua_Survey.objects.create(date= '2016-07-06',
                                                school= "OSU BEST SCHOOL",
                                                site= site,
                                                weather= "A lot",
                                                # Survey Area
                                                stream_length= 15,
                                                riffle_count= 1,
                                                pool_count= 2,
                                                # Substrate
                                                silt= "A lot",
                                                sand= "A lot",
                                                gravel= "A lot",
                                                cobble= "A lot",
                                                boulders= "A lot",
                                                bedrock= "A lot",
                                                # Instream Woody Debris
                                                wood_debris_small= "A lot",
                                                wood_debris_med= "A lot",
                                                wood_debris_lrg= "A lot",
                                                comments="it's chill",
                                                # Vegetation Types
                                                conif_trees= "A lot",
                                                decid_trees= "A lot",
                                                shrubs= "A lot",
                                                small_plants= "A lot",
                                                ferns= "A lot",
                                                grasses= "A lot",
                                                # Plants Identified
                                                plants_1= plant_1,
                                                plants_2= plant_2,
                                                plants_3= plant_3,
                                                plants_4= plant_4,
                                                plants_5= plant_5,
                                                plants_6= plant_6,
                                                # Wildlife & Birds Identified
                                                wildlife_1= wl_1,
                                                wildlife_2= wl_2,
                                                wildlife_3= wl_3,
                                                wildlife_4= wl_4,
                                                wildlife_5= wl_5,
                                                wildlife_6= wl_6
        )

        # Assert that site data matches the newly created test site
        self.assertEqual(survey.site.site_name, 'test')
        self.assertEqual(survey.site.site_type, 'some_type')
        self.assertEqual(survey.site.site_slug, 'some_slug')

    def test_datasheet_RequiredFields(self):
        """Tests that a datasheet correctly corresponds to a specified
           plant/wildlife entry - optional fields"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        plant_1 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus1", "not really")
        plant_2 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus2", "dope")

        wl_1 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog", "not really")
        wl_2 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog1", "not really")

        survey = Rip_Aqua_Survey.objects.create(date= '2016-07-06',
                                                school= "OSU BEST SCHOOL",
                                                site= site,
                                                weather= "A lot",
                                                # Survey Area
                                                stream_length= 15,
                                                riffle_count= 1,
                                                pool_count= 2,
                                                # Substrate
                                                silt= "A lot",
                                                sand= "A lot",
                                                gravel= "A lot",
                                                cobble= "A lot",
                                                boulders= "A lot",
                                                bedrock= "A lot",
                                                # Instream Woody Debris
                                                wood_debris_small= "A lot",
                                                wood_debris_med= "A lot",
                                                wood_debris_lrg= "A lot",
                                                comments="it's chill",
                                                # Vegetation Types
                                                conif_trees= "A lot",
                                                decid_trees= "A lot",
                                                shrubs= "A lot",
                                                small_plants= "A lot",
                                                ferns= "A lot",
                                                grasses= "A lot",
                                                # Plants Identified
                                                plants_1= plant_1,
                                                plants_2= plant_2,

                                                # Wildlife & Birds Identified
                                                wildlife_1= wl_1,
                                                wildlife_2= wl_2,
        )

        # Assert the required fields
        self.assertEqual(survey.date, '2016-07-06')
        self.assertEqual(survey.school, "OSU BEST SCHOOL")
        self.assertEqual(survey.site, site)
        self.assertEqual(survey.weather, "A lot")
        self.assertEqual(survey.stream_length, 15)
        self.assertEqual(survey.riffle_count, 1)
        self.assertEqual(survey.pool_count, 2)
        self.assertEqual(survey.silt, "A lot")
        self.assertEqual(survey.sand, "A lot")
        self.assertEqual(survey.gravel, "A lot")
        self.assertEqual(survey.cobble, "A lot")
        self.assertEqual(survey.boulders, "A lot")
        self.assertEqual(survey.bedrock, "A lot")
        self.assertEqual(survey.wood_debris_small, "A lot")
        self.assertEqual(survey.wood_debris_med, "A lot")
        self.assertEqual(survey.wood_debris_lrg, "A lot")
        self.assertEqual(survey.comments,"it's chill")
        self.assertEqual(survey.conif_trees, "A lot")
        self.assertEqual(survey.decid_trees, "A lot")
        self.assertEqual(survey.shrubs, "A lot")
        self.assertEqual(survey.small_plants, "A lot")
        self.assertEqual(survey.ferns, "A lot")
        self.assertEqual(survey.grasses, "A lot")

    def test_datasheet_OptionalFields(self):
        """Tests that a datasheet correctly corresponds to a specified
           plant/wildlife entry - optional fields"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        plant_1 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus1", "not really")
        plant_2 = Rip_Aqua_Survey_Plants.objects.create_sample("cactus2", "dope")

        wl_1 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog", "not really")
        wl_2 = Rip_Aqua_Survey_Wildlife.objects.create_sample("dog1", "not really")

        survey = Rip_Aqua_Survey.objects.create(date= '2016-07-06',
                                                school= "OSU BEST SCHOOL",
                                                site= site,
                                                weather= "A lot",
                                                # Survey Area
                                                stream_length= 15,
                                                riffle_count= 1,
                                                pool_count= 2,
                                                # Substrate
                                                silt= "A lot",
                                                sand= "A lot",
                                                gravel= "A lot",
                                                cobble= "A lot",
                                                boulders= "A lot",
                                                bedrock= "A lot",
                                                # Instream Woody Debris
                                                wood_debris_small= "A lot",
                                                wood_debris_med= "A lot",
                                                wood_debris_lrg= "A lot",
                                                comments="it's chill",
                                                # Vegetation Types
                                                conif_trees= "A lot",
                                                decid_trees= "A lot",
                                                shrubs= "A lot",
                                                small_plants= "A lot",
                                                ferns= "A lot",
                                                grasses= "A lot",
                                                # Plants Identified
                                                plants_1= plant_1,
                                                plants_2= plant_2,

                                                # Wildlife & Birds Identified
                                                wildlife_1= wl_1,
                                                wildlife_2= wl_2,
        )

        # Assert that the optional comment field works
        self.assertEqual(survey.comments, "it's chill")

        # Assert that the optional fields for each of the 2 plant identifications
        # and 2 wildlife identifications are for the datasheet
        self.assertEqual(survey.plants_1.species, "cactus1")
        self.assertEqual(survey.plants_1.significance, "not really")

        self.assertEqual(survey.plants_2.species, "cactus2")
        self.assertEqual(survey.plants_2.significance,  "dope")

        self.assertEqual(survey.wildlife_1.track, "dog")
        self.assertEqual(survey.wildlife_1.comments, "not really")

        self.assertEqual(survey.wildlife_2.track, "dog1")
        self.assertEqual(survey.wildlife_2.comments, "not really")

# Note: Not of high priority (since Django probably doesn't allow it in the
#       first place), but may want to eventually add tests that assert
#       datasheet creation fails when given a nonexistent or bad site
#           * def test_datasheet_nonexistent_site(self):
#           * def test_datasheet_bad_site(self):
