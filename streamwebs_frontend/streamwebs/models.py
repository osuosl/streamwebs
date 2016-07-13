# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
import datetime

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify


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
        (LEVEL_A, 'Level A'),
        (LEVEL_B, 'Level B'),
        (LEVEL_C, 'Level C'),
        (LEVEL_D, 'Level D'),
        (LEVEL_E, 'Level E'),
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
        max_length=1, choices=DEQ_DQ_CHOICES,
        default=None, verbose_name=_('DEQ data quality level')
    )
    school = models.CharField(
        max_length=250, verbose_name=_('school')
    )
    latitude = models.DecimalField(
        default=0, max_digits=9, decimal_places=6, verbose_name=_('latitude'),
        validators=[validate_WaterQuality_latitude]
    )
    longitude = models.DecimalField(
        default=0, max_digits=9, decimal_places=6, verbose_name=_('longitude'),
        validators=[validate_WaterQuality_longitude]

    )
    fish_present = models.CharField(
        max_length=255, choices=BOOL_CHOICES, default=0,
        verbose_name=_('any fish present?')
    )
    live_fish = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('number of live fish')
    )
    dead_fish = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('number of dead fish')
    )
    water_temp_unit = models.CharField(
        max_length=255, choices=UNIT_CHOICES, default=0,
        verbose_name=_('water temperature units')
    )
    air_temp_unit = models.CharField(
        max_length=255, choices=UNIT_CHOICES, default=0,
        verbose_name=_('air temperature units')
    )
    notes = models.TextField(blank=True, verbose_name=_('notes'))

    # Add some logic in which the datasheet object is only created when
    # the Site in which it corresponds to actually exists

    test_objects = WaterQualityManager()
    objects = models.Manager()

    def __str__(self):
        return self.site.site_name + ' data sheet ' + str(self.id)

    class Meta:
        verbose_name = 'water quality'
        verbose_name_plural = 'water quality'


class WQSampleManager(models.Manager):
    """
    Manager for the water quality samples - creates both the required and
    additional field data for the Water Quality datasheet tests
    """
    def create_sample(
        self, water_quality, water_temperature, water_temp_tool,
        air_temperature, air_temp_tool, dissolved_oxygen, oxygen_tool, pH,
        pH_tool, turbidity, turbid_tool, salinity, salt_tool,
        conductivity=None, total_solids=None, bod=None, ammonia=None,
        nitrite=None, nitrate=None, phosphates=None, fecal_coliform=None
    ):
        info = self.create(
            water_quality=water_quality,
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
    if not(0 <= ph and ph <= 14):
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
    water_temperature = models.DecimalField(
        default=0, max_digits=5, decimal_places=2,
        verbose_name=_('water temperature')
        )
    water_temp_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0,
    )
    air_temperature = models.DecimalField(
        default=0, max_digits=5, decimal_places=2,
        verbose_name=_('air temperature')
    )
    air_temp_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0,
    )
    dissolved_oxygen = models.DecimalField(
        default=0, max_digits=5, decimal_places=2,
        verbose_name=_('dissolved oxygen (mg/L)')
    )
    oxygen_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0,
    )
    pH = models.DecimalField(
        validators=[validate_pH], default=0,
        max_digits=5, decimal_places=2, verbose_name=_('pH')
    )
    pH_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0,
    )
    turbidity = models.DecimalField(
        default=0, max_digits=5, decimal_places=2,
        verbose_name=_('turbidity (NTU)')
    )
    turbid_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0,
    )
    salinity = models.DecimalField(
        default=0, max_digits=5, decimal_places=2,
        verbose_name=_('salinity (PSU) PPT')
    )
    salt_tool = models.CharField(
        max_length=255, choices=TOOL_CHOICES, default=0,
    )
    # The following are optional fields
    conductivity = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('conductivity (µS/cm)')
    )
    total_solids = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('total solids (mg/L)')
    )
    bod = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('BOD (mg/L)')
    )
    ammonia = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('ammonia (mg/L)')
    )
    nitrite = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('nitrite (mg/L)')
    )
    nitrate = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('nitrate (mg/L)')
    )
    phosphates = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('phosphates (mg/L)')
    )
    fecal_coliform = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, blank=True,
        null=True, verbose_name=_('fecal coliform (CFU/100 mL)')
    )

    test_objects = WQSampleManager()
    objects = models.Manager()

    def __str__(self):
        return self.water_quality.site.site_name + ' sheet ' + \
               str(self.water_quality.id) + ' sample ' + str(self.id)

    class Meta:
        verbose_name = 'water quality sample'
        verbose_name_plural = 'water quality samples'


class MacroinvertebratesManager(models.Manager):
    """
    Manager for the Macroinvertebrates model.
    """
    def create_macro(self, site, time_spent=0, num_people=0, riffle=False,
                     pool=False, caddisfly=0, mayfly=0, riffle_beetle=0,
                     stonefly=0, water_penny=0, dobsonfly=0, sensitive_total=0,
                     clam_or_mussel=0, crane_fly=0, crayfish=0, damselfly=0,
                     dragonfly=0, scud=0, fishfly=0, alderfly=0, mite=0,
                     sw_sensitive_total=0, aquatic_worm=0, blackfly=0,
                     leech=0, midge=0, snail=0, mosquito_larva=0,
                     tolerant_total=0, wq_rating=0):
        info = self.create(school='aaaa',
                           date_time='2016-07-11 14:09',
                           weather="bbbb",
                           site=site,
                           time_spent=time_spent,
                           num_people=num_people,
                           riffle=riffle,
                           pool=pool,
                           caddisfly=caddisfly,
                           mayfly=mayfly,
                           riffle_beetle=riffle_beetle,
                           stonefly=stonefly,
                           water_penny=water_penny,
                           dobsonfly=dobsonfly,
                           sensitive_total=sensitive_total,
                           clam_or_mussel=clam_or_mussel,
                           crane_fly=crane_fly,
                           crayfish=crayfish,
                           damselfly=damselfly,
                           dragonfly=dragonfly,
                           scud=scud,
                           fishfly=fishfly,
                           alderfly=alderfly,
                           mite=mite,
                           somewhat_sensitive_total=sw_sensitive_total,
                           aquatic_worm=aquatic_worm,
                           blackfly=blackfly,
                           leech=leech,
                           midge=midge,
                           snail=snail,
                           mosquito_larva=mosquito_larva,
                           tolerant_total=tolerant_total,
                           wq_rating=wq_rating,)
        return info


class CameraPointManager(models.Manager):

    def create_camera_point(self, site, cp_date, created_by='', latitude=None,
                            longitude=None, map_datum='', description=''):

        return self.create(site=site, cp_date=cp_date, created_by=created_by,
                           latitude=latitude, longitude=longitude,
                           map_datum=map_datum, description=description)


class CameraPoint(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    cp_date = models.DateField(default=datetime.date.today)
    created_by = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(default=0, max_digits=9, decimal_places=6,
                                   blank=True, null=True)
    longitude = models.DecimalField(default=0, max_digits=9, decimal_places=6,
                                    blank=True, null=True)
    map_datum = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    camera_points = CameraPointManager()

    def __str__(self):
        return ('Camera point ' + str(self.id) + ' for site ' +
                self.site.site_name)

    class Meta:
        verbose_name = 'Camera Point'
        verbose_name_plural = 'Camera Points'


class PhotoPointManager(models.Manager):

    def create_photo_point(self, camera_point, pp_date, compass_bearing,
                           distance, camera_height, photo_filename='',
                           photo=None, notes=''):

        return self.create(camera_point=camera_point, pp_date=pp_date,
                           compass_bearing=compass_bearing, distance=distance,
                           camera_height=camera_height,
                           photo_filename=photo_filename, photo=photo,
                           notes=notes)


class PhotoPoint(models.Model):
    camera_point = models.ForeignKey(CameraPoint, on_delete=models.CASCADE,
                                     null=True, related_name='camera_point')
    pp_date = models.DateField(default=datetime.date.today)
    compass_bearing = models.PositiveSmallIntegerField()
    distance = models.DecimalField(max_digits=3, decimal_places=0)
    camera_height = models.DecimalField(max_digits=3, decimal_places=0)
    photo_filename = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(blank=True, null=True)
    notes = models.TextField(blank=True)

    photo_points = PhotoPointManager()

    def __str__(self):
        return ('Photo point ' + str(self.id) + ' for camera point ' +
                str(self.camera_point.id))

    class Meta:
        verbose_name = 'Photo Point'
        verbose_name_plural = 'Photo Points'


@python_2_unicode_compatible
class Macroinvertebrates(models.Model):
    school = models.CharField(max_length=250, verbose_name=_('school'))
    date_time = models.DateTimeField(default=timezone.now,
                                     verbose_name=_('date and time'))
    weather = models.CharField(max_length=250,
                               verbose_name=_('weather'))
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE,
                             limit_choices_to={'active': True})
    time_spent = models.PositiveIntegerField(
        default=None, null=True,
        verbose_name=_('time spent sorting/identifying')
        )
    num_people = models.PositiveIntegerField(
        default=None, null=True,
        verbose_name=_('# of people sorting/identifying')
        )
    riffle = models.BooleanField(default=False, verbose_name=_('riffle'))
    pool = models.BooleanField(default=False, verbose_name=_(' pool'))

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

    objects = MacroinvertebratesManager()

    def __str__(self):
        return self.site.site_name + ' sheet ' + str(self.id)

    def clean(self):
        if ((self.caddisfly + self.mayfly + self.riffle_beetle +
             self.stonefly + self.water_penny +
             self.dobsonfly) * 3) != self.sensitive_total:
                raise ValidationError(
                    _('%(sensitive_total)s is not the correct total'),
                    params={'sensitive_total': self.sensitive_total},
                )

        if ((self.clam_or_mussel + self.crane_fly + self.crayfish +
             self.damselfly + self.dragonfly + self.scud + self.fishfly +
             self.alderfly + self.mite) * 2) != self.somewhat_sensitive_total:
                raise ValidationError(
                    _('%(some_sensitive)s is not the correct total'),
                    params={'some_sensitive': self.somewhat_sensitive_total},
                )

        if (self.aquatic_worm + self.blackfly + self.leech + self.midge +
                self.snail + self.mosquito_larva) != self.tolerant_total:
                raise ValidationError(
                    _('%(tolerant_total)s is not the correct total'),
                    params={'tolerant_total': self.tolerant_total},
                )
        if(self.sensitive_total + self.somewhat_sensitive_total +
                self.tolerant_total) != self.wq_rating:
                raise ValidationError(
                    _('%(wq_rating)s is not the correct total'),
                    params={'wq_rating': self.wq_rating},
                )

    class Meta:
        verbose_name = 'macroinvertebrate'
        verbose_name_plural = 'macroinvertebrates'

    def get_tolerant_counts(self):
        return [
            {'name': 'Aquatic Worm', 'value': self.aquatic_worm},
            {'name': 'Blackfly', 'value': self.blackfly},
            {'name': 'Leech', 'value': self.leech},
            {'name': 'Midge', 'value': self.midge},
            {'name': 'Snail', 'value': self.snail},
            {'name': 'Mosquito Larva', 'value': self.mosquito_larva}
        ]

    def get_somewhat_sensitive_counts(self):
        return [
            {'name': 'Mussel/Clam', 'value': self.clam_or_mussel},
            {'name': 'Cranefly', 'value': self.crane_fly},
            {'name': 'Crayfish', 'value': self.crayfish},
            {'name': 'Damselfly', 'value': self.damselfly},
            {'name': 'Dragonfly', 'value': self.dragonfly},
            {'name': 'Scud', 'value': self.scud},
            {'name': 'Fishfly', 'value': self.fishfly},
            {'name': 'Alderfly', 'value': self.alderfly},
            {'name': 'Water Mite', 'value': self.mite}
        ]

    def get_sensitive_counts(self):
        return [
            {'name': 'Riffle Beetle', 'value': self.riffle_beetle},
            {'name': 'Mayfly', 'value': self.mayfly},
            {'name': 'Water Penny', 'value': self.water_penny},
            {'name': 'Stonefly', 'value': self.stonefly},
            {'name': 'Caddisfly', 'value': self.caddisfly},
            {'name': 'Dobsonfly', 'value': self.dobsonfly}
        ]

    def get_totals(self):
        return {
            'Tolerant': self.tolerant_total,
            'Somewhat Sensitive': self.somewhat_sensitive_total,
            'Sensitive': self.sensitive_total
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
    school = models.CharField(max_length=255, verbose_name=_('school'))
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

    objects = RipTransectManager()

    def __str__(self):
        return 'Transect ' + str(self.id) + ' for site ' + self.site.site_name

    class Meta:
        verbose_name = 'riparian transect'
        verbose_name_plural = 'riparian transects'


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
    transect = models.ForeignKey(RiparianTransect, on_delete=models.CASCADE,
                                 related_name='transect', null=True)
    conifers = models.PositiveSmallIntegerField(default=0,
                                                verbose_name=_('conifers'))
    hardwoods = models.PositiveSmallIntegerField(default=0,
                                                 verbose_name=_('hardwoods'))
    shrubs = models.PositiveSmallIntegerField(default=0,
                                              verbose_name=_('shrubs'))
    comments = models.TextField(blank=True,
                                verbose_name=_('additional comments'))

    objects = TransectZoneManager()

    def __str__(self):
        return ('Zone ' + str(self.id) + ' for transect ' +
                str(self.transect.id))

    class Meta:
        verbose_name = 'zone'
        verbose_name_plural = 'zones'


class CardinalManager(models.Manager):
    """
    Manager for the canopy cover survey's cardinal boxes - creates dummy data
    data for each of the cardinal directions
    """
    def create_shade(self, direction, A, B, C, D, E, F, G, H, I, J, K, L, M, N,
                     O, P, Q, R, S, T, U, V, W, X, num_shaded):

        cc_info = self.create(direction=direction, A=A, B=B, C=C, D=D, E=E,
                              F=F, G=G, H=H, I=I, J=J, K=K, L=L, M=M, N=N, O=O,
                              P=P, Q=Q, R=R, S=S, T=T, U=U, V=V, W=W, X=X,
                              num_shaded=num_shaded)
        return cc_info


def validate_shaded(num_shaded):
    if not(0 <= num_shaded and num_shaded <= 24):
        raise ValidationError(
            '%(num_shaded)s is not 0-24.',
            params={'num_shaded': num_shaded},
            )


@python_2_unicode_compatible
class CC_Cardinal(models.Model):
    NORTH = 'North'
    EAST = 'East'
    SOUTH = 'South'
    WEST = 'West'

    DIRECTIONS = (
        (None, '-----'),
        (NORTH, 'North'),
        (EAST, 'East'),
        (SOUTH, 'South'),
        (WEST, 'West'),
    )

    direction = models.CharField(max_length=255, choices=DIRECTIONS,
                                 default=DIRECTIONS[0],
                                 verbose_name=_('direction'))
    A = models.BooleanField(default=False, blank=True)
    B = models.BooleanField(default=False, blank=True)
    C = models.BooleanField(default=False, blank=True)
    D = models.BooleanField(default=False, blank=True)
    E = models.BooleanField(default=False, blank=True)
    F = models.BooleanField(default=False, blank=True)
    G = models.BooleanField(default=False, blank=True)
    H = models.BooleanField(default=False, blank=True)
    I = models.BooleanField(default=False, blank=True)
    J = models.BooleanField(default=False, blank=True)
    K = models.BooleanField(default=False, blank=True)
    L = models.BooleanField(default=False, blank=True)
    M = models.BooleanField(default=False, blank=True)
    N = models.BooleanField(default=False, blank=True)
    O = models.BooleanField(default=False, blank=True)
    P = models.BooleanField(default=False, blank=True)
    Q = models.BooleanField(default=False, blank=True)
    R = models.BooleanField(default=False, blank=True)
    S = models.BooleanField(default=False, blank=True)
    T = models.BooleanField(default=False, blank=True)
    U = models.BooleanField(default=False, blank=True)
    V = models.BooleanField(default=False, blank=True)
    W = models.BooleanField(default=False, blank=True)
    X = models.BooleanField(default=False, blank=True)
    num_shaded = models.PositiveIntegerField(default=0,
                                             validators=[validate_shaded],
                                             verbose_name=_('# shaded boxes'))

    objects = CardinalManager()

    def __str__(self):
        return self.direction

    class Meta:
        verbose_name = 'cardinal direction'
        verbose_name_plural = 'cardinal directions'

    def clean(self):
        shaded = 0
        squares = [self.A, self.B, self.C, self.D, self.E, self.F, self.G,
                   self.H, self.I, self.J, self.K, self.L, self.M, self.N,
                   self.O, self.P, self.Q, self.R, self.S, self.T, self.U,
                   self.V, self.W, self.X]

        for square in squares:
            if square is True:
                shaded += 1

        if(shaded != self.num_shaded):
            raise ValidationError(
                _('%(num_shaded)s is not the correct total'),
                params={'num_shaded': self.num_shaded},
            )


def validate_cover(est_canopy_cover):
    if not(0 <= est_canopy_cover and est_canopy_cover <= 96):
        raise ValidationError(
            '%(est_canopy_cover)s is not 0-96.',
            params={'est_canopy_cover': est_canopy_cover},
            )


@python_2_unicode_compatible
class Canopy_Cover(models.Model):
    school = models.CharField(max_length=250, verbose_name=_('school'))
    date_time = models.DateTimeField(default=timezone.now,
                                     verbose_name=_('date and time'))
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE,
                             verbose_name=_('site'),
                             limit_choices_to={'active': True})
    weather = models.CharField(max_length=250, verbose_name=_('weather'))
    north = models.ForeignKey(CC_Cardinal, on_delete=models.CASCADE,
                              related_name='north', null=True,
                              verbose_name=_('north'))
    east = models.ForeignKey(CC_Cardinal, on_delete=models.CASCADE,
                             related_name='east', null=True,
                             verbose_name=_('east'))
    south = models.ForeignKey(CC_Cardinal, on_delete=models.CASCADE,
                              related_name='south', null=True,
                              verbose_name=_('south'))
    west = models.ForeignKey(CC_Cardinal, on_delete=models.CASCADE,
                             related_name='west', null=True,
                             verbose_name=_('west'))
    est_canopy_cover = models.PositiveIntegerField(
        default=0, validators=[validate_cover],
        verbose_name=_('estimated canopy cover')
        )

    def __str__(self):
        return self.site.site_name + ' sheet ' + str(self.id)

    class Meta:
        verbose_name = 'canopy cover survey'
        verbose_name_plural = 'canopy cover surveys'


class PhotoPointManager(models.Manager):
    
    def create_photo_point(self, pp_date, compass_bearing, distance_feet=None,
                           distance_inches=None, camera_height_feet=None,
                           camera_height_inches=None, photo_filename=None, photo=None, notes=None):
        return self.create(pp_date=pp_date, compass_bearing=compass_bearing, distance_feet=None, distance_inches=None, camera_height_feet=None, camera_height_inches=None, photo_filename=None, photo=None, notes=None) 


class PhotoPoint(models.Model):
    pp_date = models.DateField(default=datetime.date.today)
    compass_bearing = models.DecimalField(max_digits=5, decimal_places=2)
    distance_feet = models.PositiveSmallIntegerField(blank=True, null=True)
    # Make sure later (validator) that max inches is 12, etc.
    distance_inches = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True)
    camera_height_feet = models.PositiveSmallIntegerField(
        blank=True, null=True)
    camera_height_inches = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True)
    # photo filename: necessary??
    photo_filename = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(blank=True, null=True)
    notes = models.TextField(blank=True)

    photo_points = PhotoPointManager()

    class Meta:
        verbose_name = 'Photo Point'
        verbose_name_plural = 'Photo Points'


class CameraPoint(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    cp_date = models.DateField(default=datetime.date.today)
    created_by = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True, null=True)
    longitude = models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True, null=True)
    map_datum = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    photo_pt_1 = models.ForeignKey(PhotoPoint, on_delete=models.CASCADE, related_name='photo_pt_1', null=True)
    photo_pt_2 = models.ForeignKey(PhotoPoint, on_delete=models.CASCADE, related_name='photo_pt_2', null=True)
    photo_pt_3 = models.ForeignKey(PhotoPoint, on_delete=models.CASCADE, related_name='photo_pt_3', null=True)

    def __str__(self):
        return self.site.site_name

    class Meta:
        verbose_name = 'Camera Point'
        verbose_name_plural = 'Camera Points'
