# coding=UTF-8

from django.shortcuts import render
from django.http import HttpResponse


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
