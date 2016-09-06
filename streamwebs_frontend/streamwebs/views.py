# coding=UTF-8

from __future__ import print_function
from __future__ import print_function
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory
from streamwebs.forms import (
    UserForm, UserProfileForm, RiparianTransectForm, MacroinvertebratesForm,
    Canopy_Cover_Form, CC_Cardinal_Form)
from streamwebs.models import (
    RiparianTransect, Site, TransectZone, Macroinvertebrates, Canopy_Cover,
    CC_Cardinal)
from datetime import datetime
import json


def _timestamp(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()


# Create your views here.
def index(request):
    return render(request, 'streamwebs/index.html', {})


def sites(request):
    # TODO: actual lookup
    site_list = [
        {
            'name': 'Test 1',
            'slug': 'test1',
            'site_type': 'steward',
            'location': {'x': -122.31211423, 'y': 45.11231324}
        },
        {
            'name': 'Test 2',
            'slug': 'test2',
            'site_type': 'salmon',
            'location': {'x': -121.78305424, 'y': 44.74928593},
            'description': 'Site with a description',
        },
        {
            'name': 'Other One',
            'slug': 'other',
            'site_type': 'available',
            'location': {'x': -122.00193922, 'y': 45.01835423}
        },
        {
            'name': 'Me too',
            'slug': 'me2',
            'site_type': 'salmon',
            'location': {'x': -121.93729485, 'y': 45.62930212},
            'description': u'Embedded <b>tags</b> & unicode‽ &#x203C;'
        }
    ]
    return render(request, 'streamwebs/sites.html', {
        'sites': site_list,
    })


def site(request, site_slug):
    # TODO: actual lookup
    site = {
        'name': 'Test 1',
        'slug': 'test1',
        'site_type': 'steward',
        'location': {'x': -122.31211423, 'y': 45.11231324},
        'data': {
            'Water Quality': {
                1: '2016-06-10',
                2: '2016-06-12'
            }
        }
    }
    types = {
        'water_quality_edit': 'Water Quality'
    }
    return render(request, 'streamwebs/site_detail.html', {
        'site': site,
        'data_types': types
    })


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'streamwebs/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/streamwebs/')
        else:
            return HttpResponse(_('Invalid credentials'))
    else:
        return render(request, 'streamwebs/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/streamwebs/')


def graph_water(request, site_slug):
    # TODO: actual lookup
    return render(request, 'streamwebs/graphs/water_quality.html')


def graph_macros(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    macros = Macroinvertebrates.objects.filter(site=site)
    summary = {
        _timestamp(m.date_time): {
            'tolerant': m.get_tolerant_counts(),
            'somewhat': m.get_somewhat_sensitive_counts(),
            'sensitive': m.get_sensitive_counts()
        }
        for m in macros}

    time = {_timestamp(m.date_time): m.get_totals() for m in macros}
    return render(request, 'streamwebs/graphs/macroinvertebrates.html', {
        'data': {'summary': json.dumps(summary), 'time': json.dumps(time)},
        'site': site
    })


def water_quality(request, site_slug, data_id):
    # TODO: actual lookup
    quality_data = {
        'id': 1,
        'date': '2016-06-10',
        'site': {
            'name': 'Test 1',
            'slug': 'test1',
            'site_type': 'steward',
            'location': {'x': -122.31211423, 'y': 45.11231324}
        },
        'school': 'Education Middle School',
        'DEQ_wq_level': 'B',
        'fish_present': True,
        'live_fish': 5,
        'dead_fish': 2,
        'air_temperature_unit': 'F',
        'water_temperature_unit': 'C',
        'sample_1': {
            'water_temperature': 45,
            'water_temperature_tool': 'Vernier',
            'air_temperature': 52.3456,
            'air_temperature_tool': 'Manual',
            'dissolved_oxygen': 55.2,
            'oxygen_tool': 'Manual',
            'pH': 6.2,
            'pH_tool': 'Vernier',
            'turbidity': 12.4,
            'turbid_tool': 'Vernier',
            'salinity': 5.8,
            'salt_tool': 'Vernier',
            'conductivity': 7.644,
            'total_solids': .221,
            'bod': 15.2,
            'ammonia': 5.256,
            'nitrite': 15.2,
            'nitrate': 1.23,
            'phosphates': 8.26,
            'fecal_coliform': 54.2
        },
        'sample_2': {
            'water_temperature': 23,
            'water_temperature_tool': 'Vernier',
            'air_temperature': 123.346,
            'air_temperature_tool': 'Manual',
            'dissolved_oxygen': 87.4,
            'oxygen_tool': 'Manual',
            'pH': 7.1,
            'pH_tool': 'Vernier',
            'turbidity': 3.2,
            'turbid_tool': 'Manual',
            'salinity': 1.558,
            'salt_tool': 'Manual',
            'conductivity': 84.14,
            'total_solids': 1.32,
            'bod': 1.223,
            'ammonia': 1.223,
            'nitrite': 8.36,
            'nitrate': 9.56,
            'phosphates': 3.15,
            'fecal_coliform': 1.284
        },
        'sample_3': {
            'water_temperature': 15,
            'water_temperature_tool': 'Manual',
            'air_temperature': 32.756,
            'air_temperature_tool': 'Manual',
            'dissolved_oxygen': 5.21,
            'oxygen_tool': 'Vernier',
            'pH': 7.2,
            'pH_tool': 'Vernier',
            'turbidity': 12.4,
            'turbid_tool': 'Vernier',
            'salinity': 6.784265422397,
            'salt_tool': 'Manual',
            'conductivity': 54.0,
            'total_solids': 6.12,
            'bod': 5.3,
            'ammonia': 4.75,
            'nitrite': 0.22,
            'nitrate': 7.2,
            'phosphates': 9.4,
            'fecal_coliform': 6.23
        },
        'sample_4': {
            'water_temperature': 67,
            'water_temperature_tool': 'Vernier',
            'air_temperature': 11.56,
            'air_temperature_tool': 'Manual',
            'dissolved_oxygen': 15.24,
            'oxygen_tool': 'Vernier',
            'pH': 4.2,
            'pH_tool': 'Manual',
            'turbidity': 2.5,
            'turbid_tool': 'Manual',
            'salinity': 6.54,
            'salt_tool': 'Vernier',
            'conductivity': 94.1,
            'total_solids': 110.2,
            'bod': 8.215,
            'ammonia': 13.2,
            'nitrite': 93.4,
            'nitrate': 75.2,
            'phosphates': 64.2,
            'fecal_coliform': 57.2
        },
        'notes': 'All data completely made up for testing with.'
    }
    return render(request, 'streamwebs/datasheets/water_quality_view.html', {
        'data': quality_data
    })


def water_quality_edit(request, site_slug):
    # TODO: actual lookup
    site = {
        'name': 'Test 1',
        'slug': 'test1',
        'site_type': 'steward',
        'location': {'x': -122.31211423, 'y': 45.11231324}
    }
    return render(
        request,
        'streamwebs/datasheets/water_quality_edit.html',
        {'site': site}
    )


def macroinvertebrate(request, site_slug, data_id):
    site = Site.objects.get(site_slug=site_slug)
    # data = Macroinvertebrates.objects.filter(site_id=site.id).get(id=data_id)
    data = Macroinvertebrates.objects.get(id=data_id)
    return render(
        request,
        'streamwebs/datasheets/macroinvertebrate_view.html', {
            'data': data, 'site': site
        }
    )


def macroinvertebrate_edit(request, site_slug):
    """
    The view for the submission of a new macroinvertebrate data sheet.
    """
    site = Site.objects.get(site_slug=site_slug)
    added = False
    if request.method == 'POST':
        macro_form = MacroinvertebratesForm(data=request.POST)
        if macro_form.is_valid():
            macro_form = macro_form.save()
            added = True
    else:
        macro_form = MacroinvertebratesForm()

    return render(
        request, 'streamwebs/datasheets/macroinvertebrate_edit.html', {
            'macro_form': macro_form,
            'added': added,
            'site': site
        }
    )


def riparian_transect_view(request, site_slug, data_id):
    site = Site.objects.get(site_slug=site_slug)
    transect = RiparianTransect.objects.filter(site_id=site.id).get(id=data_id)
    zones = TransectZone.objects.filter(transect_id=transect)

    # Invoking the database by evaluating the queryset before passing it to the
    # template is necessary in order to pass Travis tests.
    # https://docs.djangoproject.com/en/1.9/ref/models/querysets/#when-querysets-are-evaluated
    zones = list(zones)

    return render(
        request, 'streamwebs/datasheets/riparian_transect_view.html', {
            'transect': transect,
            'zones': zones,
            'site': site
            }
        )


def riparian_transect_edit(request, site_slug):
    """
    The view for the submission of a new riparian transect data sheet.
    """
    added = False
    site = Site.objects.get(site_slug=site_slug)
    transect = RiparianTransect()
    TransectZoneInlineFormSet = inlineformset_factory(
        RiparianTransect, TransectZone,
        fields=('conifers', 'hardwoods', 'shrubs', 'comments'), extra=5
    )

    if request.method == 'POST':
        zone_formset = TransectZoneInlineFormSet(
            data=request.POST, instance=transect
        )
        transect_form = RiparianTransectForm(data=request.POST)

        if (zone_formset.is_valid() and transect_form.is_valid()):

            transect = transect_form.save()             # save form to object
            transect.save()                             # save object

            zones = zone_formset.save(commit=False)     # save forms to objs

            for zone in zones:                          # for each zone,
                zone.transect = transect                # assign the transect
                zone.save()                             # save the zone obj

            added = True

    else:
        zone_formset = TransectZoneInlineFormSet(instance=transect)
        transect_form = RiparianTransectForm()

    return render(
        request,
        'streamwebs/datasheets/riparian_transect_edit.html', {
            'transect_form': transect_form, 'zone_formset': zone_formset,
            'added': added, 'site': site
        }
    )


def canopy_cover_edit(request, site_slug):
    """
    The view for the submission of a new canopy cover data sheet.
    """
    added = False
    site = Site.objects.get(site_slug=site_slug)
    canopy_cover = Canopy_Cover()
    CardinalInlineFormSet = inlineformset_factory(
        Canopy_Cover, CC_Cardinal,
        fields=(
            'direction', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N','O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X',
            'num_shaded'), extra=4
    )

    if request.method == 'POST':
        cardinal_formset = CardinalInlineFormSet(
            data=request.POST, instance=canopy_cover
        )
        canopy_cover_form = Canopy_Cover_Form(data=request.POST)

        if (cardinal_formset.is_valid() and canopy_cover_form.is_valid()):

            canopy_cover = canopy_cover_form.save()             # save form to object
            canopy_cover.save()                             # save object

            cardinals = cardinal_formset.save(commit=False)     # save forms to objs

            for cardinal in cardinals:                          # for each zone,
                cardinal.canopy_cover = canopy_cover               # assign the transect
                cardinal.save()                             # save the zone obj

            added = True

    else:
        cardinal_formset = CardinalInlineFormSet(instance=canopy_cover)
        canopy_cover_form = Canopy_Cover_Form()

    return render(
        request,
        'streamwebs/datasheets/canopy_cover_edit.html', {
            'canopy_cover_form': canopy_cover_form,
            'cardinal_formset': cardinal_formset,
            'added': added, 'site': site
        }
    )
