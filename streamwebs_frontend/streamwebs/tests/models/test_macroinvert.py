from django.test import TestCase

from streamwebs.models import Macroinvertebrates
from django.contrib.gis.db import models
from django.apps import apps
from intertools import chain


class SiteTestCase(TestCase):

  def setUp(self):
      self.expected_fields = {
          'date/time': models.DatetTimeField,
          'site_name': models.ForeignKey,
          'water_type': models.CharField,
          'num_people': models.PositiveIntegerField,
          'time_spent': models.PositiveIntegerField,  # in minutes
          # 'weather': models.CharField ??

          # Sensitive/intolerant to pollution
          'caddisfly': models.PositiveIntegerField,
          'mayfly': models.PositiveIntegerField,
          'riffle_beetle': models.PositiveIntegerField,
          'stonefly': models.PositiveIntegerField,
          'water_penny': models.PositiveIntegerField,
          'dobsonfly': models.PositiveIntegerField,
          'sensitive_total': models.PositiveIntegerField,

          # Somewhat sensitive
          'clam/mussel': models.PositiveIntegerField,
          'crane_fly': models.PositiveIntegerField,
          'crayfish': models.PositiveIntegerField,
          'damselfly': models.PositiveIntegerField,
          'dragonfly': models.PositiveIntegerField,
          'scud': models.PositiveIntegerField,
          'fishfly': models.PositiveIntegerField,
          'somewhat_sensitive_total': models.PositiveIntegerField,

          # Tolerant
          'aquatic_worm': models.PositiveIntegerField,
          'blackfly': models.PositiveIntegerField,
          'leech': models.PositiveIntegerField,
          'midge': models.PositiveIntegerField,
          'snail': models.PositiveIntegerField,
          'mosquito_larva': models.PositiveIntegerField,
          'tolerant_total': models.PositiveIntegerField,
      }

  def test_fields_exist(self):
      model = apps.get_model('streamwebs', 'macroinvertebrates')
      for field, field_type in self.expected_fields.items():
          self.assertEqual(
              field_type, type(model._meta.get_field(field)))
