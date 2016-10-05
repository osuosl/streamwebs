from django.test import TestCase
from django.contrib.gis.db import models
from itertools import chain
from streamwebs.models import CameraPoint, PhotoPoint, Site


class PhotoPointTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'camera_point': models.ForeignKey,
            'number': models.PositiveSmallIntegerField,
            'pp_date': models.DateField,
            'compass_bearing': models.PositiveSmallIntegerField,
            'distance': models.DecimalField,
            'camera_height': models.DecimalField,
            'notes': models.TextField,
            'id': models.AutoField,

            'camera_point_id': models.ForeignKey,
            'photo_point': models.ManyToOneRel
        }

        self.optional_fields = {
            'notes': models.TextField
        }

        site = Site.test_objects.create_site('test site c')
        self.camera_point = CameraPoint.test_objects.create_camera_point(
            site, '2016-07-05', 'POINT(-121.393401 44.061437)')

    def test_fields_exist(self):
        """
        The model's field types and the expected field types listed in setUp
        should match exactly.
        """
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type,
                             type(PhotoPoint._meta.get_field(field)))

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
        for field in self.optional_fields:
            self.assertEqual(
                PhotoPoint._meta.get_field(field).blank, True)

    def test_PhotoPoint_ManyToOneCameraPoint(self):
        """
        A photo point should correspond to a single camera point.
        """

        photo_point = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-06', 140, 4.5, 2.3)

        self.assertEqual(photo_point.camera_point.site.site_name,
                         'test site c')
        self.assertEqual(photo_point.camera_point.letter, 'A')
        self.assertEqual(photo_point.camera_point.cp_date, '2016-07-05')
        self.assertEqual(photo_point.camera_point.location.coords,
                         (-121.393401, 44.061437))

    def test_obj_exists_req_fields(self):
        """
        A photo point should be created successfully when the required fields
        are provided.
        """
        photo_point = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-04', 270, 2.3, 0.5)

        # Required
        self.assertEqual(photo_point.camera_point.site.site_name,
                         'test site c')
        self.assertEqual(photo_point.camera_point.cp_date, '2016-07-05')
        self.assertEqual(photo_point.pp_date, '2016-07-04')
        self.assertEqual(photo_point.compass_bearing, 270)
        self.assertEqual(photo_point.distance, 2.3)
        self.assertEqual(photo_point.camera_height, 0.5)

        # Optional
        self.assertEqual(photo_point.notes, '')

    def test_obj_exists_opt_fields(self):
        """
        A photo point should be created successfully when the required and
        optional fields are provided.
        """
        photo_point = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-02', 1.62, 4.1, 5.3,
            'Notes on photo point for test site c')

        self.assertEqual(photo_point.camera_point.site.site_name,
                         'test site c')
        self.assertEqual(photo_point.camera_point.cp_date, '2016-07-05')
        self.assertEqual(photo_point.pp_date, '2016-07-02')
        self.assertEqual(photo_point.compass_bearing, 1.62)
        self.assertEqual(photo_point.distance, 4.1)
        self.assertEqual(photo_point.camera_height, 5.3)
        self.assertEqual(photo_point.notes,
                         'Notes on photo point for test site c')

    def test_number_assign_for_first_pp(self):
        photo_point = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-04', 270, 2.3, 0.5)
        self.assertEqual(photo_point.number, 1)

    def test_number_assign_for_regular_pp(self):
        photo_point = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-04', 270, 2.3, 0.5)

        self.assertEqual(photo_point.number, 1)

        photo_point_2 = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-04', 270, 2.3, 0.5)

        self.assertEqual(photo_point_2.number, 2)

        photo_point_2.number = 44
        photo_point_2.save()

        self.assertEqual(photo_point_2.number, 44)

        photo_point_3 = PhotoPoint.test_objects.create_photo_point(
            self.camera_point, '2016-07-04', 270, 2.3, 0.5)

        self.assertEqual(photo_point_3.number, 45)

    def test_restart_numbering_for_new_cp(self):
        site = Site.test_objects.create_site('test site c')
        camera_point = CameraPoint.test_objects.create_camera_point(
            site, '2016-07-05', 'POINT(-121.393401 44.061437)')
        camera_point_2 = CameraPoint.test_objects.create_camera_point(
            site, '2016-07-05', 'POINT(-121.393401 44.061437)')
        photo_point = PhotoPoint.test_objects.create_photo_point(
            camera_point, '2016-07-04', 270, 2.3, 0.5)
        photo_point_2 = PhotoPoint.test_objects.create_photo_point(
            camera_point_2, '2016-07-04', 270, 2.3, 0.5)

        self.assertEqual(camera_point.site.site_name,
                         camera_point_2.site.site_name)
        self.assertEqual(camera_point.letter, 'A')
        self.assertEqual(camera_point_2.letter, 'B')
        self.assertEqual(photo_point.number, 1)
        self.assertEqual(photo_point_2.number, 1)
