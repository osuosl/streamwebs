from __future__ import unicode_literals

import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from measurement.measures import Temperature


class SiteManager(models.Manager):
    """
    Manager for the site class - creates a site to be used in tests
    """
    def create_site(self, site_name, site_type, site_slug):
        site = self.create(site_name=site_name, site_type=site_type,
                           site_slug=site_slug)
        return site


@python_2_unicode_compatible
class Site(models.Model):
    """
    The Sites model holds the information of a site, including the geographic
    location as a pair of latitudinal/longitudinal coordinates and an optional
    text description of entry.
    """
    site_name = models.CharField(max_length=250, blank=True)
    site_type = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    site_slug = models.SlugField(blank=True)

    # Geo Django fields to store a point
    location = models.PointField(null=True, blank=True)
    objects = models.GeoManager()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = SiteManager()

    def __str__(self):
        return self.site_name

def validate_UserProfile_school(school):
    if school not in dict(settings.SCHOOL_CHOICES):
        raise ValidationError('That school is not in the list.')


def validate_UserProfile_birthdate(birthdate):
    today = datetime.datetime.now()
    if birthdate.year > today.year - 13:
        raise ValidationError(
            'You must have been born before %s' % (today.year-13)
        )
    elif birthdate.year == today.year - 13:
        if birthdate.month > today.month:
            raise ValidationError('You are not yet 13 (month)')
        elif birthdate.month == today.month:
            if birthdate.day > today.day:
                raise ValidationError('You are not yet 13 (days)')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(
        max_length=255,
        choices=settings.SCHOOL_CHOICES,
        default='',
        validators=[validate_UserProfile_school]
    )
    birthdate = models.DateField(validators=[validate_UserProfile_birthdate])

    def __unicode__(self):
        return self.user.username

class MeasurementsManager(models.Manager):
    """
    Manager for the measurement class - creates measurement info to be used in
    the datasheet tests for both the required and additional fields
    """
    def create_measurement_info(self, datasheet_type, measuring, sample_number,
                                tool):
        info = self.create(datasheet_type=datasheet_type,
                           measuring=measuring,
                           sample_number=sample_number,
                           tool=tool)
        return info

    def create_additional_info(self, datasheet_type, measuring, sample_number):
        add_info = self.create(datasheet_type=datasheet_type,
                               measuring=measuring,
                               sample_number=sample_number)
        return add_info


@python_2_unicode_compatible
class Measurements(models.Model):
    WQ = 'Water Quality'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    NOT_ACCESSED = 'N/A'
    VERNIER = 'Vernier'
    MANUAL = 'Manual'

    # Required fields
    WATER_TEMP = 'Water Temperature'
    AIR_TEMP = 'Air Temperature'
    DISSOLVED_O2 = 'Dissolved Oxygen'
    PH = 'pH'
    TURBIDITY = 'Turbidity'
    SALINITY = 'Salinity'

    # Additional paramters
    CONDUCT = 'Conductivity'
    TOT_SOL = 'Total Solids'
    BOD = 'Bod'
    AMMONIA = 'Ammonia'
    NITRITE = 'Nitrite'
    NITRATE = 'Nitrate'
    PHOSPHATES = 'Phosphates'
    FECAL_COL = 'Fecal Coliform'

    DATASHEET_OPTIONS = ((None, '-----'), (WQ, 'Water Quality'),)
    MEASURING = ((None, '-----'),
                 (WATER_TEMP, 'Water Temperature'),
                 (AIR_TEMP, 'Air Temperature'),
                 (DISSOLVED_O2, 'Dissolved Oxygen'),
                 (PH, 'pH'),
                 (TURBIDITY, 'Turbidity'),
                 (SALINITY, 'Salinity'),
                 (CONDUCT, 'Conductivity'),
                 (TOT_SOL, 'Total Solids'),
                 (BOD, 'Bod'),
                 (AMMONIA, 'Ammonia'),
                 (NITRITE, 'Nitrite'),
                 (NITRATE, 'Nitrate'),
                 (PHOSPHATES, 'Phosphates'),
                 (FECAL_COL, 'Fecal Coliform'),)
    SAMPLE_NUMBER = ((ONE, '1'), (TWO, '2'), (THREE, '3'), (FOUR, '4'),)
    TOOL_CHOICES = ((NOT_ACCESSED, 'N/A'),
                    (MANUAL, 'Manual'),
                    (VERNIER, 'Vernier'),)

    """Contains miscellaneous measurement information for the various
       datasheets such as units, sample number, etc"""
    datasheet_type = models.CharField(max_length=255,
                                      choices=DATASHEET_OPTIONS,
                                      default=DATASHEET_OPTIONS[0])
    measuring = models.CharField(max_length=255, choices=MEASURING,
                                 default=None)
    sample_number = models.CharField(max_length=255, choices=SAMPLE_NUMBER,
                                     default=ONE,)
    tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                            default=TOOL_CHOICES[0])

    objects = MeasurementsManager()

    def __str__(self):
        return self.measuring

    class Meta:
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'


@python_2_unicode_compatible
class Water_Quality(models.Model):
    LEVEL_A = 'A'   # Define DEQ water quality levels
    LEVEL_B = 'B'
    LEVEL_C = 'C'
    LEVEL_D = 'D'
    LEVEL_E = 'E'
#    NOT_ACCESSED = 'N/A'
    FAHRENHEIT = 'Fahrenheit'
    CELSIUS = 'Celsius'

    DEQ_WQ_CHOICES = (
        (None, '-----'),
        (LEVEL_A, 'Level A'),
        (LEVEL_B, 'Level B'),
        (LEVEL_C, 'Level C'),
        (LEVEL_D, 'Level D'),
        (LEVEL_E, 'Level E'),
    )

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'), (None, '-----'),)
    UNIT_CHOICES = ((None, '-----'),
                    (FAHRENHEIT, 'Fahrenheit'),
                    (CELSIUS, 'Celsius'),)

    """
    The Water Quality model corresponds to the Water Quality datasheet. Each
    object has a one-to-one relationship with its specified Site.
    """
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    DEQ_wq_level = models.CharField(max_length=1, choices=DEQ_WQ_CHOICES,
                                    default=None)
    date = models.DateField(default=datetime.date.today)
    school = models.CharField(max_length=250)
    latitude = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    longitude = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    fish_present = models.BooleanField(choices=BOOL_CHOICES, default=None)
    live_fish = models.PositiveSmallIntegerField(default=0)
    dead_fish = models.PositiveSmallIntegerField(default=0)
    air_temp_unit = models.CharField(max_length=255, choices=UNIT_CHOICES,
                                     default=UNIT_CHOICES[0])
    water_temp_unit = models.CharField(max_length=255, choices=UNIT_CHOICES,
                                       default=UNIT_CHOICES[0])
    water_temp = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    water_temp_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                        related_name='water_temp_info',
                                        null=True)
    air_temp = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    air_temp_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                      related_name='air_temp_info', null=True)
    dissolved_oxygen = models.DecimalField(default=0, max_digits=5,
                                           decimal_places=2)
    oxygen_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                    related_name='oxygen_info', null=True)
    pH = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    pH_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                related_name='pH_info', null=True)
    turbidity = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    turbid_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                    related_name='turbid_info', null=True)
    salinity = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    salt_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                  related_name='salt_info', null=True)

    # The following are optional fields
    conductivity = models.DecimalField(default=0, max_digits=5,
                                       decimal_places=2, blank=True)
    conductivity_info = models.ForeignKey(Measurements,
                                          on_delete=models.CASCADE,
                                          related_name='conductivity_info',
                                          null=True, blank=True)
    total_solids = models.DecimalField(default=0, max_digits=5,
                                       decimal_places=2, blank=True)
    tot_solids_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                        related_name='tot_solids_info',
                                        null=True, blank=True)
    bod = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                              blank=True)
    bod_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                 related_name='bod_info', null=True,
                                 blank=True)
    ammonia = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                  blank=True)
    ammonia_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                     related_name='ammonia_info', null=True,
                                     blank=True)
    nitrite = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                  blank=True)
    nitrite_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                     related_name='nitrite_info', null=True,
                                     blank=True)
    nitrate = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                  blank=True)
    nitrate_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                     related_name='nitrate_info', null=True,
                                     blank=True)
    phosphates = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                     blank=True)
    phosphate_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                       related_name='phosphate_info',
                                       null=True, blank=True)
    fecal_coliform = models.DecimalField(default=0, max_digits=5,
                                         decimal_places=2, blank=True)
    fecal_info = models.ForeignKey(Measurements, on_delete=models.CASCADE,
                                   related_name='fecal_info', null=True,
                                   blank=True)
    notes = models.TextField(blank=True)

    # Add some logic in which the datasheet object is only created when
    # the Site in which it corresponds to actually exists

    def __str__(self):
        return self.site.site_name

    class Meta:
        verbose_name = 'Water Quality'
        verbose_name_plural = 'Water Quality'
