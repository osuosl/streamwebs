from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from django.utils import timezone

from streamwebs.models import Site
from streamwebs.models import Macroinvertebrates
from django.core.exceptions import ValidationError


class MacroTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'school': models.CharField,
            'date_time': models.DateTimeField,
            'weather': models.CharField,
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'time_spent': models.PositiveIntegerField,  # in minutes
            'num_people': models.PositiveIntegerField,
            'riffle': models.BooleanField,
            'pool': models.BooleanField,
            'id': models.AutoField,

            # Sensitive/intolerant to pollution
            'caddisfly': models.PositiveIntegerField,
            'mayfly': models.PositiveIntegerField,
            'riffle_beetle': models.PositiveIntegerField,
            'stonefly': models.PositiveIntegerField,
            'water_penny': models.PositiveIntegerField,
            'dobsonfly': models.PositiveIntegerField,
            'sensitive_total': models.PositiveIntegerField,

            # Somewhat sensitive
            'clam_or_mussel': models.PositiveIntegerField,
            'crane_fly': models.PositiveIntegerField,
            'crayfish': models.PositiveIntegerField,
            'damselfly': models.PositiveIntegerField,
            'dragonfly': models.PositiveIntegerField,
            'scud': models.PositiveIntegerField,
            'fishfly': models.PositiveIntegerField,
            'alderfly': models.PositiveIntegerField,
            'mite': models.PositiveIntegerField,
            'somewhat_sensitive_total': models.PositiveIntegerField,

            # Tolerant
            'aquatic_worm': models.PositiveIntegerField,
            'blackfly': models.PositiveIntegerField,
            'leech': models.PositiveIntegerField,
            'midge': models.PositiveIntegerField,
            'snail': models.PositiveIntegerField,
            'mosquito_larva': models.PositiveIntegerField,
            'tolerant_total': models.PositiveIntegerField,

            # Water quality rating
            'wq_rating': models.PositiveIntegerField
        }

    def test_fields_exist(self):
        """Tests that the listed fields are created"""
        model = apps.get_model('streamwebs', 'macroinvertebrates')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        """Tests that no extra fields are created"""
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Macroinvertebrates._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_datasheet_ManyToOne(self):
        """Tests that a datasheet correctly corresponds to a specified site"""
        default_dt = timezone.now()  # default date_time value

        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=7,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=14,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=5,
                                                   wq_rating=26)

        self.assertEqual(macros.site.site_name, 'test')
        self.assertEqual(macros.site.site_type, 'some_type')
        self.assertEqual(macros.site.site_slug, 'some_slug')

    def test_datasheet_SetMacroInfo(self):
        """Tests that macroinvertebrate data is created"""
        default_dt = timezone.now()

        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=14,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=5,
                                                   wq_rating=26)

        # General datasheet info
        self.assertEqual(macros.date_time, default_dt)
        self.assertEqual(macros.weather, 'sunny')
        self.assertEqual(macros.time_spent, 45)
        self.assertEqual(macros.num_people, 17)
        self.assertEqual(macros.riffle, False)
        self.assertEqual(macros.pool, True)

        # Checks the values for sensitive/intolerant macroinvertebrates
        self.assertEqual(macros.caddisfly, 0)
        self.assertEqual(macros.mayfly, 2)
        self.assertEqual(macros.riffle_beetle, 1)
        self.assertEqual(macros.stonefly, 1)
        self.assertEqual(macros.water_penny, 3)
        self.assertEqual(macros.dobsonfly, 0)
        self.assertEqual(macros.sensitive_total, 21)

        # Somewhat tolerant
        self.assertEqual(macros.clam_or_mussel, 4)
        self.assertEqual(macros.crane_fly, 5)
        self.assertEqual(macros.crayfish, 2)
        self.assertEqual(macros.damselfly, 6)
        self.assertEqual(macros.dragonfly, 4)
        self.assertEqual(macros.scud, 5)
        self.assertEqual(macros.fishfly, 7)
        self.assertEqual(macros.alderfly, 8)
        self.assertEqual(macros.mite, 8)
        self.assertEqual(macros.somewhat_sensitive_total, 14)

        # Tolerant
        self.assertEqual(macros.aquatic_worm, 12)
        self.assertEqual(macros.blackfly, 9)
        self.assertEqual(macros.leech, 8)
        self.assertEqual(macros.midge, 7)
        self.assertEqual(macros.snail, 5)
        self.assertEqual(macros.mosquito_larva, 11)
        self.assertEqual(macros.tolerant_total, 5)

        # Overall water quality rating
        self.assertEqual(macros.wq_rating, 26)

    """Tests for validating intolerant macroinvertebrates"""
    def test_validate_macroinverts_intolerant(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=7,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=171)

        with self.assertRaises(ValidationError):
            macros.clean()

    def test_validate_macroinverts_intolerant_no_error(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=171)
        raised = False
        try:
            macros.clean()
        except:
            raised = True
        self.assertFalse(raised, 'ValidationError raised')

    """Tests for validating somewhat sensitive macroinvertebrates"""
    def test_validate_macroinverts_somewhat_sensitive(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=14,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=171)

        with self.assertRaises(ValidationError):
            macros.clean()

    def test_validate_macroinverts_somewhat_sensitive_no_error(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=171)
        raised = False
        try:
            macros.clean()
        except:
            raised = True
        self.assertFalse(raised, 'ValidationError raised')

    """Tests for validating tolerant macroinvertebrates"""
    def test_validate_macroinverts_tolerant(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=5,
                                                   wq_rating=171)

        with self.assertRaises(ValidationError):
            macros.clean()

    def test_validate_macroinverts_tolerant_no_error(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=171)
        raised = False
        try:
            macros.clean()
        except:
            raised = True
        self.assertFalse(raised, 'ValidationError raised')

    """Tests for validating water quality rating"""
    def test_validate_wq_rating(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=26)

        with self.assertRaises(ValidationError):
            macros.clean()

    def test_validate_wq_rating_no_error(self):
        default_dt = timezone.now()
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        macros = Macroinvertebrates.objects.create(site=site,
                                                   date_time=default_dt,
                                                   weather='sunny',
                                                   time_spent=45,
                                                   num_people=17,
                                                   riffle=False,
                                                   pool=True,
                                                   caddisfly=0,
                                                   mayfly=2, riffle_beetle=1,
                                                   stonefly=1, water_penny=3,
                                                   dobsonfly=0,
                                                   sensitive_total=21,
                                                   clam_or_mussel=4,
                                                   crane_fly=5, crayfish=2,
                                                   damselfly=6, dragonfly=4,
                                                   scud=5, fishfly=7,
                                                   alderfly=8, mite=8,
                                                   somewhat_sensitive_total=98,
                                                   aquatic_worm=12,
                                                   blackfly=9, leech=8,
                                                   midge=7, snail=5,
                                                   mosquito_larva=11,
                                                   tolerant_total=52,
                                                   wq_rating=171)
        raised = False
        try:
            macros.clean()
        except:
            raised = True
        self.assertFalse(raised, 'ValidationError raised')
