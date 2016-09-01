from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, Canopy_Cover, CC_Cardinal


class ViewCanopyCoverTestCase(TestCase):

    def test_data_sheet_view(self):
        site = Site.test_objects.create_site('Site', 'Type')

