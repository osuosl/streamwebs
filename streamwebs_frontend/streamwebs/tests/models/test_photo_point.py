from django.test import TestCase
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from streamwebs.models import CameraPoint, PhotoPoint, Site
import tempfile


class PhotoPointTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'camera_point': models.ForeignKey,
            'pp_date': models.DateField,
            'compass_bearing': models.DecimalField,
            'distance_feet': models.PositiveSmallIntegerField,
            'distance_inches': models.PositiveSmallIntegerField,
            'camera_height_feet': models.PositiveSmallIntegerField,
            'camera_height_inches': models.PositiveSmallIntegerField,
            'photo_filename': models.CharField,
            'photo': models.ImageField,
            'notes': models.TextField,
            'id': models.AutoField,

            'camera_point_id': models.ForeignKey
        }

        self.optional_fields = {
            'distance_feet': models.PositiveSmallIntegerField,
            'distance_inches': models.PositiveSmallIntegerField,
            'camera_height_feet': models.PositiveSmallIntegerField,
            'camera_height_inches': models.PositiveSmallIntegerField,
            'photo_filename': models.CharField,
            'photo': models.ImageField,
            'notes': models.TextField
        }

    def test_fields_exist(self):
        """
        The model's field types and the expected field types listed in setUp
        should match exactly.
        """
        pp_model = apps.get_model('streamwebs', 'photopoint')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type, type(pp_model._meta.get_field(field)))

    def test_no_extra_fields(self):
        """
        The model's field names and the expected field names listed in setUp
        should match exactly.
        """
        # MyModel._meta.get_all_field_names() is deprecated. The following is
        # an alternative, as suggested by the Django docs:
        # https://docs.djangoproject.com/en/1.9/ref/models/meta/
        pp_fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in PhotoPoint._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
            )))
        self.assertEqual(sorted(pp_fields),
                         sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        """
        The model's optional fields should match the ones listed in setUp.
        """
        apps.get_model('streamwebs', 'photopoint')
        for field in self.optional_fields:
            self.assertEqual(
                PhotoPoint._meta.get_field(field).blank, True)

    def test_PhotoPoint_ManyToOneCameraPoint(self):
        """
        A photo point should correspond to a single camera point.
        """
        site = Site.objects.create_site('test site c', 'test site type c',
                                        'test_site_slug_c')
        camera_point = CameraPoint.camera_points.create_camera_point(
            site=site,
            cp_date='2016-07-05'
        )

        photo_point = PhotoPoint.photo_points.create_photo_point(
            camera_point=camera_point,
            pp_date='2016-07-06',
            compass_bearing=12.6
        )

        self.assertEqual(photo_point.camera_point.site.site_name,
                         'test site c')
        self.assertEqual(photo_point.camera_point.cp_date, '2016-07-05')

    def test_obj_exists_req_fields(self):
        """
        A photo point should be created successfully when the required fields
        are provided.
        """
        site = Site.objects.create_site('test site d', 'test site type d',
                                        'test_site_slug_d')
        camera_point = CameraPoint.camera_points.create_camera_point(
            site=site,
            cp_date='2016-07-03'
        )

        photo_point = PhotoPoint.photo_points.create_photo_point(
            camera_point=camera_point,
            pp_date='2016-07-04',
            compass_bearing=6.12
        )

        # Required
        self.assertEqual(photo_point.camera_point.site.site_name,
                         'test site d')
        self.assertEqual(photo_point.camera_point.cp_date, '2016-07-03')
        self.assertEqual(photo_point.pp_date, '2016-07-04')
        self.assertEqual(photo_point.compass_bearing, 6.12)

        # Optional
        self.assertEqual(photo_point.distance_feet, None)
        self.assertEqual(photo_point.distance_inches, None)
        self.assertEqual(photo_point.camera_height_feet, None)
        self.assertEqual(photo_point.camera_height_inches, None)
        self.assertEqual(photo_point.photo_filename, '')
        self.assertEqual(photo_point.photo, None)
        self.assertEqual(photo_point.notes, '')

    def test_obj_exists_opt_fields(self):
        """
        A photo point should be created successfully when the required and
        optional fields are provided.
        """
        site = Site.objects.create_site('test site e', 'test site type e',
                                        'test_site_slug_e')
        camera_point = CameraPoint.camera_points.create_camera_point(
            site=site,
            cp_date='2016-07-01'
        )

        temp_photo = tempfile.NamedTemporaryFile(suffix='.jpg').name

        photo_point = PhotoPoint.photo_points.create_photo_point(
            camera_point=camera_point,
            pp_date='2016-07-02',
            compass_bearing=1.62,
            distance_feet=4,
            distance_inches=5,
            camera_height_feet=5,
            camera_height_inches=4,
            photo_filename='fake.jpg',
            photo=temp_photo,
            notes='Notes on photo point for test site e'
        )

        self.assertEqual(photo_point.camera_point.site.site_name,
                         'test site e')
        self.assertEqual(photo_point.camera_point.cp_date, '2016-07-01')
        self.assertEqual(photo_point.pp_date, '2016-07-02')
        self.assertEqual(photo_point.compass_bearing, 1.62)
        self.assertEqual(photo_point.distance_feet, 4)
        self.assertEqual(photo_point.distance_inches, 5)
        self.assertEqual(photo_point.camera_height_feet, 5)
        self.assertEqual(photo_point.camera_height_inches, 4)
        self.assertEqual(photo_point.photo_filename, 'fake.jpg')
        self.assertEqual(photo_point.photo, temp_photo)
        self.assertEqual(photo_point.notes,
                         'Notes on photo point for test site e')
