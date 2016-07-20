from django.test import TestCase
from streamwebs.forms import MacroinvertibrateForm


class MacroinvertibrateFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('school', 'date_time', 'weather', 'site',
                                'time_spent', 'num_people', 'riffle', 'pool',
                                'caddisfly', 'mayfly', 'riffle_beetle',
                                'stonefly', 'water_penny', 'dobsonfly',
                                'sensitive_total', 'clam_or_mussel',
                                'crane_fly', 'crayfish', 'damselfly',
                                'dragonfly', 'scud', 'fishfly', 'alderfly',
                                'mite', 'somewhat_sensitive_total',
                                'aquatic_worm', 'blackfly', 'leech', 'midge',
                                'snail', 'mosquito_larva', 'tolerant_total',
                                'wq_rating')

    def test_MacroinvertibrateForm_fields_exist(self):
        macro_form = MacroinvertibrateForm()
        self.assertEqual(set(macro_form.Meta.fields),
                         set(self.expected_fields))
