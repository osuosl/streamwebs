from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import CC_Cardinal


class CCCardinalTestCase(TestCase):
