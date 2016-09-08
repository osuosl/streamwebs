from django.test import TestCase
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
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
            'location': models.PointField,
            'map_datum': models.CharField,
            'description': models.TextField,
            'created': models.DateTimeField,
            'id': models.AutoField,

            'camera_point': models.ManyToOneRel
        }

        self.optional_fields = {
            'map_datum': models.CharField,
            'description': models.TextField
        }

        self.site = Site.test_objects.create_site('test site a')

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
            self.site, cp_date, 'POINT(-121.393401 44.061437)'
        )

        self.assertEqual(camera_point.site.site_name, 'test site a')

    def test_obj_exists_req_fields(self):
        """
        Tests that the CameraPoint object can be created successfully when the
        required fields are provided.
        """
        camera_point = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-07', 'POINT(-121.393401 44.061437)'
        )

        # Required fields
        self.assertEqual(camera_point.site.site_name, 'test site a')
        self.assertEqual(camera_point.cp_date, '2016-07-07')

        # Optional fields
        self.assertEqual(camera_point.location.coords,
                         (-121.393401, 44.061437))
        self.assertEqual(camera_point.map_datum, '')
        self.assertEqual(camera_point.description, '')

    def test_obj_exists_opt_fields(self):
        """
        Tests that the CameraPoint object can be created successfully when the
        required and optional fields are provided.
        """
        camera_point = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-08', Point(-120.2684184, 44.3910532), 'WGS84',
            'Notes on this camera point for test site a'
        )

        # Required fields
        self.assertEqual(camera_point.site.site_name, 'test site a')
        self.assertEqual(camera_point.cp_date, '2016-07-08')

        # Optional fields
        self.assertEqual(camera_point.location.coords,
                         (-120.2684184, 44.3910532))
        self.assertEqual(camera_point.map_datum, 'WGS84')
        self.assertEqual(camera_point.description,
                         'Notes on this camera point for test site a')

    def test_letter_assign_for_first_cp(self):
        camera_point = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-08', Point(-120.2684184, 44.3910532),
        )
        self.assertEqual(camera_point.letter, 'A')

    def test_letter_assign_for_regular_cp(self):
        camera_point = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-08', Point(-120.2684184, 44.3910532),
        )
        self.assertEqual(camera_point.letter, 'A')

        camera_point_2 = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-08', Point(-120.2684184, 44.3910532),
        )
        self.assertEqual(camera_point_2.letter, 'B')

    def test_letter_assign_for_end_of_alphabet(self):
        camera_point = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-08', Point(-120.2684184, 44.3910532),
        )
        camera_point.letter = 'ZZ'
        camera_point.save()

        self.assertEqual(camera_point.letter, 'ZZ')

        camera_point_2 = CameraPoint.test_objects.create_camera_point(
            self.site, '2016-07-08', Point(-120.2684184, 44.3910532)
        )
        self.assertEqual(camera_point_2.letter, 'AAA')
