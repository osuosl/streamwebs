# coding=UTF-8
from __future__ import print_function
from django.http import (
    HttpResponseRedirect, HttpResponse, HttpResponseForbidden)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from streamwebs.forms import (
    UserFormOptionalNameEmail, UserFormEmailAsUsername,
    UserEditForm, UserProfileForm,
    RiparianTransectForm, MacroinvertebratesForm,
    PhotoPointImageForm, PhotoPointForm, CameraPointForm, WQSampleForm,
    WQForm, SiteForm, Canopy_Cover_Form, SoilSurveyForm, StatisticsForm,
    TransectZoneForm, BaseZoneInlineFormSet, ResourceForm, UserEmailForm,
    UserPasswordForm, SchoolForm, RipAquaForm)

from streamwebs.models import (
    Macroinvertebrates, Site, Water_Quality, WQ_Sample, RiparianTransect,
    TransectZone, Canopy_Cover, CameraPoint, PhotoPoint,
    PhotoPointImage, Soil_Survey, Resource, RipAquaticSurvey,
    UserProfile, School)

import json
import copy
import datetime


# Decorator function that requires the user to be part of ANY school
def any_organization_required(func):
    def wrapper(request, *args, **kwargs):
        if UserProfile.objects.filter(user=request.user).exists():
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile is None or user_profile.school is None:
                return HttpResponseForbidden(
                    'Your account is not associated with any school.')
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                'Your account is not associated with any school.')
    return wrapper


# Decorator function that requires the user to be a part of the
# same school as the page they are attempting to access.
def organization_required(func):
    def wrapper(request, *args, **kwargs):
        school_data = School.objects.get(id=kwargs['school_id'])

        if not request.user.has_perm('streamwebs.is_super_admin'):
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile is None:
                return HttpResponseForbidden(
                    'Your account is not associated with any school.')
            if user_profile.school != school_data:
                return HttpResponseForbidden(
                    'Your account is not associated with this school.')
        return func(request, *args, **kwargs)
    return wrapper


# Decorator function that requires the school to be active
def organization_approved(func):
    def wrapper(request, *args, **kwargs):
        school_data = School.objects.get(id=kwargs['school_id'])

        if not school_data.active:
            return HttpResponseRedirect('/schools/%i/' % school_data.id)
        return func(request, *args, **kwargs)
    return wrapper


# Send an email
def send_email(request, subject, template, user, school, from_email,
               recipients):
    send_mail(
        subject=subject,
        message='',
        html_message=render_to_string(
            template,
            {
                'protocol': request.scheme,
                'domain': request.get_host(),
                'user': user,
                'school': school
            }),
        from_email=from_email,
        recipient_list=recipients,
        fail_silently=False,
    )


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


def confirm_registration(request):
    return render(request, 'streamwebs/confirm_register.html', {})


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

    schools = School.objects.all()
    data_new = []
    curr_school_id = 0
    for x in data:
        if data.index(x) == 0 or x['school_id'] != curr_school_id:
            school = {'type': 'school', 'name': 'No School Associated'}

            if schools.filter(id=x['school_id']).exists():
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
    if request.method == 'POST':
        user_form = UserFormEmailAsUsername(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        school_form = SchoolForm(data=request.POST)

        new_org_flag = len(request.POST.getlist('new_org_flag')) > 0

        # User form must always be valid
        if user_form.is_valid():
            if not new_org_flag and profile_form.is_valid():
                user = user_form.save()
                user.username = user.email
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                # Get current system users
                current_users = UserProfile.objects.filter(
                    school=profile.school, approved=True).all()

                # Get editors for new user's school
                editor_users = [up.user.email for up in current_users
                                if up.user.groups.filter(
                                    name='org_admin').exists()]

                # Email to org admins for new user joining org
                if (len(editor_users) > 0):
                    send_email(
                        request=request,
                        subject='New User requested to join your organization',
                        template='registration/new_user_request_email.html',
                        user=user,
                        school=profile.school,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipients=editor_users
                    )

                return HttpResponseRedirect('/register/confirm')
            # Create a school
            elif school_form.is_valid():
                school = school_form.save()
                school.province = (school.province + ', United States')
                school.save()

                user = user_form.save()
                user.username = user.email
                user.set_password(user.password)
                user.save()

                profile = UserProfile()
                profile.user = user
                profile.school_id = school.id
                profile.save()

                # Permissions
                org_editor = Group.objects.get(name='org_admin')
                user.groups.add(org_editor)
                user.save()

                # Super admins
                super_admins = [usr.email for usr in User.objects.all()
                                if usr.has_perm('streamwebs.is_super_admin')]

                # Email to super admin for new organization + account
                send_email(
                    request=request,
                    subject='New organization request: ' + str(school.name),
                    template='registration/new_org_request_email.html',
                    user=user,
                    school=school,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipients=super_admins
                )

                return HttpResponseRedirect('/register/confirm')

    else:
        user_form = UserFormEmailAsUsername()
        profile_form = UserProfileForm()
        school_form = SchoolForm()
        new_org_flag = False

    return render(request, 'streamwebs/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'school_form': school_form,
        'schools': School.objects.filter(active=True).all().order_by('name'),
        'new_org_flag': new_org_flag
    })


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
        email = ''.join(request.POST['email'].split()).lower()
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        # if the user is valid, log them in and redirect to the page where they
        # clicked "Login", or to home if they accessed login directly from the
        # url
        if user:
            if user.has_perm('streamwebs.is_super_admin'):
                login(request, user)
            else:
                user_profile = UserProfile.objects.filter(user=user).first()
                if not user_profile.approved:
                    messages.error(request,
                                   _('Sorry, you have not' +
                                     " been approved by an administrator"))
                    return redirect(reverse(
                                'streamwebs:login') + '?next=' + redirect_to)
                else:
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


def macroinvertebrate_view(request, site_slug, data_id):
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
@any_organization_required
def macroinvertebrate_edit(request, site_slug):
    """
    The view for the submission of a new macroinvertebrate data sheet.
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
    added = False
    macro_form = MacroinvertebratesForm()

    # the following are the form's fields broken up into chunks to
    # facilitate CSS manipulation in the template
    intolerant = list(macro_form)[7:13]
    somewhat = list(macro_form)[13:22]
    tolerant = list(macro_form)[22:28]

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
@any_organization_required
def riparian_aquatic_edit(request, site_slug):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
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
@any_organization_required
def riparian_transect_edit(request, site_slug):
    """
    The view for the submission of a new riparian transect data sheet.
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
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
@any_organization_required
def canopy_cover_edit(request, site_slug):
    """
    The view for the submission of a new canopy cover data sheet.
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
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
            'maps_api': settings.GOOGLE_MAPS_API,
            'map_type': settings.GOOGLE_MAPS_TYPE,
            'site': site,
            'cp': cp,
            'pps': pps,
            'pp_images': all_images
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
@any_organization_required
def add_camera_point(request, site_slug):
    """Add new CP to site + 3 PPs and respective photos"""
    site = Site.objects.get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
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
                 (request.POST['lng'], request.POST['lat']))
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
                        request, messages.ERROR,
                        _('A photo from that date already exists for this photo\
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
    # school = UserProfile.objects.filter(user=request.user).first().school
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

    # initalize variables for calculating averages
    water_temp_sample_count = 0
    water_temp_avg = 0  # worker temp value
    water_temp_avg_fah = None  # in Fahrenheit
    water_temp_avg_cel = None  # in celcius

    air_temp_sample_count = 0
    air_temp_avg = 0  # worker temp value
    air_temp_avg_fah = None  # in Fahrenheit
    air_temp_avg_cel = None  # in celcius

    dissolved_oxygen_sample_count = 0
    dissolved_oxygen_avg = 0

    pH_sample_count = 0
    pH_avg = 0

    turbidity_sample_count = 0
    turbidity_avg = 0

    salinity_sample_count = 0
    salinity_avg = 0

    # Addition for each sample type
    for sample in wq_samples:
        if sample.water_temperature is not None:
            water_temp_sample_count += 1
            water_temp_avg += sample.water_temperature
        if sample.air_temperature is not None:
            air_temp_sample_count += 1
            air_temp_avg += sample.air_temperature
        if sample.dissolved_oxygen:
            dissolved_oxygen_sample_count += 1
            dissolved_oxygen_avg += sample.dissolved_oxygen
        if sample.pH:
            pH_sample_count += 1
            pH_avg += sample.pH
        if sample.turbidity:
            turbidity_sample_count += 1
            turbidity_avg += sample.turbidity
        if sample.salinity:
            salinity_sample_count += 1
            salinity_avg += sample.salinity

    # Now divide by the count if there are any
    if water_temp_sample_count > 0:
        water_temp_avg /= water_temp_sample_count
        water_temp_avg = round(water_temp_avg, 2)
        # Calculate Other temperature unit (celcius or fahrenheit)
        if wq_data.water_temp_unit == Water_Quality.FAHRENHEIT:
            water_temp_avg_fah = water_temp_avg
            water_temp_avg_cel = round((water_temp_avg - 32) * float(5) / 9, 2)
        else:
            water_temp_avg_fah = round((water_temp_avg * (float(9)/5)) + 32, 2)
            water_temp_avg_cel = water_temp_avg

    if air_temp_sample_count > 0:
        air_temp_avg /= air_temp_sample_count
        air_temp_avg = round(air_temp_avg, 2)
        # Calculate Other temperature unit (celcius or fahrenheit)
        if wq_data.air_temp_unit == Water_Quality.FAHRENHEIT:
            air_temp_avg_fah = air_temp_avg
            air_temp_avg_cel = round((air_temp_avg - 32) * float(5) / 9, 2)
        else:
            air_temp_avg_fah = round((air_temp_avg * (float(9) / 5)) + 32, 2)
            air_temp_avg_cel = air_temp_avg

    if dissolved_oxygen_sample_count > 0:
        dissolved_oxygen_avg /= dissolved_oxygen_sample_count
        dissolved_oxygen_avg = round(dissolved_oxygen_avg, 2)

    if pH_sample_count > 0:
        pH_avg /= pH_sample_count
        pH_avg = round(pH_avg, 2)

    if turbidity_sample_count > 0:
        turbidity_avg /= turbidity_sample_count
        turbidity_avg = round(turbidity_avg, 2)

    if salinity_sample_count > 0:
        salinity_avg /= salinity_sample_count
        salinity_avg = round(salinity_avg, 2)

    # Package up averages into a dictionary
    data_averages = {}
    data_averages["water_temp_sample_count"] = water_temp_sample_count
    data_averages["water_temp_avg_fah"] = water_temp_avg_fah
    data_averages["water_temp_avg_cel"] = water_temp_avg_cel
    data_averages["air_temp_sample_count"] = air_temp_sample_count
    data_averages["air_temp_avg_fah"] = air_temp_avg_fah
    data_averages["air_temp_avg_cel"] = air_temp_avg_cel
    data_averages[
        "dissolved_oxygen_sample_count"] = dissolved_oxygen_sample_count
    data_averages["dissolved_oxygen_avg"] = dissolved_oxygen_avg
    data_averages["pH_sample_count"] = pH_sample_count
    data_averages["pH_avg"] = pH_avg
    data_averages["turbidity_sample_count"] = turbidity_sample_count
    data_averages["turbidity_avg"] = turbidity_avg
    data_averages["salinity_sample_count"] = salinity_sample_count
    data_averages["salinity_avg"] = salinity_avg

    return render(
        request, 'streamwebs/datasheets/water_quality_view.html',
        {
            'site': site,
            'wq_data': wq_data,
            'wq_samples': wq_samples,
            'data_averages': data_averages
        }
    )


@login_required
@permission_required('streamwebs.is_org_author', raise_exception=True)
@any_organization_required
def water_quality_edit(request, site_slug):
    """ Add a new water quality sample """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
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
@any_organization_required
def soil_survey_edit(request, site_slug):
    """
    The view for the submistion of a new Soil Survey (data sheet)
    """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    profile = UserProfile.objects.filter(user=request.user).first()

    school = profile.school
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
    user_start = datetime.date(today.year - 3, today.month, today.day + 1)
    start = datetime.date(1970, 1, 1)
    end = today

    if request.method == 'POST':
        stats_form = StatisticsForm(data=request.POST)

        if stats_form.is_valid():
            print(stats_form)
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
                if end == today:
                    sameday = True
                    end += datetime.timedelta(days=1)
                else:
                    sameday = False
                print(today)
                print(end)
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
        'sameday': sameday,
        'today': today
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


def schools(request):
    return render(request, 'streamwebs/schools.html', {
        'schools': School.objects.filter(active=True).all().order_by('name')
    })


def school_detail(request, school_id):
    school_data = School.objects.get(id=school_id)
    is_in_org = False
    if request.user.is_authenticated():
        if request.user.has_perm('streamwebs.is_super_admin'):
            is_in_org = True

        elif request.user.has_perm('streamwebs.is_org_admin'):
            user_profile = UserProfile.objects.filter(
                user=request.user).first()
            if user_profile is not None:
                is_in_org = (user_profile.school.id == school_data.id)
            else:
                is_in_org = False
    else:
        is_in_org = False

    wq_data = Water_Quality.objects.filter(school=school_id)
    mac_data = Macroinvertebrates.objects.filter(school=school_id)
    can_data = Canopy_Cover.objects.filter(school=school_id)
    soil_data = Soil_Survey.objects.filter(school=school_id)
    rip_data = RiparianTransect.objects.filter(school=school_id)
    rip_aqua_data = RipAquaticSurvey.objects.filter(school=school_id)

    return render(request, 'streamwebs/school_detail.html', {
        'school_data': school_data,
        'is_in_org': is_in_org,
        'wq_data': wq_data,
        'mac_data': mac_data,
        'can_data': can_data,
        'soil_data': soil_data,
        'rip_data': rip_data,
        'rip_aqua_data': rip_aqua_data,
    })


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
# Redirect to the manage accounts page, based on user's school
@any_organization_required
def get_manage_accounts(request, user_id):
    profile = UserProfile.objects.get(user=request.user)
    return HttpResponseRedirect(
        '/schools/%i/manage_accounts/' % int(profile.school.id))


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
@organization_required
@organization_approved
def manage_accounts(request, school_id):
    school = School.objects.get(id=school_id)

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
                if profile is not None:
                    user.groups.add(org_editor)
                    user.save()

                    profile.approved = True
                    profile.save()

                    # Email editors that they were approved
                    send_email(
                        request=request,
                        subject='Your editor account was approved at ' +
                                str(school.name),
                        template='registration/' +
                                 'approve_user_request_email.html',
                        user=user,
                        school=school,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipients=[user.email]
                    )

            for i in contributors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile is not None:
                    user.groups.add(org_contributor)
                    user.save()

                    profile.approved = True
                    profile.save()

                    # Email contributors that they were approved
                    send_email(
                        request=request,
                        subject='Your contributor account was approved at ' +
                                str(school.name),
                        template='registration/' +
                                 'approve_user_request_email.html',
                        user=user,
                        school=school,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipients=[user.email]
                    )

            for i in denyUsers:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile is not None:
                    profile.delete()
                    user.delete()

        # Delete Selected Editors
        elif 'btn_delete_editors' in request.POST:
            editors = request.POST.getlist('editors')

            for i in editors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)

                if user.id != request.user.id:
                    if profile is not None:
                        profile.delete()
                    if user is not None:
                        user.delete()

        # Demote Editor
        elif 'btn_demote' in request.POST:
            editors = request.POST.getlist('editors')

            for i in editors:
                user = User.objects.get(id=i)

                if user.id != request.user.id:
                    if user.groups.filter(name=org_editor).exists():
                        user.groups.remove(org_editor)
                    user.groups.add(org_contributor)
                    user.save()

        # Delete Selected Contributors
        elif 'btn_delete_contributors' in request.POST:
            contributors = request.POST.getlist('contributors')

            for i in contributors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)

                if user.id != request.user.id:
                    if profile is not None:
                        profile.delete()
                    if user is not None:
                        user.delete()

        # Promote Contributor
        elif 'btn_promote' in request.POST:
            contributors = request.POST.getlist('contributors')

            for i in contributors:
                user = User.objects.get(id=i)
                profile = UserProfile.objects.get(user=user)
                if profile is not None:
                    if user.groups.filter(name=org_contributor).exists():
                        user.groups.remove(org_contributor)
                    user.groups.add(org_editor)
                    user.save()

    # GET method
    new_users = UserProfile.objects.filter(school=school,
                                           approved=False).all()
    current_users = UserProfile.objects.filter(school=school,
                                               approved=True).all()

    contributor_users = [up for up in current_users
                         if up.user.groups.filter(name='org_author').exists()]
    editor_users = [up for up in current_users
                    if up.user.groups.filter(name='org_admin').exists()]

    return render(request, 'streamwebs/manage_accounts.html', {
        'school_data': school,
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
        user_form = UserFormOptionalNameEmail(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)

            org_contributor = Group.objects.get(name='org_author')
            user.groups.add(org_contributor)
            user.save()

            profile = UserProfile()
            profile.school_id = school_id
            profile.user = user
            profile.approved = True
            profile.save()

            return HttpResponseRedirect('/schools/%i/manage_accounts/'
                                        % school_data.id)
    else:
        user_form = UserFormOptionalNameEmail()

    return render(request, 'streamwebs/add_account.html', {
        'school_data': school_data,
        'user_form': user_form
    })


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
@organization_required
def edit_account(request, school_id, user_id):
    school_data = School.objects.get(id=school_id)
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=user)

        if user_form.is_valid():
            user = user_form.save()

            return HttpResponseRedirect('/schools/%i/manage_accounts/'
                                        % school_data.id)
    else:
        user_form = UserEditForm(instance=user)

    return render(request, 'streamwebs/edit_account.html', {
        'school_data': school_data,
        'user': user,
        'user_form': user_form
    })


@login_required
@permission_required('streamwebs.is_org_admin', raise_exception=True)
def var_debug(request, value):
    return render(request, 'streamwebs/var_debug.html', {
        'value': value
    })


@login_required
@permission_required('streamwebs.is_super_admin', raise_exception=True)
def new_org_request(request, school_id):
    school = School.objects.get(id=school_id)
    profiles = UserProfile.objects.filter(school=school)
    profile = profiles.first()

    if profile is None:
        return HttpResponseForbidden(
            'There is no user associated with this organization request.')

    user = profile.user

    if request.method == 'POST':
        editor_permission = request.POST.getlist('editor_permission')
        contributor_permission = request.POST.getlist('contributor_permission')

        org_contributor = Group.objects.get(name='org_author')
        org_editor = Group.objects.get(name='org_admin')

        # Deny org and user
        if 'btn_deny' in request.POST:
            user.delete()
            profile.delete()
            school.delete()
            # Redirect to home
            return HttpResponseRedirect('/')
        # Approve org
        elif 'btn_approve' in request.POST:
            school.active = True
            profile.approved = True

            # Approved for editor permission
            if len(editor_permission) > 0:
                user.groups.clear()
                user.groups.add(org_editor)
            # Approved for contributor permission
            elif len(contributor_permission) > 0:
                user.groups.clear()
                user.groups.add(org_contributor)

            school.save()
            profile.save()

            # Email
            send_email(
                request=request,
                subject='Your organization was approved: ' + str(school.name),
                template='registration/approve_org_request_email.html',
                user=user,
                school=school,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipients=[user.email]
            )

            return HttpResponseRedirect('/schools/%i/' % school.id)

    return render(request, 'streamwebs/new_org_request.html', {
        'school_data': school,
        'user': user
        })
