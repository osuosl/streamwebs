from django.test import TestCase
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from streamwebs.models import CameraPoint, Site
import datetime


class CameraPointTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'letter': models.CharField,
            'cp_date': models.DateField,
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'map_datum': models.CharField,
            'description': models.TextField,
            'id': models.AutoField,

            'camera_point': models.ManyToOneRel
        }

        self.optional_fields = {
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'map_datum': models.CharField,
            'description': models.TextField
        }

        self.site = Site.test_objects.create_site('test site a',
                                                  'test site type a',
                                                  'test_site_slug_a')

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'camerapoint')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        cp_fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in CameraPoint._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
            )))
        self.assertEqual(sorted(cp_fields),
                         sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(
                CameraPoint._meta.get_field(field).blank, True)

    def test_CameraPoint_ManyToOneSite(self):
        """
        A camera point should correspond to a single specified site.
        """
        cp_date = datetime.date.today()

        camera_point = CameraPoint.test_objects.create_camera_point(
            site=self.site,
            letter='A',
            cp_date=cp_date
        )

        self.assertEqual(camera_point.site.site_name, 'test site a')
        self.assertEqual(camera_point.site.site_type, 'test site type a')
        self.assertEqual(camera_point.site.site_slug, 'test_site_slug_a')

    def test_obj_exists_req_fields(self):
        """
        Tests that the CameraPoint object can be created successfully when the
        required fields are provided.
        """
        camera_point = CameraPoint.test_objects.create_camera_point(
            site=self.site,
            letter='B',
            cp_date='2016-07-07'
        )

        # Required fields
        self.assertEqual(camera_point.site.site_name, 'test site a')
        self.assertEqual(camera_point.letter, 'B')
        self.assertEqual(camera_point.cp_date, '2016-07-07')

        # Optional fields
        self.assertEqual(camera_point.latitude, None)
        self.assertEqual(camera_point.longitude, None)
        self.assertEqual(camera_point.map_datum, '')
        self.assertEqual(camera_point.description, '')

    def test_obj_exists_opt_fields(self):
        """
        Tests that the CameraPoint object can be created successfully when the
        required and optional fields are provided.
        """
        camera_point = CameraPoint.test_objects.create_camera_point(
            site=self.site,
            letter='C',
            cp_date='2016-07-08',
            latitude=0.45,
            longitude=0.45,
            map_datum='WGS84',
            description='Notes on this camera point for test site a'
        )

        # Required fields
        self.assertEqual(camera_point.site.site_name, 'test site a')
        self.assertEqual(camera_point.letter, 'C')
        self.assertEqual(camera_point.cp_date, '2016-07-08')
        # Optional fields
        self.assertEqual(camera_point.latitude, 0.45)
        self.assertEqual(camera_point.longitude, 0.45)
        self.assertEqual(camera_point.map_datum, 'WGS84')
        self.assertEqual(camera_point.description,
                         'Notes on this camera point for test site a')
