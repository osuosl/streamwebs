from django.test import TestCase
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from streamwebs.models import CameraPoint, PhotoPoint, Site
import tempfile, datetime

class CameraPointTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'cp_date': models.DateField,
            'created_by': models.CharField, #necessary? or link to User? 
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'map_datum': models.CharField,
            'description': models.TextField,
            'photo_pt_1': models.ForeignKey,
            'photo_pt_2': models.ForeignKey,
            'photo_pt_3': models.ForeignKey,
            'id': models.AutoField,

            # Corresponding photo point entry (id)
            'photo_pt_1_id': models.ForeignKey,
            'photo_pt_2_id': models.ForeignKey,
            'photo_pt_3_id': models.ForeignKey
        }

        self.optional_fields = {
            'taken_by': models.CharField, #necessary? or link to User? 
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'map_datum': models.CharField,
            'description': models.TextField
        }
            
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
        model = apps.get_model('streamwebs', 'camerapoint')
        for field in self.optional_fields:
            self.assertEqual(
                CameraPoint._meta.get_field(field).blank, True)

    def test_CameraPoint_ManyToOneSite(self):
        """
        A camera point should correspond to a single specified site.
        """
        site = Site.objects.create_site('test site', 'test site type',
                                        'test_site_slug')
        #make the samples (3)
        # make the camerapoint/monitoring datasheet
        # assert that the site  data matches the newly created test site 
        cp_date = datetime.date.today()
        photo1 = tempfile.NamedTemporaryFile(suffix='.jpg').name
        photo2 = tempfile.NamedTemporaryFile(suffix='.jpg').name
        photo3 = tempfile.NamedTemporaryFile(suffix='.jpg').name
  
        photo_pt_1 = PhotoPoint.photo_points.create_photo_point(cp_date, 5.3, 7, 3, 4, 1, 'TempPhoto.jpg', photo1, 'Photo point 1 notes')
        photo_pt_2 = PhotoPoint.photo_points.create_photo_point(cp_date, 5.2, 6, 2, 5, 2, 'TempPhoto.jpg', photo2, 'Photo point 2 notes')
        photo_pt_3 = PhotoPoint.photo_points.create_photo_point(cp_date, 5.4, 8, 9, 2, 3, 'TempPhoto.jpg', photo3, 'Photo point 3 notes')

        camera_point = CameraPoint.objects.create(site=site, cp_date=cp_date,
            created_by='Ms. Frizzle', latitude=45.0, longitude=45.0,
            map_datum='WGS 84', description='camera_point description',
            photo_pt_1=photo_pt_1, photo_pt_2=photo_pt_2,
            photo_pt_3=photo_pt_3)

        self.assertEqual(camera_point.site.site_name, 'test site')
        self.assertEqual(camera_point.site.site_type, 'test site type')
        self.assertEqual(camera_point.site.site_slug, 'test_site_slug')
