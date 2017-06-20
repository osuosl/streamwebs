from django.test import TestCase
from django.forms import inlineformset_factory
from streamwebs.forms import BaseZoneInlineFormSet, TransectZoneForm
from streamwebs.models import RiparianTransect, TransectZone, Site, School


class BaseZoneFormSetTestCase(TestCase):

    def setUp(self):
        # create the inline formset using inline formset factory
        self.ZoneFormSet = inlineformset_factory(
                RiparianTransect, TransectZone, form=TransectZoneForm,
                extra=5,
                formset=BaseZoneInlineFormSet)

        # create valid transect (+ site) for future assignation
        site = Site.test_objects.create_site('Site')
        school = School.test_objects.create_school('School')
        self.transect = RiparianTransect.test_objects.create_transect(
                school, '2015-01-01 11:56', site)

    def test_zeroed_zones_with_comments(self):
        """All zone values 0; some zones have comments. Error raised"""
        # make data dict; pass to formset
        data = {
                'transect-TOTAL_FORMS': '5',
                'transect-INITIAL_FORMS': '0',
                'transect-MAX_NUM_FORMS': '5',

                'transect-0-conifers': 0,
                'transect-0-hardwoods': 0,
                'transect-0-shrubs': 0,
                'transect-0-comments': '',

                'transect-1-conifers': 0,
                'transect-1-hardwoods': 0,
                'transect-1-shrubs': 0,
                'transect-1-comments': 'comments for zone 2',

                'transect-2-conifers': 0,
                'transect-2-hardwoods': 0,
                'transect-2-shrubs': 0,
                'transect-2-comments': '',

                'transect-3-conifers': 0,
                'transect-3-hardwoods': 0,
                'transect-3-shrubs': 0,
                'transect-3-comments': 'comments for zone 4',

                'transect-4-conifers': 0,
                'transect-4-hardwoods': 0,
                'transect-4-shrubs': 0,
                'transect-4-comments': 'comments for zone 5'
                }
        formset = self.ZoneFormSet(data, instance=self.transect)
        # assert formset is NOT valid
        self.assertFalse(formset.is_valid())
        # assert there are no regular form field errors
        self.assertEquals(formset.errors, [{}, {}, {}, {}, {}])
        # assert there are non form field errors
        self.assertEquals(
            formset.non_form_errors(),
            ['At least one zone must have at least one value greater than 0.'])

    def test_completely_blank_zones(self):
        """All zone values 0; no comments. Error raised"""
        # same as previours test but without comments
        data = {
                'transect-TOTAL_FORMS': '5',
                'transect-INITIAL_FORMS': '0',
                'transect-MAX_NUM_FORMS': '5',

                'transect-0-conifers': 0,
                'transect-0-hardwoods': 0,
                'transect-0-shrubs': 0,
                'transect-0-comments': '',

                'transect-1-conifers': 0,
                'transect-1-hardwoods': 0,
                'transect-1-shrubs': 0,
                'transect-1-comments': '',

                'transect-2-conifers': 0,
                'transect-2-hardwoods': 0,
                'transect-2-shrubs': 0,
                'transect-2-comments': '',

                'transect-3-conifers': 0,
                'transect-3-hardwoods': 0,
                'transect-3-shrubs': 0,
                'transect-3-comments': '',

                'transect-4-conifers': 0,
                'transect-4-hardwoods': 0,
                'transect-4-shrubs': 0,
                'transect-4-comments': ''
                }
        formset = self.ZoneFormSet(data, instance=self.transect)
        self.assertFalse(formset.is_valid())
        self.assertEquals(formset.errors, [{}, {}, {}, {}, {}])
        self.assertEquals(
            formset.non_form_errors(),
            ['At least one zone must have at least one value greater than 0.'])

    def test_bare_minimum(self):
        """Only one zone has value greater than 0. All zones count as valid"""
        data = {
                'transect-TOTAL_FORMS': '5',
                'transect-INITIAL_FORMS': '0',
                'transect-MAX_NUM_FORMS': '5',

                'transect-0-conifers': 0,
                'transect-0-hardwoods': 0,
                'transect-0-shrubs': 0,
                'transect-0-comments': '',

                'transect-1-conifers': 0,
                'transect-1-hardwoods': 0,
                'transect-1-shrubs': 0,
                'transect-1-comments': '',

                # third form satisfies the minimum requirement for valid zones
                'transect-2-conifers': 0,
                'transect-2-hardwoods': 1,
                'transect-2-shrubs': 0,
                'transect-2-comments': '',

                'transect-3-conifers': 0,
                'transect-3-hardwoods': 0,
                'transect-3-shrubs': 0,
                'transect-3-comments': '',

                'transect-4-conifers': 0,
                'transect-4-hardwoods': 0,
                'transect-4-shrubs': 0,
                'transect-4-comments': ''
                }
        formset = self.ZoneFormSet(data, instance=self.transect)
        self.assertTrue(formset.is_valid())
        self.assertEquals(formset.errors, [{}, {}, {}, {}, {}])
        self.assertEquals(formset.non_form_errors(), [])
