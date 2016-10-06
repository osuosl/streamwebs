from django.test import TestCase
from streamwebs.forms import MacroinvertebratesForm


class MacroinvertibrateFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('school', 'date_time', 'weather', 'time_spent',
                                'num_people', 'riffle', 'pool', 'caddisfly',
                                'mayfly', 'riffle_beetle', 'stonefly',
                                'water_penny', 'dobsonfly', 'clam_or_mussel',
                                'crane_fly', 'crayfish', 'damselfly',
                                'dragonfly', 'scud', 'fishfly', 'alderfly',
                                'mite', 'aquatic_worm', 'blackfly', 'leech',
                                'midge', 'snail', 'mosquito_larva')

    def test_MacroinvertibrateForm_fields_exist(self):
        macro_form = MacroinvertebratesForm()
        self.assertEqual(set(macro_form.Meta.fields),
                         set(self.expected_fields))
