from django.test import TestCase
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from itertools import chain
from streamwebs.models import (Site, CameraPoint, PhotoPoint, PhotoPointImage)
import tempfile


class PhotoPointImageTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'photo_point': models.ForeignKey,
            'image': models.ImageField,
            'date': models.DateField,
            'id': models.AutoField,

            'photo_point_id': models.ForeignKey
        }

        site = Site.test_objects.create_site('Test site')
        camera_point = CameraPoint.test_objects.create_camera_point(
            site, '2016-07-29', 'POINT(-121.393401 44.061437)')
        self.photo_point = PhotoPoint.test_objects.create_photo_point(
            camera_point, '2016-07-30', 45, 4, 5)
        self.temp_photo = tempfile.NamedTemporaryFile(suffix='.jpg').name
        self.pp_image = PhotoPointImage.objects.create(
            photo_point=self.photo_point,
            date='2016-08-30',
            image=self.temp_photo)

    def test_fields_exist(self):
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type,
                             type(PhotoPointImage._meta.get_field(field)))

    def test_no_extra_fields(self):
        # MyModel._meta.get_all_field_names() is deprecated. The following is
        # an alternative, as suggested by the Django docs:
        # https://docs.djangoproject.com/en/1.9/ref/models/meta/
        pp_fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in PhotoPointImage._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
            )))
        self.assertEqual(sorted(pp_fields),
                         sorted(self.expected_fields.keys()))

    def test_obj_exists(self):
        self.assertEqual(self.pp_image.image, self.temp_photo)
        self.assertEqual(self.pp_image.date, '2016-08-30')

    def test_PhotoPointImage_ManyToOnePhotoPoint(self):
        """A photo point image should correspond to a single photo point."""
        self.assertEqual(self.pp_image.photo_point.number, 1)
        self.assertEqual(self.pp_image.photo_point.pp_date, '2016-07-30')
        self.assertEqual(
            self.pp_image.photo_point.camera_point.cp_date, '2016-07-29')
        self.assertEqual(
            self.pp_image.photo_point.camera_point.site.site_name, 'Test site')

    def test_create_pp_img_with_existing_date(self):
        new_pp_img = PhotoPointImage.objects.create(
            photo_point=self.photo_point,
            date='2016-08-30',
            image=self.temp_photo)

        with self.assertRaises(ValidationError):
            new_pp_img.clean()

    def test_create_pp_img_with_new_date(self):
        new_pp_img = PhotoPointImage.objects.create(
            photo_point=self.photo_point,
            date='2016-08-31',
            image=self.temp_photo)

        try:
            new_pp_img.clean()
        except:
            self.fail('An exception was raised.')
