from django.test import TestCase

from streamwebs.models import Site
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.apps import apps
from itertools import chain
import tempfile


class SiteTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site_name': models.CharField,
            'description': models.TextField,
            'site_slug': models.SlugField,
            'location': models.PointField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'image': models.ImageField,
            'active': models.BooleanField,
            'id': models.AutoField,

            # Datasheets
            'water_quality': models.ManyToOneRel,
            'macroinvertebrates': models.ManyToOneRel,
            'ripaquaticsurvey': models.ManyToOneRel,
            'ripariantransect': models.ManyToOneRel,
            'canopy_cover': models.ManyToOneRel,
            'camerapoint': models.ManyToOneRel,  # "Photo Point Monitoring"
            'soil_survey': models.ManyToOneRel
        }

        self.optional_fields = {
            'description',
            'image'
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'site')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        # the following is equivalent to MyField._meta.get_all_field_names()
        # which was deprecated  bin Django 1.9
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Site._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'site')
        for field in self.optional_fields:
            self.assertEqual(Site._meta.get_field(field).blank, True)

    def test_site_slug_is_unique(self):
        self.siteA = Site.test_objects.create_site('test site')
        self.siteB = Site.test_objects.create_site('test site')
        self.assertNotEqual(self.siteA.site_slug, self.siteB.site_slug)
        # Long site names are truncated, make sure they are still unique
        self.siteA = Site.test_objects.create_site(
            'test site with a really, really, really, REALLY long name',
        )
        self.siteB = Site.test_objects.create_site(
            'test site with a really, really, really, REALLY long name',
        )
        self.assertNotEqual(self.siteA.site_slug, self.siteB.site_slug)

    def test_site_slug_max_length(self):
        self.siteA = Site.test_objects.create_site(
            'test site with a really, really, really, REALLY long name',
        )
        self.assertIs(len(self.siteA.site_slug), 50)
        # Conflicting long site names must still be max of 50 chars
        self.siteB = Site.test_objects.create_site(
            'test site with a really, really, really, REALLY long name',
        )
        self.assertIs(len(self.siteB.site_slug), 50)

    def test_site_slug_not_empty(self):
        self.site = Site.test_objects.create_site('')
        self.assertIsNotNone(self.site.site_slug)

    def test_obj_creation_req_fields(self):
        """Sites should be created successfully with only req fields"""
        site = Site.test_objects.create_site('Cool Creek')
        self.assertEqual(site.site_name, 'Cool Creek')
        self.assertEqual(site.site_slug, 'cool-creek')
        self.assertEqual(site.location.coords, (-121.3846841, 44.0612385))
        self.assertEqual(site.description, '')
        self.assertEqual(site.image, None)

    def test_obj_creation_opt_fields(self):
        """Sites should be created successfully with both req and opt fields"""
        point = Point(-120.2684184, 44.3910532)
        temp_photo = tempfile.NamedTemporaryFile(suffix='.jpg').name

        site = Site.test_objects.create_site('Cool Creek', point,
                                             'A very cool creek', temp_photo)

        self.assertEqual(site.site_name, 'Cool Creek')
        self.assertEqual(site.site_slug, 'cool-creek')
        self.assertEqual(site.location.coords, (-120.2684184, 44.3910532))
        self.assertEqual(site.description, 'A very cool creek')
        self.assertEqual(site.image, temp_photo)
