from django.test import TestCase

# Create your tests here.
class IndexViewTest(TestCase):
    def test_index(self):
        response = self.client.get('/streamwebs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/index.html')
