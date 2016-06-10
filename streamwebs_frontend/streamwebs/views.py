# coding=UTF-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from streamwebs.forms import UserForm, UserProfileForm

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
    return HttpResponse('Viewing page for site %s' % site_slug)


def register(request):
#    context = RequestContext(request)
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
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

#    context.push(
#            {
#                'user_form': user_form,
#                'profile_form': profile_form,
#                'registered': registered
#            }
#    )

#    return render_to_response(
#            'streamwebs/register.html', context)
    return render(request, 'streamwebs/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
#    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/streamwebs/')
        else:
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse('Invalid credentials')
    else:
#        return render_to_response('streamwebs/login.html', {}, context)
        return render(request, 'streamwebs/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/streamwebs/')
