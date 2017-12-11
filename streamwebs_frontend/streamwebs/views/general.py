# coding=UTF-8
from __future__ import print_function
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from streamwebs.forms import (
    UserForm, UserFormOptionalFields, UserProfileForm, RiparianTransectForm, MacroinvertebratesForm,
    PhotoPointImageForm, PhotoPointForm, CameraPointForm, WQSampleForm,
    WQForm, SiteForm, Canopy_Cover_Form, SoilSurveyForm, StatisticsForm,
    TransectZoneForm, BaseZoneInlineFormSet, ResourceForm, AdminPromotionForm,
    UserEmailForm, UserPasswordForm, SchoolForm, RipAquaForm)

from streamwebs.models import (
    Macroinvertebrates, Site, Water_Quality, WQ_Sample, RiparianTransect,
    TransectZone, Canopy_Cover, CameraPoint, PhotoPoint,
    PhotoPointImage, Soil_Survey, Resource, School, RipAquaticSurvey,
    UserProfile, School )

import json
import copy
import datetime


def toDateTime(date, time, period):
    date_time = datetime.datetime.strptime((date + " " + time + " " + period),
                                           '%Y-%m-%d %I:%M %p')
    return date_time


def _timestamp(dt):
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()


def index(request):
    return render(request, 'streamwebs/index.html', {})


def about(request):
    return render(request, 'streamwebs/about.html', {})


def faq(request):
    return render(request, 'streamwebs/faq.html', {})


@login_required
def create_school(request):
    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
        school_form = SchoolForm(data=request.POST)

        if school_form.is_valid():
            school = school_form.save()
            school.province = (school.province + ', United States')
            school.save()
            messages.success(request,
                             _('You have successfully added a new school'))
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        school_form = SchoolForm()

    return render(request, 'streamwebs/add_school.html', {
        'school_form': school_form
    })


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
def create_site(request):
    created = False
    site_list = Site.objects.filter(active=True)

    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True

        if 'lat' in request.POST and 'lng' in request.POST:
            # convert lat/lng to pointfield object
            point = ("SRID=4326;POINT(%s %s)" %
                     (request.POST['lng'], request.POST['lat']))
            request.POST['location'] = point

        site_form = SiteForm(request.POST, request.FILES)
        if site_form.is_valid():
            site = site_form.save()
            site.save()
            created = True
            messages.success(request,
                             _('You have successfully added a new site.'))
            return redirect(reverse('streamwebs:site',
                            kwargs={'site_slug': site.site_slug}))

    else:
        site_form = SiteForm()

    return render(request, 'streamwebs/create_site.html', {
        'site_form': site_form,
        'created': created,
        'sites': site_list,
        'maps_api': settings.GOOGLE_MAPS_API,
        'map_type': settings.GOOGLE_MAPS_TYPE
        })


def sites(request):
    """ View for streamwebs/sites """
    site_list = Site.objects.filter(active=True).order_by('site_name')
    return render(request, 'streamwebs/sites.html', {
        'sites': site_list,
        'maps_api': settings.GOOGLE_MAPS_API,
        'map_type': settings.GOOGLE_MAPS_TYPE
    })


# view-view for individual specified site
def site(request, site_slug):
    """ View an individual site """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    wq_sheets = Water_Quality.objects.filter(site_id=site.id)
    wq_sheets = list(wq_sheets.order_by('-date_time').values())
    wq_sheets_new = []
    for x in wq_sheets:
        wq_data = {'id': x['id'], 'uri': 'water', 'type': 'Water Quality',
                   'date': x['date_time'].date()}
        if 'school_id' in x and x['school_id']:
            wq_data['school_id'] = x['school_id']
        else:
            wq_data['school_id'] = -1
        wq_sheets_new.append(wq_data)
    wq_sheets = wq_sheets_new

    macro_sheets = Macroinvertebrates.objects.filter(site_id=site.id)
    macro_sheets = list(macro_sheets.order_by('-date_time').values())
    macro_sheets_new = []
    for x in macro_sheets:
        macro_data = {'id': x['id'], 'uri': 'macro',
                      'type': 'Macroinvertebrate',
                      'date': x['date_time'].date()}
        if 'school_id' in x and x['school_id']:
            macro_data['school_id'] = x['school_id']
        else:
            macro_data['school_id'] = -1
        macro_sheets_new.append(macro_data)
    macro_sheets = macro_sheets_new

    transect_sheets = RiparianTransect.objects.filter(site_id=site.id)
    transect_sheets = list(transect_sheets.order_by('-date_time').values())
    transect_sheets_new = []
    for x in transect_sheets:
        transect_data = {'id': x['id'], 'uri': 'transect',
                         'type': 'Riparian Transect',
                         'date': x['date_time'].date()}
        if 'school_id' in x and x['school_id']:
            transect_data['school_id'] = x['school_id']
        else:
            transect_data['school_id'] = -1
        transect_sheets_new.append(transect_data)
    transect_sheets = transect_sheets_new

    canopy_sheets = Canopy_Cover.objects.filter(site_id=site.id)
    canopy_sheets = list(canopy_sheets.order_by('-date_time').values())
    canopy_sheets_new = []
    for x in canopy_sheets:
        canopy_data = {'id': x['id'], 'uri': 'canopy', 'type': 'Canopy Cover',
                       'date': x['date_time'].date()}
        if 'school_id' in x and x['school_id']:
            canopy_data['school_id'] = x['school_id']
        else:
            canopy_data['school_id'] = -1
        canopy_sheets_new.append(canopy_data)
    canopy_sheets = canopy_sheets_new

    ppm_sheets = CameraPoint.objects.filter(site_id=site.id)
    ppm_sheets = list(ppm_sheets.order_by('letter').values())
    ppm_sheets_new = []
    for x in ppm_sheets:
        ppm_data = {'id': x['id'], 'uri': 'camera', 'type': 'Camera Point',
                    'date': x['cp_date']}
        if 'school_id' in x and x['school_id'] is not None:
            ppm_data['school_id'] = x['school_id']
        else:
            ppm_data['school_id'] = -1
        ppm_sheets_new.append(ppm_data)
    ppm_sheets = ppm_sheets_new

    soil_sheets = Soil_Survey.objects.filter(site_id=site.id)
    soil_sheets = list(soil_sheets.order_by('-date_time').values())
    soil_sheets_new = []
    for x in soil_sheets:
        soil_data = {'id': x['id'], 'uri': 'soil', 'type': 'Soil Survey',
                     'date': x['date_time'].date()}
        if 'school_id' in x and x['school_id']:
            soil_data['school_id'] = x['school_id']
        else:
            soil_data['school_id'] = -1
        soil_sheets_new.append(soil_data)
    soil_sheets = soil_sheets_new

    rip_aqua_sheets = RipAquaticSurvey.objects.filter(site_id=site.id)
    rip_aqua_sheets = list(rip_aqua_sheets.order_by('-date_time').values())
    rip_aqua_sheets_new = []
    for x in rip_aqua_sheets:
        rip_data = {'id': x['id'], 'uri': 'rip_aqua',
                    'type': 'Riparian Aquatic', 'date': x['date_time'].date()}
        if 'school_id' in x and x['school_id']:
            rip_data['school_id'] = x['school_id']
        else:
            rip_data['school_id'] = -1
        rip_aqua_sheets_new.append(rip_data)
    rip_aqua_sheets = rip_aqua_sheets_new

    data = wq_sheets + macro_sheets + transect_sheets + canopy_sheets +\
        ppm_sheets + soil_sheets + rip_aqua_sheets

    def sort_date(x, y):
        return y.year - x.year or y.month - x.month or y.day - x.day

    data.sort(cmp=sort_date, key=lambda x: x['date'])
    data.sort(key=lambda x: -x['school_id'])

    num_schools = count_schools(data)
    number_item = len(data) + num_schools

    pages = (number_item)/10
    if number_item % 10 != 0:
        pages += 1

    data_len_range = range(2, pages + 1)
    data = add_school_name(data)

    return render(request, 'streamwebs/site_detail.html', {
        'site': site,
        'maps_api': settings.GOOGLE_MAPS_API,
        'map_type': settings.GOOGLE_MAPS_TYPE,
        'data': json.dumps(data, cls=DjangoJSONEncoder),
        'data_len_range': data_len_range,
        'pages': pages,
        'has_wq': len(wq_sheets) > 0,
        'has_macros': len(macro_sheets) > 0,
        'has_transects': len(transect_sheets) > 0,
        'has_cc': len(canopy_sheets) > 0,
        'has_soil': len(soil_sheets) > 0,
        'has_camera': len(ppm_sheets) > 0,
        'has_aqua': len(rip_aqua_sheets) > 0
    })


def count_schools(data):
    schools = []
    num_schools = 0
    for i in data:
        if i['school_id'] not in schools:
            schools.append(i['school_id'])
            num_schools += 1
    return num_schools


def add_school_name(data):
    if len(data) == 0:
        return

    schools = School.objects.filter(active=True)
    data_new = []
    curr_school_id = 0
    for x in data:
        if data.index(x) == 0 or x['school_id'] != curr_school_id:
            school = {'type': 'school', 'name': 'No School Associated'}

            if x['school_id'] != -1:
                school = schools.get(id=x['school_id'])
                school = {'type': 'school', 'name': school.name}

            data_new.append(school)
            curr_school_id = x['school_id']

        data_new.append(x)
    return data_new


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
def update_site(request, site_slug):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    temp = copy.copy(site)

    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True

        if 'lat' in request.POST and 'lng' in request.POST:
            # convert lat/lng to pointfield object
            point = ("SRID=4326;POINT(%s %s)" %
                     (request.POST['lng'], request.POST['lat']))
            request.POST['location'] = point

        if 'checkbox' in request.POST:
            site.image = None

        site_form = SiteForm(request.POST, request.FILES, instance=site)
        if site_form.is_valid():
            site = site_form.save(commit=False)

            if (site.site_name != temp.site_name or
                    site.description != temp.description or
                    site.location != temp.location or
                    site.image != temp.image):
                site.save()

            messages.success(request, _('You have successfully updated ') +
                             site.site_name + '.')
            return redirect(reverse('streamwebs:site',
                                    kwargs={'site_slug': site.site_slug}))

    else:
        site_form = SiteForm(initial={'site_name': site.site_name,
                                      'description': site.description,
                                      'location': site.location,
                                      'image': site.image})

    return render(request, 'streamwebs/update_site.html', {
        'site': site,
        'site_form': site_form,
        'map_type': settings.GOOGLE_MAPS_TYPE,
        'latitude': site.location.y,
        'longitude': site.location.x,

    })


def deactivate_site(request, site_slug):
    deactivated = False
    site = Site.objects.filter(active=True).get(site_slug=site_slug)

    if not(Water_Quality.objects.filter(site_id=site.id).exists() or
            Macroinvertebrates.objects.filter(site_id=site.id).exists() or
            RiparianTransect.objects.filter(site_id=site.id).exists() or
            Canopy_Cover.objects.filter(site_id=site.id).exists() or
            CameraPoint.objects.filter(site_id=site.id).exists()):

        site.active = False
        site.modified = timezone.now()
        site.save()
        deactivated = True

    return render(request, 'streamwebs/deactivate_site.html', {
        'site': site,
        'modified_time': site.modified,
        'deactivated': deactivated
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


@login_required
def account(request):
    user = request.user
    user = User.objects.get(username=user)
    return render(request, 'streamwebs/account.html', {
                  'user': user})


@login_required
def update_email(request):
    user = request.user
    temp = copy.copy(user)
    if request.method == 'POST':
        user_email_form = UserEmailForm(request.POST, instance=user)
        if user_email_form.is_valid():
            if user.email != temp.email:
                user = user_email_form.save(commit=False)
                user.save()
                messages.success(request, 'You have successfully updated' +
                                 ' your email.')
            return redirect(reverse('streamwebs:account'))

    else:
        user_email_form = UserEmailForm(initial={'email': user.email})

    return render(request, 'streamwebs/update_email.html', {
        'user_form': user_email_form,
    })


@login_required
def update_password(request):
    old_password_incorrect = False
    if request.method == 'POST':
        username = request.user
        old_password = request.POST['old_password']
        password = request.POST['password']

        user_password_form = UserPasswordForm(request.POST, instance=username)
        user = authenticate(username=username, password=old_password)

        if user:
            if user_password_form.is_valid():
                user = User.objects.get(username=user)
                user.set_password(password)
                user.save()
                messages.success(request, 'You have successfully updated' +
                                 ' your password.')

                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(reverse('streamwebs:account'))

        else:
            old_password_incorrect = True
    else:
        user_password_form = UserPasswordForm()

    return render(request, 'streamwebs/update_password.html', {
        'user_form': user_password_form,
        'old_password_incorrect': old_password_incorrect
    })


def user_login(request):
    redirect_to = request.POST.get('next', '')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # if the user is valid, log them in and redirect to the page where they
        # clicked "Login", or to home if they accessed login directly from the
        # url
        if user:
            login(request, user)
            if redirect_to != '':
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect(reverse('streamwebs:index'))

        # otherwise, if the user is invalid, flash a message and return them to
        # login while remembering which page to redirect them to if they login
        # successfully this time
        else:
            messages.error(request, _('Invalid username or password.'))
            return redirect(reverse(
                                'streamwebs:login') + '?next=' + redirect_to)

    else:
        return render(request, 'streamwebs/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def graph_water(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    wq_data = Water_Quality.objects.filter(site=site)
    data = [m.to_dict() for m in wq_data]
    site_list = Site.objects.filter(active=True)

    for single_site in site_list:
        wq_sheets = Water_Quality.objects.filter(site_id=single_site.id)
        if len(list(wq_sheets)) == 0:
            site_list = site_list.exclude(site_slug=single_site.site_slug)

    for x in data:
        x['school'] = str(x['school'])
    return render(request, 'streamwebs/graphs/water_quality.html', {
        'data': json.dumps(data),
        'site': site,
        'site_js': json.dumps(site.to_dict()),
        'sites': site_list
    })


def water_graph_site_data(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    wq_data = Water_Quality.objects.filter(site=site)
    data = [m.to_dict() for m in wq_data]
    for x in data:
        x['school'] = str(x['school'])
    return HttpResponse(json.dumps({
        'data': data,
        'site': site.to_dict()
    }), content_type='application/json')


def water_histogram(request, site_slug, data_type, date):
    site = Site.objects.get(site_slug=site_slug)
    day = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    wq_data = Water_Quality.objects.filter(site=site)
    data = [m.to_dict() for m in wq_data if m.date_time.date() == day]
    if data_type == 'pH':
        data_name = data_type
    elif data_type == 'bod':
        data_name = 'BOD'
    else:
        data_name = data_type.replace('_', ' ').title()
    for x in data:
        x['school'] = str(x['school'])
    return render(request, 'streamwebs/graphs/wq_histogram.html', {
        'site': site.to_dict(),
        'data': json.dumps(data),
        'type_key': data_type,
        'type_name': data_name,
        'date': day
    })


def graph_macros(request, site_slug):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
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


def macroinvertebrate(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    data = Macroinvertebrates.objects.get(id=data_id)

    if data.wq_rating > 22:
        rating = "Excellent"
    elif data.wq_rating >= 17 and data.wq_rating <= 22:
        rating = "Good"
    elif data.wq_rating >= 11 and data.wq_rating <= 16:
        rating = "Fair"
    else:
        rating = "Poor"

    counts = data.get_totals()
    bug_count = (counts['Tolerant'] + counts['Somewhat Sensitive'] +
                 counts['Sensitive'])

    # thwart divide-by-0 error
    if bug_count == 0:
        EPT = 0

    # The EPT is the proportion of caddisflies, mayflies, and stoneflies found
    else:
        EPT = 100 * (float(data.caddisfly + data.mayfly + data.stonefly) /
                     float(bug_count))

    return render(
        request,
        'streamwebs/datasheets/macroinvertebrate_view.html', {
            'data': data, 'site': site, 'rating': rating, 'EPT': EPT,
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def macroinvertebrate_edit(request, site_slug):
    """
    The view for the submission of a new macroinvertebrate data sheet.
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    added = False
    macro_form = MacroinvertebratesForm()

    # the following are the form's fields broken up into chunks to
    # facilitate CSS manipulation in the template
    intolerant = list(macro_form)[8:14]
    somewhat = list(macro_form)[14:23]
    tolerant = list(macro_form)[23:29]

    if request.method == 'POST':
        macro_form = MacroinvertebratesForm(data=request.POST)
        if macro_form.is_valid():
            macro = macro_form.save(commit=False)
            macro.date_time = toDateTime(
                macro_form.data['date'],
                macro_form.data['time'],
                macro_form.data['ampm']
            )
            macro.site = site
            macro.school = school
            macro.save()
            added = True
            messages.success(
                request,
                _('You have successfully added a new macroinvertebrates ') +
                'data sheet.')
            return redirect(reverse('streamwebs:macroinvertebrate_view',
                            kwargs={'site_slug': site.site_slug,
                                    'data_id': macro.id}))

    return render(
        request, 'streamwebs/datasheets/macroinvertebrate_edit.html', {
            'macro_form': macro_form,
            'intolerant': intolerant,
            'somewhat': somewhat,
            'tolerant': tolerant,
            'added': added,
            'site': site,
            'school': school
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def riparian_aquatic_edit(request, site_slug):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    rip_aqua_form = RipAquaForm()

    if request.method == 'POST':
        rip_aqua_form = RipAquaForm(data=request.POST)
        if rip_aqua_form.is_valid():
            rip_aqua = rip_aqua_form.save(commit=False)
            rip_aqua.date_time = toDateTime(
                rip_aqua_form.data['date'],
                rip_aqua_form.data['time'],
                rip_aqua_form.data['ampm']
            )
            rip_aqua.site = site
            rip_aqua.school = school
            rip_aqua.save()
            messages.success(
                request,
                _('You have successfully added a Riparian Aquatic Survey.'))
            return redirect(reverse('streamwebs:rip_aqua_view',
                            kwargs={'site_slug': site.site_slug,
                                    'data_id': rip_aqua.id}))

    return render(
        request, 'streamwebs/datasheets/rip_aqua_edit.html', {
            'rip_aqua_form': rip_aqua_form,
            'site': site,
            'school': school
        }
    )


def riparian_aquatic_view(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    data = RipAquaticSurvey.objects.get(id=data_id)

    return render(
        request,
        'streamwebs/datasheets/rip_aqua_view.html', {
            'data': data, 'site': site
            }
        )


def riparian_transect_view(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    transect = RiparianTransect.objects.get(id=data_id)
    zones = TransectZone.objects.filter(transect_id=transect)\
        .order_by('zone_num')

    # Invoking the database by evaluating the queryset before passing it to the
    # template is necessary in order to pass Travis tests.
    # https://docs.djangoproject.com/en/1.9/ref/models/querysets/#when-querysets-are-evaluated
    zones = list(zones)
    zones_json = list()
    for i in zones:
        zone = dict()
        if i.conifers:
            zone['conifers'] = i.conifers
        else:
            zone['conifers'] = 0
        if i.hardwoods:
            zone['hardwoods'] = i.hardwoods
        else:
            zone['hardwoods'] = 0
        if i.shrubs:
            zone['shrubs'] = i.shrubs
        else:
            zone['shrubs'] = 0
        zones_json.append(zone)

    return render(
        request, 'streamwebs/datasheets/riparian_transect_view.html', {
            'transect': transect,
            'zones': zones,
            'zones_json': json.dumps(zones_json),
            'site': site
            }
        )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def riparian_transect_edit(request, site_slug):
    """
    The view for the submission of a new riparian transect data sheet.
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    transect = RiparianTransect()
    TransectZoneInlineFormSet = inlineformset_factory(
        RiparianTransect, TransectZone, form=TransectZoneForm,
        extra=5,
        formset=BaseZoneInlineFormSet
    )

    if request.method == 'POST':
        # process the zone formset
        zone_formset = TransectZoneInlineFormSet(
            data=request.POST, instance=transect
        )
        # process the transect form
        transect_form = RiparianTransectForm(data=request.POST)

        # if both the zone formset and the transect form have "valid" data,
        if (zone_formset.is_valid() and transect_form.is_valid()):
            zones = zone_formset.save(commit=False)     # save forms to objs
            transect = transect_form.save()             # save form to object
            transect.date_time = toDateTime(
                transect_form.data['date'],
                transect_form.data['time'],
                transect_form.data['ampm']
            )
            transect.site = site
            transect.school = school
            transect.save()                             # save object

            for index, zone in enumerate(zones):        # for each zone,
                zone.transect = transect                # assign the transect
                zone.zone_num = index + 1               # save the zone obj
                zone.save()

            messages.success(
                request,
                _('You have successfully added a new riparian transect ') +
                'data sheet.')

            return redirect(reverse('streamwebs:riparian_transect',
                                    kwargs={'site_slug': site.site_slug,
                                            'data_id': transect.id}))

    else:
        zone_formset = TransectZoneInlineFormSet(instance=transect)
        transect_form = RiparianTransectForm()

    return render(
        request,
        'streamwebs/datasheets/riparian_transect_edit.html', {
            'transect_form': transect_form, 'zone_formset': zone_formset,
            'site': site,
            'school': school
        }
    )


def canopy_cover_view(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    canopy_cover = Canopy_Cover.objects.filter(site_id=site.id).get(id=data_id)

    return render(
        request, 'streamwebs/datasheets/canopy_cover_view.html', {
            'canopy_cover': canopy_cover,
            'site': site
            }
        )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def canopy_cover_edit(request, site_slug):
    """
    The view for the submission of a new canopy cover data sheet.
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    canopy_cover = Canopy_Cover()
    error = False

    if request.method == 'POST':
        canopy_cover_form = Canopy_Cover_Form(data=request.POST)

        if (canopy_cover_form.is_valid()):
            canopy_cover = canopy_cover_form.save()
            canopy_cover.date_time = toDateTime(
                canopy_cover_form.data['date'],
                canopy_cover_form.data['time'],
                canopy_cover_form.data['ampm']
            )
            canopy_cover.site = site
            canopy_cover.school = school
            canopy_cover.save()
            messages.success(
                request,
                _('You have successfully added a new canopy cover ') +
                'data sheet.')

            return redirect(reverse('streamwebs:canopy_cover',
                                    kwargs={'site_slug': site.site_slug,
                                            'data_id': canopy_cover.id}))
        else:
            error = True

    else:
        canopy_cover_form = Canopy_Cover_Form()

    return render(
        request,
        'streamwebs/datasheets/canopy_cover_edit.html', {
            'canopy_cover_form': canopy_cover_form,
            'site': site,
            'school': school,
            'error': error
        }
    )


def site_camera(request, site_slug):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    cp = CameraPoint.objects.filter(site_id=site.id)

    return render(
        request,
        'streamwebs/site_camera.html', {
            'site': site,
            'cp': cp,
        }
    )


def camera_point_view(request, site_slug, cp_id):
    """View a site's CP: includes all of its PPs/PPIs"""
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    cp = CameraPoint.objects.get(id=cp_id)
    pps = PhotoPoint.objects.filter(camera_point_id=cp)
    all_images = dict()

    for pp in pps:
        pp_images = PhotoPointImage.objects.filter(photo_point_id=pp.id)
        all_images[pp.number] = pp_images

    return render(
        request, 'streamwebs/datasheets/camera_point_view.html', {
            'site': site,
            'cp': cp,
            'pps': pps,
            'pp_images': all_images
        }
    )


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
def add_camera_point(request, site_slug):
    """Add new CP to site + 3 PPs and respective photos"""
    site = Site.objects.get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    camera = CameraPoint()

    PhotoPointInlineFormset = inlineformset_factory(  # photo point formset (3)
        CameraPoint, PhotoPoint,
        form=PhotoPointForm,
        extra=1, max_num=1, min_num=1                 # three PPs per CP
    )
    PPImageModelFormset = modelformset_factory(       # pp image formset (3)
        PhotoPointImage,
        form=PhotoPointImageForm,
        extra=1, max_num=1, min_num=1                 # one PPI for each PP
    )

    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
        # check if lat and lng came in, if not, set it to 0
        if 'lat' not in request.POST and 'lng' not in request.POST:
            request.POST['lat'] = 0
            request.POST['lng'] = 0

        # convert lat and longs into a pointfield object
        point = ("SRID=4326;POINT(%s %s)" %
                 (request.POST['lat'], request.POST['lng']))
        # spoof the location and  request param with the point object
        # and proceed like normal.
        request.POST['location'] = point
        request.POST['site'] = site.id

        camera_form = CameraPointForm(request.POST)
        # camera_form.location = point

        pp_formset = PhotoPointInlineFormset(request.POST, instance=camera)
        ppi_formset = PPImageModelFormset(
            request.POST, request.FILES,
            queryset=PhotoPointImage.objects.none()
        )
        
        if (camera_form.is_valid() and pp_formset.is_valid() and
                ppi_formset.is_valid()):
            camera = camera_form.save()
            camera.school = school
            camera.save()

            photo_points = pp_formset.save(commit=False)
            pp_images = ppi_formset.save(commit=False)

            for (pp, ppi) in zip(photo_points, pp_images):
                pp.camera_point = camera
                # Since there is no pp_date on the form, use the parent's
                # camera point date
                pp.pp_date = camera.cp_date
                pp.save()

                ppi = PhotoPointImage(photo_point=pp, image=ppi.image,
                                      date=ppi.date)
                ppi.save()

            messages.success(
                request,
                _('You have successfully added a new camera point.'))

            return redirect(reverse('streamwebs:camera_point',
                                    kwargs={'site_slug': site.site_slug,
                                            'cp_id': camera.id}))
    else:
        camera_form = CameraPointForm()
        pp_formset = PhotoPointInlineFormset(instance=camera)
        ppi_formset = PPImageModelFormset(
            queryset=PhotoPointImage.objects.none()
        )

    return render(
        request,
        'streamwebs/datasheets/camera_point_add.html', {
            'camera_form': camera_form,
            'pp_formset': pp_formset,
            'ppi_formset': ppi_formset,
            'site': site,
            'school': school
        }
    )


def view_pp_and_add_img(request, site_slug, cp_id, pp_id):
    """View a specific photopoint and add photos while you're at it"""
    added = False
    pp = PhotoPoint.objects.get(id=pp_id)
    site = Site.objects.get(site_slug=site_slug)
    cp = CameraPoint.objects.get(id=cp_id)

    PPImageModelFormset = modelformset_factory(
        PhotoPointImage,
        form=PhotoPointImageForm,
        extra=1, max_num=1, min_num=1
    )

    if request.method == 'POST':
        ppi_formset = PPImageModelFormset(
            request.POST, request.FILES,
            queryset=PhotoPointImage.objects.none()
        )
        if ppi_formset.is_valid():
            new_images = ppi_formset.save(commit=False)
            prev_images = PhotoPointImage.objects.filter(photo_point_id=pp_id)

            for (new_ppi, old_ppi) in zip(new_images, prev_images):
                if old_ppi.date != new_ppi.date:
                    new_ppi = PhotoPointImage(
                        photo_point=pp, image=new_ppi.image, date=new_ppi.date)
                    new_ppi.save()
                    added = True

                else:
                    messages.add_message(
                        request, messages.INFO,
                        _('A photo from that date already exists for this photo \
                        point.'),
                    )
    else:
        ppi_formset = PPImageModelFormset(
            queryset=PhotoPointImage.objects.none()
        )

    all_images = PhotoPointImage.objects.filter(photo_point_id=pp_id)

    return render(
        request,
        'streamwebs/datasheets/photo_point_view.html', {
            'site': site,
            'cp': cp,
            'pp': pp,
            'ppi_formset': ppi_formset,
            'pp_images': all_images,
            'added': added,
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def add_photo_point(request, site_slug, cp_id):
    """Add new PP to existing CP + respective photo(s)"""
    site = Site.objects.get(site_slug=site_slug)
    #school = UserProfile.objects.filter(user=request.user).first().school
    cp = CameraPoint.objects.get(id=cp_id)
    photo_point = PhotoPoint()
    photo_point.camera_point = cp

    PPImageInlineFormset = inlineformset_factory(
        PhotoPoint, PhotoPointImage,
        form=PhotoPointImageForm,
        extra=1, max_num=1, min_num=1
    )

    if request.method == 'POST':
        pp_form = PhotoPointForm(request.POST)
        ppi_formset = PPImageInlineFormset(request.POST, request.FILES,
                                           instance=photo_point)
        if pp_form.is_valid() and ppi_formset.is_valid():
            photo_point = pp_form.save(commit=False)
            photo_point.camera_point = cp
            # use parent camera point date
            photo_point.pp_date = cp.cp_date
            photo_point.save()

            pp_images = ppi_formset.save(commit=False)

            for ppi in pp_images:
                ppi.photo_point = photo_point
                ppi.save()

            messages.success(
                request,
                _('You have successfully added a new camera point.'))

            return redirect(reverse('streamwebs:photo_point',
                                    kwargs={'site_slug': site.site_slug,
                                            'cp_id': cp.id,
                                            'pp_id': photo_point.id}))

    else:
        pp_form = PhotoPointForm()
        ppi_formset = PPImageInlineFormset(instance=photo_point)

    return render(
        request,
        'streamwebs/datasheets/photo_point_add.html', {
            'site': site,
            'cp': cp,
            'pp_form': pp_form,
            'ppi_formset': ppi_formset,
        }
    )


def water_quality(request, site_slug, data_id):
    """ View a water quality sample """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    wq_data = Water_Quality.objects.get(id=data_id)
    wq_samples = WQ_Sample.objects.filter(water_quality=data_id)\
        .order_by('sample')

    return render(
        request, 'streamwebs/datasheets/water_quality_view.html',
        {
            'site': site,
            'wq_data': wq_data,
            'wq_samples': wq_samples,
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def water_quality_edit(request, site_slug):
    """ Add a new water quality sample """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    WQInlineFormSet = inlineformset_factory(
        Water_Quality, WQ_Sample,
        form=WQSampleForm,
        can_delete=False,
        max_num=4, min_num=4,
        extra=4      # always return exactly 4 samples
    )

    if request.method == 'POST':
        sample_formset = WQInlineFormSet(
            data=request.POST, instance=Water_Quality()
        )
        wq_form = WQForm(data=request.POST)
        if (sample_formset.is_valid() and wq_form.is_valid()):
            water_quality = wq_form.save()   # save form to object
            water_quality.date_time = toDateTime(
                wq_form.data['date'],
                wq_form.data['time'],
                wq_form.data['ampm']
            )
            water_quality.site = site
            water_quality.school = school
            water_quality.save()             # save object to db
            allSamples = sample_formset.save(commit=False)
            counter = 0
            for sample in allSamples:
                sample.water_quality = water_quality
                counter = counter + 1
                sample.sample = counter
                sample.save()
            messages.success(
                request,
                _('You have successfully added a new water quality ') +
                'data sheet.')
            return redirect(reverse('streamwebs:water_quality',
                            kwargs={'site_slug': site.site_slug,
                                    'data_id': water_quality.id}))

    else:
        # blank forms for normal page render
        wq_form = WQForm()
        sample_formset = WQInlineFormSet(instance=Water_Quality())
    return render(
        request, 'streamwebs/datasheets/water_quality_edit.html',
        {
            'site': site,
            'wq_form': wq_form,
            'sample_formset': sample_formset,
            'school': school
        }
    )


def soil_survey(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    soil_data = Soil_Survey.objects.get(id=data_id)
    school = soil_data.school

    return render(
        request, 'streamwebs/datasheets/soil_view.html', {
            'soil_data': soil_data, 'site': site, 'school': school
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
def soil_survey_edit(request, site_slug):
    """
    The view for the submistion of a new Soil Survey (data sheet)
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    school = UserProfile.objects.filter(user=request.user).first().school
    soil_form = SoilSurveyForm()

    if request.method == 'POST':
        soil_form = SoilSurveyForm(data=request.POST)

        if soil_form.is_valid():
            soil = soil_form.save(commit=False)
            soil.date_time = toDateTime(
                soil_form.data['date'],
                soil_form.data['time'],
                soil_form.data['ampm']
            )
            soil.site = site
            soil.school = school
            soil.save()
            messages.success(
                request,
                _('You have successfully submitted a new soil survey.')
            )
            return redirect(reverse('streamwebs:soil',
                            kwargs={'site_slug': site.site_slug,
                                    'data_id': soil.id}))

    return render(
        request, 'streamwebs/datasheets/soil_edit.html', {
            'soil_form': soil_form,
            'site': site,
            'school': school
        }
    )


@login_required
@permission_required('streamwebs.is_super_admin', raise_exception=True)
def admin_site_statistics(request):
    """
    The view for viewing site statistics (admin only)
    """
    stats_form = StatisticsForm()
    default = True

    # A user is defined as "active" if they have logged in w/in the last 3 yrs
    today = datetime.date.today()
    user_start = datetime.date(today.year - 3, today.month, today.day)
    start = datetime.date(1970, 1, 1)
    end = today

    if request.method == 'POST':
        stats_form = StatisticsForm(data=request.POST)

        if stats_form.is_valid():
            # At least one date provided:
            if (stats_form.cleaned_data['start'] is not None or
                    stats_form.cleaned_data['end'] is not None):
                default = False
                # start date provided:
                if stats_form.cleaned_data['start'] is not None:
                    start = stats_form.cleaned_data['start']
                # end date provided:
                if stats_form.cleaned_data['end'] is not None:
                    end = stats_form.cleaned_data['end']

                users = User.objects.filter(date_joined__range=(start, end))
            else:
                users = User.objects.filter(
                    last_login__range=(user_start, end))

    # no form submission: default view displays "all time" total stats
    else:
        users = User.objects.filter(last_login__range=(user_start, end))

    num_soil = Soil_Survey.objects.filter(
        date_time__range=(start, end)).count()
    num_transect = RiparianTransect.objects.filter(
        date_time__range=(start, end)).count()
    num_camera = CameraPoint.objects.filter(
        cp_date__range=(start, end)).count()
    num_macro = Macroinvertebrates.objects.filter(
        date_time__range=(start, end)).count()
    num_canopy = Canopy_Cover.objects.filter(
        date_time__range=(start, end)).count()
    num_water = Water_Quality.objects.filter(
        date_time__range=(start, end)).count()
    total = (num_soil + num_transect + num_camera + num_macro + num_canopy +
             num_water)

    soil_sites = set(Site.objects.filter(
        soil_survey__date_time__range=(start, end)))
    transect_sites = set(Site.objects.filter(
        ripariantransect__date_time__range=(start, end)))
    camera_sites = set(Site.objects.filter(
        camerapoint__cp_date__range=(start, end)))
    macro_sites = set(Site.objects.filter(
        macroinvertebrates__date_time__range=(start, end)))
    canopy_sites = set(Site.objects.filter(
        canopy_cover__date_time__range=(start, end)))
    water_sites = set(Site.objects.filter(
        water_quality__date_time__range=(start, end)))
    all_sites = (soil_sites | transect_sites | camera_sites | macro_sites |
                 canopy_sites | water_sites)

    soil_sch = set(School.objects.filter(
        soil_survey__date_time__range=(start, end)))
    # transect_sch = set(School.objects.filter(
    #     ripariantransect__date_time__range=(start, end)))
    # camera_sch = set(School.objects.filter(
    #     camerapoint__cp_date__range=(start, end)))
    # macro_sch = set(School.objects.filter(
    #     macroinvertebrates__date_time__range=(start, end)))
    canopy_sch = set(School.objects.filter(
        canopy_cover__date_time__range=(start, end)))
    water_sch = set(School.objects.filter(
        water_quality__date_time__range=(start, end)))
    # all_schools = (soil_sch | transect_sch | camera_sch | macro_sch |
    #                canopy_sch | water_sch)
    all_schools = soil_sch | canopy_sch | water_sch

    return render(request, 'streamwebs/admin/stats.html', {
        'stats_form': stats_form,
        'all_time': default,
        'users': {'count': users.count(), 'users': users},
        'user_start': user_start,
        'sheets': {'total': total, 'soil': num_soil, 'transect': num_transect,
                   'camera': num_camera, 'macro': num_macro,
                   'canopy': num_canopy, 'water': num_water},
        'sites': {'total': len(all_sites), 'sites': all_sites},
        'schools': {'total': len(all_schools), 'schools': all_schools},
        'start': start,
        'end': end,
        }
    )


def resources(request):
    return render(request, 'streamwebs/resources.html')


def resources_data_sheets(request):
    """ View for data_sheet resources """
    data = Resource.objects.filter(res_type='data_sheet').order_by(
        'sort_order', 'name'
    )
    return render(
        request, 'streamwebs/resources/resources_data_sheets.html', {
            'data': data,
        }
    )


def resources_publications(request):
    """ View for publication resources """
    data = Resource.objects.filter(res_type='publication').order_by(
        'sort_order', 'name'
        )

    return render(
        request, 'streamwebs/resources/resources_publications.html', {
            'data': data,
        }
    )


def resources_tutorial_videos(request):
    """ View for publication resources """
    data = Resource.objects.filter(res_type='tutorial_video').order_by(
        'sort_order', 'name'
        )

    return render(
        request, 'streamwebs/resources/resources_tutorial_videos.html', {
            'data': data,
        }
    )


@login_required
@permission_required('streamwebs.is_super_admin', raise_exception=True)
def resources_upload(request):
    """ View for uploading a new resource """
    res_form = ResourceForm()

    if request.method == 'POST':
        res_form = ResourceForm(request.POST, request.FILES)
        if res_form.is_valid():
            # if tutorial_video selected
            if res_form.cleaned_data['res_type'] == 'tutorial_video':
                # check that the file extension is of an acceptable type
                m = str(request.FILES["downloadable"])
                # if it is, publish to the video page
                if m.lower().endswith(('.mp4', '.ogg', '.webm')):
                    res = res_form.save()
                    res.save()
                    messages.success(
                        request,
                        _('Tutorial video successfully uploaded')
                    )
                    return redirect(reverse(
                        'streamwebs:resources-tutorial_videos'))
                else:
                    # otherwise, tell the admin that the video is no good
                    messages.error(
                        request,
                        _('Sorry, that video type is unacceptable.')
                        + _('Please upload a .mp4, .webm, or .ogg')
                    )
                    return redirect(reverse(
                        'streamwebs:resources-tutorial_videos'))
            elif res_form.cleaned_data['res_type'] == 'data_sheet':
                res = res_form.save()
                res.save()
                messages.success(
                    request,
                    _('Data sheet successfully uploaded a new data sheet.')
                )
                return redirect(reverse('streamwebs:resources-data-sheets'))
            elif res_form.cleaned_data['res_type'] == 'publication':
                res = res_form.save()
                res.save()
                messages.success(
                    request,
                    _('Publication successfully uploaded.')
                )
                return redirect(reverse('streamwebs:resources-publications'))
    return render(
        request, 'streamwebs/resources/resources_upload.html', {
            'res_form': res_form,
        }
    )


@login_required
@permission_required('streamwebs.is_super_admin', raise_exception=True)
def admin_user_promotion(request):
    admins = Group.objects.get(name='admin')
    admin_perms = Permission.objects.filter(group=admins)
    can_view_stats = Permission.objects.get(codename='can_view_stats')
    can_upload_resources = Permission.objects.get(
        codename='can_upload_resources')
    msgs = []    # list to hold custom flash messages

    promo_form = AdminPromotionForm()

    if request.method == 'POST':
        promo_form = AdminPromotionForm(request.POST)

        if promo_form.is_valid():
            action = promo_form.cleaned_data['perms']
            selected_users = promo_form.cleaned_data['users']

            for user in selected_users:
                if action == 'add_admin':
                    user.groups.add(admins)
                    msgs.append(
                        _('%s added to the Admin group.' % user.username))

                elif action == 'del_admin':
                    user.groups.remove(admins)
                    msgs.append(
                        _('%s removed from the Admin group.' % user.username))

                elif action == 'add_stats':
                    user.user_permissions.add(can_view_stats)
                    msgs.append(
                        _('%s granted permission to view Statistics.'
                          % user.username))

                elif action == 'del_stats':
                    # if they're an admin,
                    if user.groups.filter(name='admin').exists():
                        # remove them from the admins group
                        user.groups.remove(admins)
                        # add back all perms admins enjoy, EXCLUDING stats
                        admin_perms = Permission.objects.filter(group=admins)
                        for perm in admin_perms:
                            if perm.codename != 'can_view_stats':
                                user.user_permissions.add(perm)
                    # otherwise if they're a regular user,
                    else:
                        user.user_permissions.remove(can_view_stats)

                    msgs.append(
                        _('%s was revoked the permission to view Statistics.'
                          % user.username))

                elif action == 'add_upload':
                    user.user_permissions.add(can_upload_resources)
                    msgs.append(
                        _('%s was granted permission to upload resources.'
                          % user.username))

                elif action == 'del_upload':
                    if user.groups.filter(name='admin').exists():
                        user.groups.remove(admins)
                        for perm in admin_perms:
                            if perm.codename != 'can_upload_resources':
                                user.user_permissions.add(perm)
                    else:
                        user.user_permissions.remove(can_upload_resources)

                    msgs.append(
                        _('%s was revoked the permission to upload resources.'
                          % user.username))

    all_users = User.objects.all()
    user_info = dict()
    for u in all_users:
        user_info[u] = {
            'is staff': u.is_staff,
            'is an admin': u.groups.filter(name='admin').exists(),
            'can view stats': u.has_perm('streamwebs.can_view_stats'),
            'can upload resources': u.has_perm(
                'streamwebs.can_upload_resources'),
            'can manage other users': u.has_perm(
                'streamwebs.can_promote_users')}

    paginator = Paginator(list(all_users), 10)  # Show 10 users per page
    page = request.GET.get('page')

    try:
        page_of_users = paginator.page(page)
    except PageNotAnInteger:
        page_of_users = paginator.page(1)
    except EmptyPage:
        page_of_users = paginator.page(paginator.num_pages)

    return render(
        request, 'streamwebs/admin/user_promo.html', {
            'promo_form': promo_form,
            'page_of_users': page_of_users,
            'msgs': msgs,
            'all_users': all_users,
            'user_info': user_info,
        }
    )


def schools(request):
    return render(request, 'streamwebs/schools.html', {
        'schools': School.objects.all().order_by('name')
    })


def school_detail(request, school_id):
    school_data = School.objects.get(id=school_id)
    wq_data = Water_Quality.objects.filter(school=school_id)
    mac_data = Macroinvertebrates.objects.filter(school=school_id)
    can_data = Canopy_Cover.objects.filter(school=school_id)
    soil_data = Soil_Survey.objects.filter(school=school_id)
    rip_data = RiparianTransect.objects.filter(school=school_id)
    rip_aqua_data = RipAquaticSurvey.objects.filter(school=school_id)

    return render(request, 'streamwebs/school_detail.html', {
        'school_data': school_data,
        'school_id': school_id,
        'wq_data': wq_data,
        'mac_data': mac_data,
        'can_data': can_data,
        'soil_data': soil_data,
        'rip_data': rip_data,
        'rip_aqua_data': rip_aqua_data,
    })


# Decorator function that requires the user to be a part of the
# same school as the page they are attempting to access.
def organization_required(func):
    def wrapper(request, school_id):
        school_data = School.objects.get(id=school_id)

        if not request.user.has_perm('streamwebs.is_super_admin'):
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.school != school_data:
                return HttpResponseForbidden('Your account is not associated with this school.')

        return func(request, school_id)
    return wrapper


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
@organization_required
def manage_accounts(request, school_id):
    school_data = School.objects.get(id=school_id)

    org_contributor = Group.objects.get(name='org_author')
    org_editor = Group.objects.get(name='org_admin')

    if request.method == 'POST':
        # Check which submit button was clicked

        # Apply new user settings
        if 'btn_apply' in request.POST:
            editors = request.POST.getlist('nu_editor')
            contributors = request.POST.getlist('nu_contributor')
            denyUsers = request.POST.getlist('nu_deny')
            
            for i in editors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile != None:
                    user.groups.add(org_editor)
                    user.save()

                    profile.approved = True
                    profile.save()
            
            for i in contributors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile != None:
                    user.groups.add(org_contributor)
                    user.save()

                    profile.approved = True
                    profile.save()

            for i in denyUsers:
                profile = UserProfile.objects.get(user=User.objects.get(id=i))
                if profile != None:
                    profile.delete()
        # Delete Selected Editors
        elif 'btn_delete_editors' in request.POST:
            editors = request.POST.getlist('editors')

            for i in editors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile != None:
                    profile.delete()
        # Demote Editor
        elif 'btn_demote' in request.POST:
            editors = request.POST.getlist('editors')

            for i in editors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile != None:
                    user.groups.remove(org_editor)
                    user.groups.add(org_contributor)
                    user.save()
        # Delete Selected Contributors
        elif 'btn_delete_contributors' in request.POST: 
            contributors = request.POST.getlist('contributors')

            for i in contributors:
                profile = UserProfile.objects.get(user=User.objects.get(id=i))
                if profile != None:
                    profile.delete()
        # Promote Contributor
        elif 'btn_promote' in request.POST:
            contributors = request.POST.getlist('contributors')

            for i in contributors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile != None:
                    user.groups.remove(org_contributor)
                    user.groups.add(org_editor)
                    user.save()

    # GET method
    new_users = UserProfile.objects.filter(school=school_data, approved=False).all()
    current_users = UserProfile.objects.filter(school=school_data, approved=True).all()

    contributor_users = [up for up in current_users if up.user.groups.filter(name='org_author').exists()]
    editor_users  = [up for up in current_users if up.user.groups.filter(name='org_admin').exists()]
    
    return render(request, 'streamwebs/manage_accounts.html', {
        'school_data': school_data,
        'school_id': school_id,
        'new_users': new_users,
        'contributor_users': contributor_users,
        'editor_users': editor_users
    })


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
@organization_required
def add_account(request, school_id):
    school_data = School.objects.get(id=school_id)

    if request.method == 'POST':
        user_form = UserFormOptionalFields(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            org_contributor, created = Group.objects.get_or_create(name='org_author')
            user.groups.add(org_contributor)
            #user.is_active = True
            user.save()

            profile = UserProfile()
            profile.birthdate = '1970-01-01' #TODO: Remove when birthday is removed from DB
            profile.school_id = school_id
            profile.user = user
            profile.approved = True # User accounts are made by editors at this level, and are always approved
            profile.save()

            #messages.success(request, _('You have successfully added a new account'))
            return HttpResponseRedirect('/schools/%i/manage_accounts/' % school_data.id)
    else:
        user_form = UserFormOptionalFields()

    return render(request, 'streamwebs/add_account.html', {
        'school_data': school_data,
        'user_form': user_form
    })