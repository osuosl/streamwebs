from __future__ import unicode_literals

from django.utils import timezone
import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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
        raise ValidationError('You must be at least 13')
    elif birthdate.year == today.year - 13:
        if birthdate.month > today.month:
            raise ValidationError('You must be at least 13')
        elif birthdate.month == today.month:
            if birthdate.day > today.day:
                raise ValidationError('You must be at least 13')


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


class WQSampleManager(models.Manager):
    """
    Manager for the water quality samples - creates both the required and
    additional field data for the Water Quality datasheet tests
    """
    def create_sample(self, water_temp, wt_tool, air_temp, at_tool, oxygen,
                      oxygen_tool, pH, pH_tool, turbidity, turbid_tool,
                      salinity, salt_tool, conductivity=None, tot_sol=None,
                      bod=None, ammonia=None, nitrite=None, nitrate=None,
                      phosphates=None, fecal_col=None):

        info = self.create(water_temperature=water_temp,
                           water_temp_tool=wt_tool,
                           air_temperature=air_temp, air_temp_tool=at_tool,
                           dissolved_oxygen=oxygen, oxygen_tool=oxygen_tool,
                           pH=pH, pH_tool=pH_tool,
                           turbidity=turbidity, turbid_tool=turbid_tool,
                           salinity=salinity, salt_tool=salt_tool,
                           conductivity=conductivity,
                           total_solids=tot_sol,
                           bod=bod,
                           ammonia=ammonia,
                           nitrite=nitrite,
                           nitrate=nitrate,
                           phosphates=phosphates,
                           fecal_coliform=fecal_col)
        return info


@python_2_unicode_compatible
class WQ_Sample(models.Model):
    NOT_ACCESSED = 'N/A'
    VERNIER = 'Vernier'
    MANUAL = 'Manual'
    TOOL_CHOICES = ((NOT_ACCESSED, 'N/A'),
                    (MANUAL, 'Manual'),
                    (VERNIER, 'Vernier'),)

    # These are required fields
    water_temperature = models.DecimalField(default=0, max_digits=5,
                                            decimal_places=2)
    water_temp_tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                                       default=TOOL_CHOICES[0])
    air_temperature = models.DecimalField(default=0, max_digits=5,
                                          decimal_places=2)
    air_temp_tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                                     default=TOOL_CHOICES[0])
    dissolved_oxygen = models.DecimalField(default=0, max_digits=5,
                                           decimal_places=2)
    oxygen_tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                                   default=TOOL_CHOICES[0])
    pH = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    pH_tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                               default=TOOL_CHOICES[0])
    turbidity = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    turbid_tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                                   default=TOOL_CHOICES[0])
    salinity = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    salt_tool = models.CharField(max_length=255, choices=TOOL_CHOICES,
                                 default=TOOL_CHOICES[0])

    # The following are optional fields
    conductivity = models.DecimalField(default=0, max_digits=5,
                                       decimal_places=2, blank=True, null=True)
    total_solids = models.DecimalField(default=0, max_digits=5,
                                       decimal_places=2, blank=True, null=True)
    bod = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                              blank=True, null=True)
    ammonia = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                  blank=True, null=True)
    nitrite = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                  blank=True, null=True)
    nitrate = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                  blank=True, null=True)
    phosphates = models.DecimalField(default=0, max_digits=5, decimal_places=2,
                                     blank=True, null=True)
    fecal_coliform = models.DecimalField(default=0, max_digits=5,
                                         decimal_places=2, blank=True,
                                         null=True)

    objects = WQSampleManager()

    def __str__(self):
        return self.site.site_name

    class Meta:
        verbose_name = 'Water Quality Sample'
        verbose_name_plural = 'Water Quality Samples'


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
    sample_1 = models.ForeignKey(WQ_Sample, on_delete=models.CASCADE,
                                 related_name='sample_1', null=True)
    sample_2 = models.ForeignKey(WQ_Sample, on_delete=models.CASCADE,
                                 related_name='sample_2', null=True)
    sample_3 = models.ForeignKey(WQ_Sample, on_delete=models.CASCADE,
                                 related_name='sample_3', null=True)
    sample_4 = models.ForeignKey(WQ_Sample, on_delete=models.CASCADE,
                                 related_name='sample_4', null=True)
    notes = models.TextField(blank=True)

    # Add some logic in which the datasheet object is only created when
    # the Site in which it corresponds to actually exists

    def __str__(self):
        return self.site.site_name

    class Meta:
        verbose_name = 'Water Quality'
        verbose_name_plural = 'Water Quality'


@python_2_unicode_compatible
class Macroinvertebrates(models.Model):
    school = models.CharField(max_length=250)
    date_time = models.DateTimeField(default=timezone.now)
    weather = models.CharField(max_length=250)
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    time_spent = models.PositiveIntegerField(default=0)
    num_people = models.PositiveIntegerField(default=0)
    riffle = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)

    # Sensitive/intolerant to pollution
    caddisfly = models.PositiveIntegerField(default=0)
    mayfly = models.PositiveIntegerField(default=0)
    riffle_beetle = models.PositiveIntegerField(default=0)
    stonefly = models.PositiveIntegerField(default=0)
    water_penny = models.PositiveIntegerField(default=0)
    dobsonfly = models.PositiveIntegerField(default=0)
    sensitive_total = models.PositiveIntegerField(default=0)

    # Somewhat sensitive
    clam_or_mussel = models.PositiveIntegerField(default=0)
    crane_fly = models.PositiveIntegerField(default=0)
    crayfish = models.PositiveIntegerField(default=0)
    damselfly = models.PositiveIntegerField(default=0)
    dragonfly = models.PositiveIntegerField(default=0)
    scud = models.PositiveIntegerField(default=0)
    fishfly = models.PositiveIntegerField(default=0)
    alderfly = models.PositiveIntegerField(default=0)
    mite = models.PositiveIntegerField(default=0)
    somewhat_sensitive_total = models.PositiveIntegerField(default=0)

    # Tolerant
    aquatic_worm = models.PositiveIntegerField(default=0)
    blackfly = models.PositiveIntegerField(default=0)
    leech = models.PositiveIntegerField(default=0)
    midge = models.PositiveIntegerField(default=0)
    snail = models.PositiveIntegerField(default=0)
    mosquito_larva = models.PositiveIntegerField(default=0)
    tolerant_total = models.PositiveIntegerField(default=0)

    # Water quality rating
    wq_rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.site.site_name

    def clean(self):
        if ((self.caddisfly + self.mayfly + self.riffle_beetle
             + self.stonefly + self.water_penny +
             self.dobsonfly) * 3) != self.sensitive_total:
                raise ValidationError(
                    _('%(sensitive_total)s is not the correct total'),
                    params={'sensitive_total': self.sensitive_total},
                )

    class Meta:
        verbose_name = 'Macroinvertebrate'
        verbose_name_plural = 'Macroinvertebrates'
