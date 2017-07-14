from django.test import TestCase
from django.contrib.auth.models import User
from streamwebs.forms import AdminPromotionForm


class AdminPromotionFormTestCase(TestCase):
    fixtures = ['sample_users.json']

    def setUp(self):
        self.expected_fields = (
            'users_display',
            'users',
            'perms'
        )
        self.promo_form = AdminPromotionForm()

    def test_form_fields_exist(self):
        self.assertEqual(set(self.promo_form.fields),
                         set(self.expected_fields))

    def test_required_fields(self):
        """All fields should be required"""
        for field in self.expected_fields:
            self.assertEqual(self.promo_form.base_fields[field].required,
                             True)

    def test_form_isValid_with_mult_users(self):
        user1 = User.objects.get(pk=1)
        data = {
            'users_display': user1.username,
            'users': user1.id,
            'perms': 'add_admin',
        }
        self.promo_form = AdminPromotionForm(data)
        self.assertTrue(self.promo_form.is_valid())
