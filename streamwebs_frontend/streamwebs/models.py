# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from numbers import Number

from django.utils import timezone
import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.text import slugify
from django.utils.dateformat import format


def _timestamp(dt):
    return int(format(dt, 'U'))


def _temp_conv(temp, unit):
    if (not (isinstance(unit, str) or isinstance(unit, unicode))) or \
            not isinstance(temp, Number):
        return None

    if unit != _('Celsius') and unit != _('Fahrenheit'):
        raise ValueError(_('Invalid unit'))

    if unit == _('Celsius'):
        return temp

    return 5/9 * (temp - 32)


class SiteManager(models.Manager):
    """
    Manager for the site class - creates a site to be used in tests
    """
    default = 'POINT(-121.3846841 44.0612385)'

    def create_site(self, site_name, location=default,
                    description='', image=None, active=True):

        site = self.create(site_name=site_name, location=location,
                           description=description, image=image, active=active)
        return site


def validate_Site_location(location):
    if location.x > 180 or location.x < -180:
        raise ValidationError(_('Longitude is not within valid range.'))
    if location.y > 90 or location.y < -90:
        raise ValidationError(_('Latitude is not within valid range.'))


@python_2_unicode_compatible
class Site(models.Model):
    """
    The Sites model holds the information of a site, including the geographic
    location as a pair of latitudinal/longitudinal coordinates and an optional
    text description of entry.
    """

    site_name = models.CharField(max_length=250, verbose_name=_('site name'))
    description = models.TextField(blank=True,
                                   verbose_name=_('site description'))
    site_slug = models.SlugField(unique=True, max_length=50, editable=False)

    # Geo Django fields to store a point
    location = models.PointField(default='POINT(-121.3846841 44.0612385)',
                                 verbose_name=_('location'),
                                 validators=[validate_Site_location])
    image = models.ImageField(null=True, blank=True, verbose_name=_('image'),
                              upload_to='site_photos/')
    active = models.BooleanField(default=True)

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    objects = models.Manager()  # default manager
    test_objects = SiteManager()  # custom manager for use in writing tests

    def __str__(self):
        return self.site_name

    def to_dict(self):
        return {
            'site_name': self.site_name,
            'site_slug': self.site_slug,
            'description': self.description,
            'location': {
                'x': self.location.x,
                'y': self.location.y
            },
            'created': _timestamp(self.created),
            'modified': _timestamp(self.modified)
        }

    def save(self, **kwargs):
        'Ensure site_slug is a unique, not-null field'
        if not self.site_slug:
            self.site_slug = origSlug = slugify(self.site_name)[:50]
            # If the generated slug is not unique, append a number
            for i in xrange(1, 99):
                if not Site.objects.filter(site_slug=self.site_slug).exists():
                    break
                # Ensure the slug is never longer than it's field's maxiumum
                self.site_slug = "%s%d" % (origSlug[:50-len(str(i))], i)
        super(Site, self).save()


class SchoolManager(models.Manager):
    """
    Manager for the school class - creates a school to be used in tests
    """
    def create_school(self, name, school_type='Test', address='12345 Foo St',
                      city='Bar', province='Baz', zipcode='54321',
                      active=True):

        school = self.create(name=name, school_type=school_type,
                             address=address, city=city, province=province,
                             zipcode=zipcode, active=active)
        return school


@python_2_unicode_compatible
class School(models.Model):
    name = models.CharField(max_length=250)
    school_type = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    province = models.CharField(max_length=250, blank=True)
    zipcode = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    # nid and assoc_uid are only used by the data_scripts to make relations
    # between the models
    # nid = models.PositiveIntegerField(blank=True, null=True)
    # assoc_uid = models.PositiveIntegerField(blank=True, null=True)

    test_objects = SchoolManager()
    objects = models.Manager()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SchoolRelations(models.Model):
    uid = models.PositiveIntegerField(blank=True, null=True)
    school = models.ForeignKey(
        School, null=True, on_delete=models.CASCADE,
        limit_choices_to={'active': True}
    )

    objects = models.Manager()

    def __str__(self):
        return self.name


def validate_UserProfile_birthdate(birthdate):
    today = datetime.datetime.now()
    if birthdate.year > today.year - 13:
        raise ValidationError(_('You must be at least 13'))
    elif birthdate.year == today.year - 13:
        if birthdate.month > today.month:
            raise ValidationError(_('You must be at least 13'))
        elif birthdate.month == today.month:
            if birthdate.day > today.day:
                raise ValidationError(_('You must be at least 13'))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    birthdate = models.DateField(validators=[validate_UserProfile_birthdate],
                                 verbose_name=_('birthdate'))

    def __unicode__(self):
        return self.user.username


class WaterQualityManager(models.Manager):
    """
    Manager for the Water_Quality model/datasheet.
    """
    def create_water_quality(self, site, date, school, DEQ_dq_level,
                             latitude, longitude, fish_present,
                             live_fish, dead_fish, air_temp_unit,
                             water_temp_unit, notes=''):

        wq_info = self.create(site=site,
                              date=date,
                              school=school,
                              DEQ_dq_level=DEQ_dq_level,
                              latitude=latitude,
                              longitude=longitude,
                              fish_present=fish_present,
                              live_fish=live_fish,
                              dead_fish=dead_fish,
                              air_temp_unit=air_temp_unit,
                              water_temp_unit=water_temp_unit,
                              notes=notes)
        return wq_info


def validate_WaterQuality_latitude(latitude):
    if abs(latitude) > 90:
        raise ValidationError(_('Latitude is not within valid range.'))


def validate_WaterQuality_longitude(longitude):
    if abs(longitude) > 180:
        raise ValidationError(_('Longitude is not within valid range.'))


@python_2_unicode_compatible
class Water_Quality(models.Model):
    """
    The Water Quality model corresponds to the Water Quality datasheet. Each
    object has a one-to-one relationship with its specified Site.
    """
    LEVEL_A = 'A'   # Define DEQ water quality levels
    LEVEL_B = 'B'
    LEVEL_C = 'C'
    LEVEL_D = 'D'
    LEVEL_E = 'E'
    FAHRENHEIT = _('Fahrenheit')
    CELSIUS = _('Celsius')

    DEQ_DQ_CHOICES = (
        (None, '-----'),
        (LEVEL_A, _('Level A')),
        (LEVEL_B, _('Level B')),
        (LEVEL_C, _('Level C')),
        (LEVEL_D, _('Level D')),
        (LEVEL_E, _('Level E')),
    )

    BOOL_CHOICES = (('True', _('Yes')), ('False', _('No')))
    UNIT_CHOICES = ((FAHRENHEIT, _('Fahrenheit')), (CELSIUS, _('Celsius')))

    site = models.ForeignKey(
        Site, null=True, on_delete=models.CASCADE,
        verbose_name=_('Stream/Site name'), limit_choices_to={'active': True}
    )
    date = models.DateField(
        default=datetime.date.today, verbose_name=_('date')
    )
    DEQ_dq_level = models.CharField(
        max_length=10, choices=DEQ_DQ_CHOICES,
        default=None, null=True, verbose_name=_('DEQ data quality level')
    )
    school = models.ForeignKey(
        School, null=True, on_delete=models.CASCADE,
        verbose_name=_('school'), limit_choices_to={'active': True}
    )
    latitude = models.DecimalField(
        null=True, max_digits=9, decimal_places=6,
        verbose_name=_('latitude'), validators=[validate_WaterQuality_latitude]
    )
    longitude = models.DecimalField(
        null=True, max_digits=9, decimal_places=6,
        verbose_name=_('longitude'),
        validators=[validate_WaterQuality_longitude]
    )
    fish_present = models.CharField(
        max_length=255, choices=BOOL_CHOICES, default=0, null=True,
        verbose_name=_('any fish present?')
    )
    live_fish = models.PositiveSmallIntegerField(
        default=0, null=True, verbose_name=_('number of live fish')
    )
    dead_fish = models.PositiveSmallIntegerField(
        default=0, null=True, verbose_name=_('number of dead fish')
    )
    water_temp_unit = models.CharField(
        max_length=255, choices=UNIT_CHOICES, default=0, null=True,
        verbose_name=_('water temperature units')
    )
    air_temp_unit = models.CharField(
        max_length=255, choices=UNIT_CHOICES, default=0, null=True,
        verbose_name=_('air temperature units')
    )
    notes = models.TextField(blank=True, verbose_name=_('notes'))
    nid = models.PositiveIntegerField(blank=True, null=True)

    # Uid used to make relations between school and data sheet
    uid = models.PositiveIntegerField(blank=True, null=True)

    test_objects = WaterQualityManager()
    objects = models.Manager()

    def __str__(self):
        if self.site is not None:
            return self.site.site_name + ' data sheet ' + str(self.id)
        else:
            return _('Unspecified site for data sheet ') + str(self.id)

    def to_dict(self):
        samples = WQ_Sample.objects.filter(water_quality=self)
        return {
            'DEQ_dq_level': self.DEQ_dq_level,
            'date': _timestamp(self.date),
            'school': self.school,
            'location': {
                'x': str(self.longitude),
                'y': str(self.latitude)
            },
            'fish_present': self.fish_present,
            'live_fish': self.live_fish,
            'dead_fish': self.dead_fish,
            'air_temp_unit': self.air_temp_unit,
            'water_temp_unit': self.water_temp_unit,
            'notes': self.notes,
            'samples': [m.to_dict() for m in samples]
        }

    class Meta:
        verbose_name = 'water quality'
        verbose_name_plural = 'water quality'


class WQSampleManager(models.Manager):
    """
    Manager for the water quality samples - creates both the required and
    additional field data for the Water Quality datasheet tests
    """
    def create_sample(
        self, water_quality, sample, water_temperature, water_temp_tool,
        air_temperature, air_temp_tool, dissolved_oxygen, oxygen_tool, pH,
        pH_tool, turbidity, turbid_tool, salinity, salt_tool,
        conductivity=None, total_solids=None, bod=None, ammonia=None,
        nitrite=None, nitrate=None, phosphates=None, fecal_coliform=None
    ):
        info = self.create(
            water_quality=water_quality,
            sample=sample,
            water_temperature=water_temperature,
            water_temp_tool=water_temp_tool,
            air_temperature=air_temperature,
            air_temp_tool=air_temp_tool,
            dissolved_oxygen=dissolved_oxygen,
            oxygen_tool=oxygen_tool,
            pH=pH,
            pH_tool=pH_tool,
            turbidity=turbidity,
            turbid_tool=turbid_tool,
            salinity=salinity,
            salt_tool=salt_tool,
            conductivity=conductivity,
            total_solids=total_solids,
            bod=bod,
            ammonia=ammonia,
            nitrite=nitrite,
            nitrate=nitrate,
            phosphates=phosphates,
            fecal_coliform=fecal_coliform
        )
        return info


def validate_pH(ph):
    if not(0 <= ph <= 14):
        raise ValidationError(
            '%(ph)s is not 0-14.',
            params={'ph': ph},
        )


@python_2_unicode_compatible
class WQ_Sample(models.Model):
    """
    The WQ_Sample model describes each water quality sample
    """
    NOT_ACCESSED = 'N/A'
    VERNIER = _('Vernier')
    MANUAL = _('Manual')
    TOOL_CHOICES = ((MANUAL, _('Manual')), (VERNIER, _('Vernier')),)

    # These are required fields
    water_quality = models.ForeignKey(
        Water_Quality,
        on_delete=models.CASCADE,
        related_name='water_quality',
        null=True
    )
    DEFAULT = '(Select a sample number)'
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    TOOL_CHOICES = ((NOT_ACCESSED, None),
                    (MANUAL, _('Manual')),
                    (VERNIER, _('Vernier')),)
    SAMPLE_CHOICES = ((DEFAULT, _('(Select a sample number)')),
                      (ONE, 1),
                      (TWO, 2),
                      (THREE, 3),
                      (FOUR, 4),)

    # These are required fields
    water_quality = models.ForeignKey(Water_Quality, on_delete=models.CASCADE,
                                      related_name='water_quality', null=True)
    sample = models.CharField(max_length=255, choices=SAMPLE_CHOICES,
                              null=True, default=SAMPLE_CHOICES[0])
    water_temperature = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True,
        verbose_name=_('water temperature')
    )
    water_temp_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0, null=True,
    )
    air_temperature = models.DecimalField(
        default=0, null=True, max_digits=5, decimal_places=2,
        verbose_name=_('air temperature')
    )
    air_temp_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0, null=True,
    )
    dissolved_oxygen = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True,
        verbose_name=_('dissolved oxygen (mg/L)')
    )
    oxygen_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0, null=True,
    )
    pH = models.DecimalField(
        validators=[validate_pH], default=0, null=True,
        max_digits=5, decimal_places=2, verbose_name=_('pH')
    )
    pH_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0, null=True
    )
    turbidity = models.DecimalField(
        default=0, null=True, max_digits=5, decimal_places=2,
        verbose_name=_('turbidity (NTU)')
    )
    turbid_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0, null=True,
    )
    salinity = models.DecimalField(
        default=0, null=True, max_digits=5, decimal_places=2,
        verbose_name=_('salinity (PSU) PPT')
    )
    salt_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0, null=True
    )
    # The following are optional fields
    conductivity = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('conductivity (µS/cm)')
    )
    total_solids = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('total solids (mg/L)')
    )
    bod = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('BOD (mg/L)')
    )
    ammonia = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('ammonia (mg/L)')
    )
    nitrite = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('nitrite (mg/L)')
    )
    nitrate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('nitrate (mg/L)')
    )
    phosphates = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('phosphates (mg/L)')
    )
    fecal_coliform = models.DecimalField(
        max_digits=5,
        decimal_places=2, blank=True,
        null=True,
        verbose_name=_('fecal coliform (CFU/100 mL)')
    )
    nid = models.PositiveIntegerField(blank=True, null=True)

    test_objects = WQSampleManager()
    objects = models.Manager()

    def __str__(self):
        if self.water_quality.site is not None:
            return self.water_quality.site.site_name + ' sheet ' + \
                str(self.water_quality.id) + ' sample ' + str(self.sample)
        else:
            return ' Unspecified site: sheet ' + \
                str(self.water_quality.id) + ' sample ' + str(self.sample)

    def to_dict(self):
        return {
            'water_temperature': str(_temp_conv(self.water_temperature,
                                     self.water_quality.water_temp_unit)),
            'water_temp_tool': self.water_temp_tool,
            'air_temperature': str(_temp_conv(self.air_temperature,
                                   self.water_quality.air_temp_unit)),
            'air_temp_tool': self.air_temp_tool,
            'dissolved_oxygen': str(self.dissolved_oxygen),
            'oxygen_tool': self.oxygen_tool,
            'pH': str(self.pH),
            'pH_tool': self.pH_tool,
            'turbidity': str(self.turbidity),
            'turbid_tool': self.turbid_tool,
            'salinity': str(self.salinity),
            'salt_tool': self.salt_tool,
            'conductivity': str(self.conductivity),
            'total_solids': str(self.total_solids),
            'bod': str(self.bod),
            'ammonia': str(self.ammonia),
            'nitrite': str(self.nitrite),
            'nitrate': str(self.nitrate),
            'phosphates': str(self.phosphates),
            'fecal_coliform': str(self.fecal_coliform)
        }

    class Meta:
        verbose_name = 'water quality sample'
        verbose_name_plural = 'water quality samples'


class CameraPointManager(models.Manager):

    def create_camera_point(self, site, cp_date, location, map_datum='',
                            description=''):

        return self.create(site=site, cp_date=cp_date, location=location,
                           map_datum=map_datum, description=description)


class CameraPoint(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    letter = models.CharField(null=True, max_length=5, editable=False)
    cp_date = models.DateField(default=datetime.date.today,
                               verbose_name=_('date established'))
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE,
                               verbose_name=_('school'))
    location = models.PointField(null=True, verbose_name=_('location'))
    map_datum = models.CharField(max_length=255, blank=True,
                                 verbose_name=_('map datum'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    created = models.DateTimeField(default=timezone.now)

    test_objects = CameraPointManager()
    objects = models.Manager()

    def __str__(self):
        return (_('Camera point ') + self.letter + _(' for site ') +
                self.site.site_name)

    def save(self, **kwargs):
        if not self.letter:
            site_cps = CameraPoint.objects.filter(site_id=self.site.id)
            if not site_cps.exists():
                self.letter = 'A'
            else:
                prev_letter = site_cps.latest('created').letter
                max_len = len(prev_letter)
                if prev_letter[0] == 'Z':
                    self.letter = (max_len + 1) * 'A'
                else:
                    self.letter = max_len * chr(ord(prev_letter[0]) + 1)
        super(CameraPoint, self).save()

    class Meta:
        verbose_name = _('camera point')
        verbose_name_plural = _('camera points')


class PhotoPointManager(models.Manager):

    def create_photo_point(self, camera_point, pp_date, compass_bearing,
                           distance, camera_height, notes=''):

        return self.create(camera_point=camera_point, pp_date=pp_date,
                           compass_bearing=compass_bearing, distance=distance,
                           camera_height=camera_height, notes=notes)


class PhotoPoint(models.Model):
    camera_point = models.ForeignKey(CameraPoint, on_delete=models.CASCADE,
                                     null=True, related_name='camera_point')
    number = models.PositiveSmallIntegerField(null=True, editable=False)
    pp_date = models.DateField(default=datetime.date.today,
                               verbose_name=_('date established'))
    compass_bearing = models.PositiveSmallIntegerField(
        verbose_name=_('compass bearing'))
    distance = models.DecimalField(
        max_digits=3, decimal_places=0,
        verbose_name=_('distance from camera point'))
    camera_height = models.DecimalField(max_digits=3, decimal_places=0,
                                        verbose_name=_('camera height'))
    notes = models.TextField(blank=True, verbose_name=_('notes'))

    test_objects = PhotoPointManager()
    objects = models.Manager()

    def __str__(self):
        return (_('Photo point ') + str(self.number) + _(' for camera point ')
                + self.camera_point.letter)

    def save(self, **kwargs):
        if not self.number:
            p = PhotoPoint.objects.filter(camera_point_id=self.camera_point.id)
            if not p.exists():
                self.number = 1
            else:
                prev_num = p.latest('number').number
                self.number = prev_num + 1
        super(PhotoPoint, self).save()

    class Meta:
        verbose_name = _('photo point')
        verbose_name_plural = _('photo points')


class PhotoPointImage(models.Model):
    photo_point = models.ForeignKey(PhotoPoint, on_delete=models.CASCADE,
                                    null=True, related_name='photo_point')
    image = models.ImageField(null=True, upload_to='pp_photos/',
                              verbose_name=_('photo'))
    date = models.DateField(default=datetime.date.today,
                            verbose_name=_('date taken'))

    def __str__(self):
        return (str(self.date) + _(' for photo point ') +
                str(self.photo_point.number))

    class Meta:
        verbose_name = _('photo point image')
        verbose_name_plural = _('photo point images')


class MacroinvertebratesManager(models.Manager):
    """
    Manager for the Macroinvertebrates model.
    """
    def create_macro(self, site, school, time_spent=0, num_people=0,
                     water_type='riff', caddisfly=0, mayfly=0, riffle_beetle=0,
                     stonefly=0, water_penny=0, dobsonfly=0, clam_or_mussel=0,
                     crane_fly=0, crayfish=0, damselfly=0, dragonfly=0, scud=0,
                     fishfly=0, alderfly=0, mite=0, aquatic_worm=0, blackfly=0,
                     leech=0, midge=0, snail=0, mosquito_larva=0, notes=''):

        info = self.create(school=school,
                           date_time='2016-07-11 14:09',
                           weather='bbbb',
                           site=site,
                           time_spent=time_spent,
                           num_people=num_people,
                           water_type=water_type,
                           caddisfly=caddisfly,
                           mayfly=mayfly,
                           riffle_beetle=riffle_beetle,
                           stonefly=stonefly,
                           water_penny=water_penny,
                           dobsonfly=dobsonfly,
                           clam_or_mussel=clam_or_mussel,
                           crane_fly=crane_fly,
                           crayfish=crayfish,
                           damselfly=damselfly,
                           dragonfly=dragonfly,
                           scud=scud,
                           fishfly=fishfly,
                           alderfly=alderfly,
                           mite=mite,
                           aquatic_worm=aquatic_worm,
                           blackfly=blackfly,
                           leech=leech,
                           midge=midge,
                           snail=snail,
                           mosquito_larva=mosquito_larva,
                           notes=notes)
        return info


@python_2_unicode_compatible
class Macroinvertebrates(models.Model):
    RIFFLE = 'riff'
    POOL = 'pool'

    WATER_TYPE_CHOICES = (
        (None, '-----'),
        (RIFFLE, _('riffle')),
        (POOL, _('pool')),
    )

    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE,
                               verbose_name=_('school'))
    date_time = models.DateTimeField(default=timezone.now,
                                     verbose_name=_('date and time'))
    weather = models.CharField(max_length=250,
                               verbose_name=_('weather'))
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE,
                             limit_choices_to={'active': True})
    time_spent = models.PositiveIntegerField(
        default=None, null=True,
        verbose_name=_('Time spent sorting/identifying')
        )
    num_people = models.PositiveIntegerField(
        default=None, null=True,
        verbose_name=_('Number of people sorting/identifying')
        )
    water_type = models.CharField(max_length=4, verbose_name=_('water type'),
                                  choices=WATER_TYPE_CHOICES, default=None)
    notes = models.TextField(blank=True, verbose_name=_('field notes'))

    # Sensitive/intolerant to pollution
    caddisfly = models.PositiveIntegerField(default=0,
                                            verbose_name=_('caddisfly'))
    mayfly = models.PositiveIntegerField(default=0,
                                         verbose_name=_('mayfly'))
    riffle_beetle = models.PositiveIntegerField(
        default=0, verbose_name=_('riffle beetle')
        )
    stonefly = models.PositiveIntegerField(default=0,
                                           verbose_name=_('stonefly'))
    water_penny = models.PositiveIntegerField(default=0,
                                              verbose_name=_('water penny'))
    dobsonfly = models.PositiveIntegerField(default=0,
                                            verbose_name=_('dobsonfly'))
    sensitive_total = models.PositiveIntegerField(
        default=0, verbose_name=_('sensitive total')
        )

    # Somewhat sensitive
    clam_or_mussel = models.PositiveIntegerField(default=0,
                                                 verbose_name=_('clam/mussel'))
    crane_fly = models.PositiveIntegerField(default=0,
                                            verbose_name=_('crane fly'))
    crayfish = models.PositiveIntegerField(default=0,
                                           verbose_name=_('crayfish'))
    damselfly = models.PositiveIntegerField(default=0,
                                            verbose_name=_('damselfly'))
    dragonfly = models.PositiveIntegerField(default=0,
                                            verbose_name=_('dragonfly'))
    scud = models.PositiveIntegerField(default=0, verbose_name=_('scud'))
    fishfly = models.PositiveIntegerField(default=0, verbose_name=_('fishfly'))
    alderfly = models.PositiveIntegerField(default=0,
                                           verbose_name=_('alderfly'))
    mite = models.PositiveIntegerField(default=0, verbose_name=_('mite'))
    somewhat_sensitive_total = models.PositiveIntegerField(
        default=0, verbose_name=_('somewhat sensitive total')
        )

    # Tolerant
    aquatic_worm = models.PositiveIntegerField(default=0,
                                               verbose_name=_('aquatic worm'))
    blackfly = models.PositiveIntegerField(default=0,
                                           verbose_name=_('blackfly'))
    leech = models.PositiveIntegerField(default=0, verbose_name=_('leech'))
    midge = models.PositiveIntegerField(default=0, verbose_name=_('midge'))
    snail = models.PositiveIntegerField(default=0, verbose_name=_('snail'))
    mosquito_larva = models.PositiveIntegerField(
        default=0, verbose_name=_('mosquito larva')
        )
    tolerant_total = models.PositiveIntegerField(
        default=0, verbose_name=_('tolerant total')
        )

    # Water quality rating
    wq_rating = models.PositiveIntegerField(
        default=0, verbose_name=_('water quality rating')
        )

    # Uid used to make relations between school and data sheet
    uid = models.PositiveIntegerField(blank=True, null=True)

    objects = models.Manager()
    test_objects = MacroinvertebratesManager()

    def __str__(self):
        return self.site.site_name + ' sheet ' + str(self.id)

    def save(self, **kwargs):
        self.sensitive_total = 0
        self.somewhat_sensitive_total = 0

        # divvy up indiv count values into three arrays
        sensitive = [self.caddisfly, self.mayfly, self.riffle_beetle,
                     self.stonefly, self.water_penny, self.dobsonfly]
        somewhat = [self.clam_or_mussel, self.crane_fly, self.crayfish,
                    self.damselfly, self.dragonfly, self.scud, self.fishfly,
                    self.alderfly, self.mite]
        tolerant = [self.aquatic_worm, self.blackfly, self.leech, self.midge,
                    self.snail, self.mosquito_larva]

        # loop thru each array-- if a bug's count is at least one, that bug
        # gets n points towards its category's final score (n = 3 for
        # sensitive, n = 2 for somewhat sensitive, n = 1 for tolerant)
        for count in sensitive:
            if count > 0:
                self.sensitive_total += 3

        for count in somewhat:
            if count > 0:
                self.somewhat_sensitive_total += 2

        for count in tolerant:
            if count > 0:
                self.tolerant_total += 1

        # the water quality rating is just the sum of the three scores
        self.wq_rating = (self.sensitive_total +
                          self.somewhat_sensitive_total + self.tolerant_total)

        super(Macroinvertebrates, self).save()

    class Meta:
        verbose_name = _('macroinvertebrate')
        verbose_name_plural = _('macroinvertebrates')

    def get_tolerant_counts(self):
        return [
            {'name': _('Aquatic Worm'), 'value': self.aquatic_worm},
            {'name': _('Blackfly'), 'value': self.blackfly},
            {'name': _('Leech'), 'value': self.leech},
            {'name': _('Midge'), 'value': self.midge},
            {'name': _('Snail'), 'value': self.snail},
            {'name': _('Mosquito Larva'), 'value': self.mosquito_larva}
        ]

    def get_somewhat_sensitive_counts(self):
        return [
            {'name': _('Mussel/Clam'), 'value': self.clam_or_mussel},
            {'name': _('Crane Fly'), 'value': self.crane_fly},
            {'name': _('Crayfish'), 'value': self.crayfish},
            {'name': _('Damselfly'), 'value': self.damselfly},
            {'name': _('Dragonfly'), 'value': self.dragonfly},
            {'name': _('Scud'), 'value': self.scud},
            {'name': _('Fishfly'), 'value': self.fishfly},
            {'name': _('Alderfly'), 'value': self.alderfly},
            {'name': _('Mite'), 'value': self.mite}
        ]

    def get_sensitive_counts(self):
        return [
            {'name': _('Riffle Beetle'), 'value': self.riffle_beetle},
            {'name': _('Mayfly'), 'value': self.mayfly},
            {'name': _('Water Penny'), 'value': self.water_penny},
            {'name': _('Stonefly'), 'value': self.stonefly},
            {'name': _('Caddisfly'), 'value': self.caddisfly},
            {'name': _('Dobsonfly'), 'value': self.dobsonfly}
        ]

    def get_totals(self):
        # total number of somewhat sensitive macros found:
        somewhat = (int(self.clam_or_mussel) + int(self.crane_fly) +
                    int(self.crayfish) + int(self.damselfly) +
                    int(self.dragonfly) + int(self.scud) + int(self.fishfly) +
                    int(self.alderfly) + int(self.mite))

        # total number of sensitive macros found:
        sensitive = (int(self.caddisfly) + int(self.mayfly) +
                     int(self.riffle_beetle) + int(self.stonefly) +
                     int(self.water_penny) + int(self.dobsonfly))

        # total number of tolerant macros found:
        tolerant = (int(self.aquatic_worm) + int(self.blackfly) +
                    int(self.leech) + int(self.midge) + int(self.snail) +
                    int(self.mosquito_larva))

        return {
            _('Tolerant'): tolerant,
            _('Somewhat Sensitive'): somewhat,
            _('Sensitive'): sensitive
        }


class RipTransectManager(models.Manager):
    """
    Manager for the RiparianTransect model/datasheet.
    """
    def create_transect(self, school, date_time, site, weather='', slope=None,
                        notes=''):
        return self.create(school=school, date_time=date_time, site=site,
                           weather=weather, slope=slope, notes=notes)


def validate_slope(slope):
    if not(0 <= slope):
        raise ValidationError(
            '%(slope)s is not positive.',
            params={'slope': slope},
            )


class RiparianTransect(models.Model):
    """
    This model corresponds to the Riparian Transect data sheet and has a one-to
    -one relationship with its specified Site.
    """
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE,
                               verbose_name=_('school'))
    date_time = models.DateTimeField(default=timezone.now,
                                     verbose_name=_('date and time'))
    weather = models.CharField(max_length=255, blank=True,
                               verbose_name=_('weather'))
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE,
                             verbose_name=_('site'),
                             limit_choices_to={'active': True})
    slope = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=3,
        verbose_name=_('slope of stream bank (rise over run)')
    )
    notes = models.TextField(blank=True, verbose_name=_('notes'))
    nid = models.PositiveIntegerField(blank=True, null=True)

    # Uid used to make relations between school and data sheet
    uid = models.PositiveIntegerField(blank=True, null=True)

    test_objects = RipTransectManager()
    objects = models.Manager()

    def __str__(self):
        return (_('Transect ') + str(self.id) + _(' for site ')
                + self.site.site_name)

    class Meta:
        verbose_name = _('riparian transect')
        verbose_name_plural = _('riparian transects')


class TransectZoneManager(models.Manager):
    """
    Manager for the TransectZone model.
    """
    def create_zone(self, transect, conifers=0, hardwoods=0, shrubs=0,
                    comments=''):
        return self.create(transect=transect, conifers=conifers,
                           hardwoods=hardwoods, shrubs=shrubs,
                           comments=comments)


class TransectZone(models.Model):
    """
    Each Riparian Transect datasheet requires five zones.
    """
    ZONE_1 = 1
    ZONE_2 = 2
    ZONE_3 = 3
    ZONE_4 = 4
    ZONE_5 = 5

    ZONES = ((ZONE_1, 1), (ZONE_2, 2), (ZONE_3, 3), (ZONE_4, 4), (ZONE_5, 5))

    transect = models.ForeignKey(RiparianTransect, on_delete=models.CASCADE,
                                 related_name='transect', null=True)
    zone_num = models.CharField(max_length=1, default=0, choices=ZONES)
    conifers = models.PositiveSmallIntegerField(default=0, null=True,
                                                verbose_name=_('conifers'))
    hardwoods = models.PositiveSmallIntegerField(default=0, null=True,
                                                 verbose_name=_('hardwoods'))
    shrubs = models.PositiveSmallIntegerField(default=0, null=True,
                                              verbose_name=_('shrubs'))
    comments = models.TextField(blank=True, default='',
                                verbose_name=_('additional comments'))

    test_objects = TransectZoneManager()
    objects = models.Manager()

    def __str__(self):
        return ('Zone ' + str(self.zone_num) + ' for transect ' +
                str(self.transect.id))

    class Meta:
        verbose_name = 'zone'
        verbose_name_plural = 'zones'


def validate_cover(canopy_cover):
    if canopy_cover & 0b11111111000000000000000000000000 != 0:
        raise ValidationError(
            '%(canopy_cover)s has bad bits set.',
            params={'canopy_cover': canopy_cover},
            )


def validate_total_cover(est_canopy_cover):
    if not(0 <= est_canopy_cover and est_canopy_cover <= 96):
        raise ValidationError(
            '%(est_canopy_cover)s is not 0-96.',
            params={'est_canopy_cover': est_canopy_cover},
            )


@python_2_unicode_compatible
class Canopy_Cover(models.Model):
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE,
                               verbose_name=_('school'))
    date_time = models.DateTimeField(default=timezone.now,
                                     verbose_name=_('date and time'))
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE,
                             verbose_name=_('site'))
    weather = models.CharField(max_length=250, verbose_name=_('weather'))
    north_cc = models.IntegerField(
        default=0, validators=[validate_cover],
        verbose_name=_('north canopy cover')
        )
    east_cc = models.IntegerField(
        default=0, validators=[validate_cover],
        verbose_name=_('east canopy cover')
        )
    south_cc = models.IntegerField(
        default=0, validators=[validate_cover],
        verbose_name=_('south canopy cover')
        )
    west_cc = models.IntegerField(
        default=0, validators=[validate_cover],
        verbose_name=_('west canopy cover')
        )
    est_canopy_cover = models.PositiveIntegerField(
        default=0, validators=[validate_total_cover],
        verbose_name=_('estimated canopy cover')
        )

    # Uid used to make relations between school and data sheet
    uid = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return(str(self.date_time) + ' ' + self.site.site_name)

    class Meta:
        verbose_name = _('canopy cover survey')
        verbose_name_plural = _('canopy cover surveys')


@python_2_unicode_compatible
class Soil_Survey(models.Model):
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE,
                               verbose_name=_('school'))
    date = models.DateTimeField(default=timezone.now,
                                verbose_name=_('date and time'))
    weather = models.CharField(max_length=250, verbose_name=_('weather'),
                               blank=True)
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE,
                             verbose_name=_('site'))

    landscape_pos_choices = [
        ('summit', _('Summit')),
        ('slope', _('Slope')),
        ('depression', _('Depression')),
        ('large_flat', _('Large Flat Area')),
        ('stream_bank', _('Stream Bank'))
    ]

    cover_type_choices = [
        ('bare_soil', _('Bare Soil')),
        ('rocks', _('Rocks')),
        ('grass', _('Grass')),
        ('shrubs', _('Shrubs')),
        ('trees', _('Trees'))
    ]

    land_use_choices = [
        ('urban', _('Urban')),
        ('agricultural', _('Agricultural')),
        ('recreation', _('Recreation')),
        ('wilderness', _('Wilderness')),
        ('other', _('Other'))
    ]

    landscape_pos = models.CharField(max_length=11, default=None,
                                     choices=landscape_pos_choices)
    cover_type = models.CharField(max_length=9, default=None,
                                  choices=cover_type_choices)
    land_use = models.CharField(max_length=12, default=None,
                                choices=land_use_choices)

    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                   verbose_name=_('distance from stream (ft)'))
    site_char = models.TextField(blank=True,
                                 verbose_name=_('distinguishing site \
                                 characteristics'))

    soil_type_choices = [
        (None, '-----'),
        ('sand', _('Sand')),
        ('loamy_sand', _('Loamy Sand')),
        ('silt_loam', _('Silt Loam')),
        ('loam', _('Loam')),
        ('clay_loam', _('Clay Loam')),
        ('light_clay', _('Light Clay')),
        ('heavy_clay', _('Heavy Clay')),
        ('n/a', _('N/A')),
        ('other', _('Other'))
    ]

    soil_type = models.CharField(max_length=10, default=None,
                                 choices=soil_type_choices)

    # Uid used to make relations between school and data sheet
    uid = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.site.site_name

    class Meta:
        verbose_name = _('soil survey')
        verbose_name_plural = _('soil surveys')


class ResourceManager(models.Model):
    """ Manager for the Resources model """
    def create_resource(
        self, name, res_type, downloadable, thumbnail, sort_order
    ):
        return self.create(
            name=name, res_type=res_type, downloadable=downloadable,
            thumbnail=thumbnail, sort_order=sort_order
        )


class Resource(models.Model):
    """ This model organizes Resources like pdfs or videos """
    TYPE_CHOICES = (
        (None, '-----'),
        ('data_sheet', _('Data Sheet')),
        ('publication', _('Publication')),
        ('tutorial_video', _('Tutorial Video')),
    )
    name = models.CharField(max_length=255, blank=False)
    res_type = models.CharField(
        max_length=255, blank=False, choices=TYPE_CHOICES
    )
    # bad way to handle upload_to!  It should be based on res_type
    downloadable = models.FileField(upload_to='assets/', blank=True)
    thumbnail = models.ImageField(upload_to='assets/thumbnails/', blank=True)
    sort_order = models.PositiveSmallIntegerField(default=1000)

    objects = models.Manager()
    test_objects = ResourceManager()

    class Meta:
        verbose_name = _('resource')
        verbose_name_plural = _('resources')

    def __str__(self):
        return self.name
