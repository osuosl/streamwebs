from django.test import TestCase
from streamwebs.forms import MacroinvertebratesForm


class MacroinvertebrateFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('date_time', 'weather', 'time_spent',
                                'num_people', 'water_type', 'caddisfly',
                                'mayfly', 'riffle_beetle', 'stonefly',
                                'water_penny', 'dobsonfly', 'clam_or_mussel',
                                'crane_fly', 'crayfish', 'damselfly',
                                'dragonfly', 'scud', 'fishfly', 'alderfly',
                                'mite', 'aquatic_worm', 'blackfly', 'leech',
                                'midge', 'snail', 'mosquito_larva', 'notes')

    def test_MacroinvertebrateForm_fields_exist(self):
        macro_form = MacroinvertebratesForm()
        self.assertEqual(set(macro_form.Meta.fields),
                         set(self.expected_fields))
