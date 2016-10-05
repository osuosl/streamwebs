# coding=UTF-8
from __future__ import print_function
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.conf import settings

from streamwebs.forms import (
    UserForm, UserProfileForm, RiparianTransectForm, MacroinvertebratesForm,
    Canopy_Cover_Form, WQSampleForm, WQSampleFormReadOnly, WQForm,
    WQFormReadOnly, SiteForm, Resource_Data_Sheet_Form,
    Resource_Publication_Form, Resource_Video_Tutorial_Form)
from streamwebs.models import (
    Macroinvertebrates, Site, Water_Quality, WQ_Sample, RiparianTransect,
    TransectZone, Canopy_Cover, CC_Cardinal, Resource)

from datetime import datetime
import json
import copy


def _timestamp(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()


def index(request):
    return render(request, 'streamwebs/index.html', {})


def create_site(request):
    created = False

    if request.method == 'POST':
        site_form = SiteForm(request.POST, request.FILES)

        if site_form.is_valid():
            site = site_form.save()
            site.save()
            created = True
            messages.success(request,
                             'You have successfully added a new site.')
            return redirect(reverse('streamwebs:site',
                            kwargs={'site_slug': site.site_slug}))

    else:
        site_form = SiteForm()

    return render(request, 'streamwebs/create_site.html', {
        'site_form': site_form, 'created': created})


def sites(request):
    """ View for streamwebs/sites """
    site_list = Site.objects.filter(active=True)
    return render(request, 'streamwebs/sites.html', {
        'sites': site_list,
        'maps_api': settings.GOOGLE_MAPS_API
    })


# view-view for individual specified site
def site(request, site_slug):
    """ View an individual site """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    wq_sheets = Water_Quality.objects.filter(site_id=site.id).order_by('-date')
    macro_sheets = Macroinvertebrates.objects.filter(site_id=site.id)
    macro_sheets = macro_sheets.order_by('-date_time')
    transect_sheets = RiparianTransect.objects.filter(site_id=site.id)
    transect_sheets = transect_sheets.order_by('-date_time')
    canopy_sheets = Canopy_Cover.objects.filter(site_id=site.id)
    canopy_sheets = canopy_sheets.order_by('-date_time')

    return render(request, 'streamwebs/site_detail.html', {
        'site': site,
        'wq_sheets': wq_sheets,
        'macro_sheets': macro_sheets,
        'transect_sheets': transect_sheets,
        'canopy_sheets': canopy_sheets,
    })


def update_site(request, site_slug):
    updated = False
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    temp = copy.copy(site)

    if request.method == 'POST':
        site_form = SiteForm(request.POST, request.FILES, instance=site)

        if site_form.is_valid():
            if (site.site_name != temp.site_name or
                    site.description != temp.description or
                    site.location != temp.location or
                    site.image != temp.image):
                site = site_form.save(commit=False)
                site.modified = timezone.now()
                site.save()

            updated = True

    else:
        site_form = SiteForm(initial={'site_name': site.site_name,
                                      'description': site.description,
                                      'location': site.location,
                                      'image': site.image})

    return render(request, 'streamwebs/update_site.html', {
        'site': site,
        'site_form': site_form,
        'modified_time': site.modified,
        'updated': updated
    })


def deactivate_site(request, site_slug):
    deactivated = False
    site = Site.objects.filter(active=True).get(site_slug=site_slug)

    if not(Water_Quality.objects.filter(site_id=site.id).exists() or
            Macroinvertebrates.objects.filter(site_id=site.id).exists() or
            RiparianTransect.objects.filter(site_id=site.id).exists() or
            Canopy_Cover.objects.filter(site_id=site.id).exists()):

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
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
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


def resources(request):
    return render(request, 'streamwebs/resources.html')


def resources_data_sheets(request):
    """ View for data_sheet resources """
    data = Resource.objects.filter(res_type='data_sheet').order_by(
        'sort_order', 'name'
    )
    resource_form = Resource_Data_Sheet_Form()
    added = False

    if request.method == 'POST':
        resource_form = Resource_Data_Sheet_Form(request.POST, request.FILES)
        if resource_form.is_valid():
            resource_form.save()
            added = True
        else:
            print(resource_form.errors)

    return render(
        request, 'streamwebs/resources_data_sheets.html', {
            'added': added,
            'data': data,
            'resource_form': resource_form
        }
    )


def resources_publications(request):
    """ View for publication resources """
    data = Resource.objects.filter(res_type='publication').order_by(
        'sort_order', 'name'
    )
    resource_form = Resource_Publication_Form()
    added = False

    if request.method == 'POST':
        resource_form = Resource_Publication_Form(request.POST, request.FILES)
        if resource_form.is_valid():
            resource_form.save()
            added = True
        else:
            print(resource_form.errors)

    return render(
        request, 'streamwebs/resources_publications.html', {
            'added': added,
            'data': data,
            'resource_form': resource_form
        }
    )


def resources_tutorials(request):
    """ View for video tutorial resources """
    data = Resource.objects.filter(res_type='video-tutorial').order_by(
        'sort_order', 'name'
    )
    resource_form = Resource_Video_Tutorial_Form()
    resource_form.res_type = 'Tutorial Video'
    added = False

    if request.method == 'POST':
        resource_form = Resource_Video_Tutorial_Form(
            request.POST, request.FILES
        )
        if resource_form.is_valid():
            resource_form.save()
            added = True
        else:
            print(resource_form.errors)

    return render(
        request, 'streamwebs/resources_tutorial_videos.html', {
            'added': added,
            'data': data,
            'resource_form': resource_form
        }
    )


def riparian_transect_view(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
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
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
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


def canopy_cover_view(request, site_slug, data_id):
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    canopy_cover = Canopy_Cover.objects.filter(site_id=site.id).get(id=data_id)
    cardinals = CC_Cardinal.objects.filter(canopy_cover_id=canopy_cover)

    return render(
        request, 'streamwebs/datasheets/canopy_cover_view.html', {
            'canopy_cover': canopy_cover,
            'cardinals': cardinals,
            'site': site
            }
        )


def canopy_cover_edit(request, site_slug):
    """
    The view for the submission of a new canopy cover data sheet.
    """
    added = False
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    canopy_cover = Canopy_Cover()
    CardinalInlineFormSet = inlineformset_factory(
        Canopy_Cover, CC_Cardinal,
        fields=(
            'direction', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
            'X', 'num_shaded'), extra=4
    )

    if request.method == 'POST':
        cardinal_formset = CardinalInlineFormSet(
            data=request.POST, instance=canopy_cover
        )
        canopy_cover_form = Canopy_Cover_Form(data=request.POST)

        if (cardinal_formset.is_valid() and canopy_cover_form.is_valid()):

            canopy_cover = canopy_cover_form.save()
            canopy_cover.save()

            cardinals = cardinal_formset.save(commit=False)

            for cardinal in cardinals:
                cardinal.canopy_cover = canopy_cover
                cardinal.save()

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


def water_quality(request, site_slug, data_id):
    """ View a water quality sample """
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
    wq_form = WQFormReadOnly(instance=Water_Quality.objects.get(id=data_id))

    WQInlineFormSet = modelformset_factory(
        WQ_Sample,
        form=WQSampleFormReadOnly,
        can_delete=False,
        max_num=4, min_num=4,
        extra=4      # always return exactly 4 samples
    )
    sample_formset = WQInlineFormSet(
        queryset=WQ_Sample.objects.filter(water_quality=data_id)
    )

    return render(
        request, 'streamwebs/datasheets/water_quality.html',
        {
            'editable': False,
            'site': site,
            'wq_form': wq_form,
            'sample_formset': sample_formset
        }
    )


def water_quality_edit(request, site_slug):
    """ Add a new water quality sample """
    added = False       # flag for the page to see if we added a sample
    site = Site.objects.filter(active=True).get(site_slug=site_slug)
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
            water_quality.save()             # save object to db
            allSamples = sample_formset.save(commit=False)
            for sample in allSamples:
                sample.water_quality = water_quality
                sample.save()
            added = True
            # ugly way of resetting the form if successful form submission
            wq_form = WQForm()
            sample_formset = WQInlineFormSet(instance=Water_Quality())
    else:
        # blank forms for normal page render
        wq_form = WQForm()
        sample_formset = WQInlineFormSet(instance=Water_Quality())
    return render(
        request, 'streamwebs/datasheets/water_quality.html',
        {
            'editable': True,
            'added': added,
            'site': site,
            'wq_form': wq_form,
            'sample_formset': sample_formset
        }
    )
