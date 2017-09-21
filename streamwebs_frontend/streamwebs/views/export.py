# coding=UTF-8
from __future__ import print_function
from django.http import HttpResponse

from streamwebs.models import (
    Macroinvertebrates, Site, Water_Quality, WQ_Sample, RiparianTransect,
    TransectZone, Canopy_Cover, Soil_Survey, RipAquaticSurvey)

from djqscsv import render_to_csv_response
import csv

def export_rip_aqua(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    print(site)
    ripaq = RipAquaticSurvey.objects.filter(site_id=site.id).values(
        'site__site_name', 'school', 'date', 'weather', 'riffle_count', 'pool_count', 'silt',
        'sand', 'gravel', 'cobble', 'boulders', 'bedrock', 'small_debris',
        'medium_debris', 'large_debris', 'comments', 'coniferous_trees',
        'deciduous_trees', 'shrubs', 'small_plants', 'ferns', 'grasses',
        'species', 'significance', 'wildlife_type', 'wildlife_comments'
    )
    return render_to_csv_response(
        ripaq, field_header_map={
            'site__site_name': 'site',
            'date': 'date',
            'school': 'school',
            'weather': 'weather',
            'riffle_count': '# of riffles', 'pool_count': '# of pools',
            'silt': 'silt count',
            'sand': 'sand count',
            'gravel': 'gravel count',
            'cobble': 'cobble count',
            'boulders': 'boulder count',
            'bedrock': 'bedrock count',
            'small_debris': 'small debris',
            'medium_debris': 'medium_debris',
            'large_debris': 'large debris',
            'comments': 'comments',
            'coniferous_trees': '# of coniferous trees',
            'deciduous_trees': '#of deciduous trees',
            'shrubs': '# of shrubs',
            'small_plants': '# of small plants',
            'ferns': '# of ferns',
            'grasses': '# of grasses',
            'species': '# of species',
            'significance': 'significance',
            'wildlife_type': 'wildlife type',
            'wildlife_comments': 'wildlife comments'
            }
        )


def export_wq(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    waterq = Water_Quality.objects.filter(site_id=site.id)

    # Store nid of each wq data sheet into a list
    sheets = []
    for each in waterq:
        sheets.append(each.nid)

    # Query the first set of samples outside of the loop and pop nid from list
    samples = WQ_Sample.objects.prefetch_related('water_quality')
    samples = samples.filter(nid=sheets[0]).order_by('id').values(
        'water_quality__school__name', 'water_quality__date',
        'water_quality__site__site_name', 'water_quality__DEQ_dq_level',
        'water_quality__latitude', 'water_quality__longitude',
        'water_quality__fish_present', 'water_quality__live_fish',
        'water_quality__dead_fish', 'water_quality__water_temp_unit',
        'water_quality__air_temp_unit', 'water_quality__notes', 'sample',
        'water_temperature', 'water_temp_tool', 'air_temperature',
        'air_temp_tool', 'dissolved_oxygen', 'oxygen_tool', 'pH', 'pH_tool',
        'turbidity', 'turbid_tool', 'salinity', 'salt_tool', 'conductivity',
        'total_solids', 'bod', 'ammonia', 'nitrite', 'nitrate', 'phosphates',
        'fecal_coliform'
    )
    sheets.pop(0)

    # Query for the remaining samples according to wq_nid
    for sheet in sheets:
        n_samples = WQ_Sample.objects.prefetch_related('water_quality')
        n_samples = n_samples.filter(nid=sheet).order_by('id').values(
            'water_quality__school__name', 'water_quality__date',
            'water_quality__site__site_name', 'water_quality__DEQ_dq_level',
            'water_quality__latitude', 'water_quality__longitude',
            'water_quality__fish_present', 'water_quality__live_fish',
            'water_quality__dead_fish', 'water_quality__water_temp_unit',
            'water_quality__air_temp_unit', 'water_quality__notes', 'sample',
            'water_temperature', 'water_temp_tool', 'air_temperature',
            'air_temp_tool', 'dissolved_oxygen', 'oxygen_tool', 'pH',
            'pH_tool', 'turbidity', 'turbid_tool', 'salinity', 'salt_tool',
            'conductivity', 'total_solids', 'bod', 'ammonia', 'nitrite',
            'nitrate', 'phosphates', 'fecal_coliform'
        )
        samples = samples | n_samples

    filename = 'water_quality_export'

    return render_to_csv_response(
        samples, filename=filename, field_header_map={
            'water_quality__school__name': 'school',
            'water_quality__date': 'date',
            'water_quality__site__site_name': 'site',
            'water_quality__DEQ_dq_level': 'DEQ Data Quality level',
            'water_quality__latitude': 'latitude',
            'water_quality__longitude': 'longitude',
            'water_quality__fish_present': 'Are fish present?',
            'water_quality__live_fish': '# of live fish',
            'water_quality__dead_fish': '# of dead fish',
            'water_quality__water_temp_unit': 'water temperature unit',
            'water_quality__air_temp_unit': 'air temperature unit',
            'water_quality__notes': 'notes',
            'water_temperature': 'water temperature',
            'water_temp_tool': 'water temperature tool',
            'air_temperature': 'air temperature',
            'air_temp_tool': 'air temperature tool',
            'dissolved_oxygen': 'dissolved oxygen',
            'oxygen_tool': 'oxygen tool', 'pH_tool': 'pH tool',
            'turbid_tool': 'turbidity tool', 'salt_tool': 'salinity tool',
            'total_solids': 'total solids', 'fecal_coliform': 'fecal coliform'
        }
    )


def export_macros(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    macros = Macroinvertebrates.objects.filter(site_id=site.id).values(
        'school', 'date_time', 'site__site_name', 'weather', 'time_spent',
        'num_people', 'water_type', 'notes', 'caddisfly', 'mayfly',
        'riffle_beetle', 'stonefly', 'water_penny', 'dobsonfly',
        'sensitive_total', 'clam_or_mussel', 'crane_fly', 'crayfish',
        'damselfly', 'dragonfly', 'scud', 'fishfly', 'alderfly', 'mite',
        'somewhat_sensitive_total', 'aquatic_worm', 'blackfly', 'leech',
        'midge', 'snail', 'mosquito_larva', 'tolerant_total', 'wq_rating'
    )
    return render_to_csv_response(
        macros, field_header_map={
            'date_time': 'date/time', 'site__site_name': 'site',
            'time_spent': 'time spent sorting',
            'num_people': '# of people sorting', 'water_type': 'water type',
            'riffle_beetle': 'riffle beetle', 'water_penny': 'water penny',
            'sensitive_total': 'sensitive total',
            'clam_or_mussel': 'clam/mussel', 'crane_fly': 'crane fly',
            'somewhat_sensitive_total': 'somewhat sensitive total',
            'aquatic_worm': 'aquatic worm', 'mosquito_larva': 'mosquito larva',
            'tolerant_total': 'tolerant total',
            'wq_rating': 'water quality rating'
        }
    )


# Come back to this to fix schools and foreign key calls
def export_ript(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    rip_transect = RiparianTransect.objects.filter(site_id=site.id)

    sheets = []
    for each in rip_transect:
        sheets.append(each.id)

    zones = TransectZone.objects.filter(transect_id=sheets[0])
    zones = zones.values(
        'transect__school', 'transect__date_time', 'transect__site__site_name',
        'transect__weather', 'transect__slope', 'transect__notes', 'zone_num',
        'conifers', 'hardwoods', 'shrubs', 'comments'
    )
    sheets.pop(0)

    for sheet in sheets:
        n_zones = TransectZone.objects.filter(transect_id=sheet)
        n_zones = n_zones.order_by('transect__id', 'zone_num').values(
            'transect__school', 'transect__date_time',
            'transect__site__site_name', 'transect__weather',
            'transect__slope', 'transect__notes', 'zone_num', 'conifers',
            'hardwoods', 'shrubs', 'comments'
        )
        zones = zones | n_zones

    filename = 'riparian_transect_export'

    return render_to_csv_response(
        zones, filename=filename, field_header_map={
            'transect__school': 'school', 'transect__date_time': 'date/time',
            'transect__site__site_name': 'site',
            'transect__weather': 'weather', 'transect__slope': 'slope',
            'transect__notes': 'notes', 'zone_num': 'zone number'
        }
    )


def export_cc(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    canopyc = Canopy_Cover.objects.filter(site_id=site.id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
                                       filename="canopy_cover_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['school', 'date/time', 'site', 'weather', 'north',
                     'east', 'south', 'west', 'estimated canopy cover'])

    for each in canopyc:
        cc = canopyc.get(id=each.id)

        # Convert int to binary
        north = "{0:b}".format(cc.north_cc)
        east = "{0:b}".format(cc.east_cc)
        south = "{0:b}".format(cc.south_cc)
        west = "{0:b}".format(cc.west_cc)

        # "Count" the number of shaded squares
        n = north.count('1')
        e = east.count('1')
        s = south.count('1')
        w = west.count('1')

        writer.writerow([cc.school, cc.date_time, cc.site.site_name,
                         cc.weather, n, e, s, w, cc.est_canopy_cover])

    return response


def export_soil(request, site_slug):
    site = Site.objects.get(site_slug=site_slug)
    soil = Soil_Survey.objects.filter(site_id=site.id).values(
        'school__name', 'date', 'site__site_name', 'weather', 'landscape_pos',
        'cover_type', 'land_use', 'soil_type', 'distance', 'site_char'
    )
    return render_to_csv_response(
        soil, field_header_map={
            'school__name': 'school', 'site__site_name': 'site',
            'landscape_pos': 'landscape position', 'cover_type': 'cover type',
            'land_use': 'land use', 'distance': 'distance from stream',
            'soil_type': 'soil type', 'site_char': 'site characteristics'
        }
    )
