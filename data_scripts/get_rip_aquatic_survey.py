#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime

from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import RipAquaticSurvey # NOQA


if os.path.isdir("../sw_data/"):
    datapath = '../sw_data/'
else:
    datapath = '../csvs/'

rip_aquatic_survey = datapath + 'rip_aquatic_survey.csv'
ripa_plants_species = datapath + 'ripa_plants_species.csv'
ripa_significance = datapath + 'ripa_plants_significance.csv'
ripa_wildlife_comments = datapath + 'ripa_wildlife_comments.csv'
ripa_wildlife_type = datapath + 'ripa_wildlife_type.csv'

# nid, site, riffle_count, pool_count, collected, silt, sand, gravel, cobble,
# boulders, bedrock, small_debris, medium_debris, large_debris, comments,
# coniferous_trees, deciduous_trees, shrubs, small_plants, ferns, grasses,
# species, significance, wildlife_type, wildlife_comments
with open(rip_aquatic_survey, 'r') as csvfile:
    ripareader = csv.reader(csvfile)
    for row in ripareader:
        significance_reader = csv.DictReader(open(ripa_significance, 'r'))
        species_reader = csv.DictReader(open(ripa_plants_species, 'r'))
        wl_comments_reader = csv.DictReader(open(ripa_wildlife_comments, 'r'))
        wl_type_reader = csv.DictReader(open(ripa_wildlife_type, 'r'))
        if row[0] != 'nid':  # Skip the header

            id = row[0]
            site = Site.objects.get(site_name=row[1])
            if row[2] == '':
                stream_length = 0
            else:
                stream_length = row[2]
            if row[3] == '':
                riffle_count = 0
            else:
                riffle_count = row[3]
            if row[4] == '':
                pool_count = 0
            else:
                pool_count = row[4]
            # Replace any "All day" entrys with 12:00
            dt = row[5].replace('(All day)', '12:00')
            ripa_date = datetime.strptime(dt, "%a, %Y-%m-%d %H:%M")
            silt = row[6]
            sand = row[7]
            gravel = row[8]
            cobble = row[9]
            boulders = row[10]
            bedrock = row[11]
            small_debris = row[12]
            medium_debris = row[13]
            large_debris = row[14]
            comments = row[15]
            coniferous_trees = row[16]
            deciduous_trees = row[17]
            shrubs = row[18]
            small_plants = row[19]
            ferns = row[20]
            grasses = row[21]

            species = []
            significance = []
            wildlife_type = []
            wildlife_comments = []
            for sp_row in species_reader:
                if sp_row['nid'] == id:
                    species.append(sp_row['species'])
            for si_row in significance_reader:
                if si_row['nid'] == id:
                    significance.append(si_row['significance'])
            for wlt_row in wl_type_reader:
                if wlt_row['nid'] == id:
                    wildlife_type.append(wlt_row['wildlife_type'])
            for wlc_row in wl_comments_reader:
                if wlc_row['nid'] == id:
                    wildlife_comments.append(wlc_row['wildlife_comments'])
            try:
                RipAquaticSurvey.objects.filter(id=id).update(
                    site=site, stream_length=stream_length,
                    riffle_count=riffle_count, pool_count=pool_count,
                    date_time=ripa_date, silt=silt, sand=sand, gravel=gravel,
                    cobble=cobble, boulders=boulders, bedrock=bedrock,
                    small_debris=small_debris, medium_debris=medium_debris,
                    large_debris=large_debris, comments=comments,
                    coniferous_trees=coniferous_trees,
                    deciduous_trees=deciduous_trees, shrubs=shrubs,
                    small_plants=small_plants, ferns=ferns, grasses=grasses,
                    species1=species[0], species2=species[1],
                    species3=species[2], species4=species[3],
                    species5=species[4], species6=species[5],
                    significance1=significance[0],
                    significance2=significance[1],
                    significance3=significance[2],
                    significance4=significance[3],
                    significance5=significance[4],
                    significance6=significance[5],
                    wildlife_type1=wildlife_type[0],
                    wildlife_type2=wildlife_type[1],
                    wildlife_type3=wildlife_type[2],
                    wildlife_type4=wildlife_type[3],
                    wildlife_type5=wildlife_type[4],
                    wildlife_type6=wildlife_type[5],
                    wildlife_comments1=wildlife_comments[0],
                    wildlife_comments2=wildlife_comments[1],
                    wildlife_comments3=wildlife_comments[2],
                    wildlife_comments4=wildlife_comments[3],
                    wildlife_comments5=wildlife_comments[4],
                    wildlife_comments6=wildlife_comments[5]
                )
            except ObjectDoesNotExist:
                rip_aquatic_survey = RipAquaticSurvey.objects.update_or_create(
                    id=id, site=site, stream_length=stream_length,
                    riffle_count=riffle_count, pool_count=pool_count,
                    date_time=ripa_date, silt=silt, sand=sand, gravel=gravel,
                    cobble=cobble, boulders=boulders, bedrock=bedrock,
                    small_debris=small_debris, medium_debris=medium_debris,
                    large_debris=large_debris, comments=comments,
                    coniferous_trees=coniferous_trees,
                    deciduous_trees=deciduous_trees, shrubs=shrubs,
                    small_plants=small_plants, ferns=ferns, grasses=grasses,
                    species1=species[0], species2=species[1],
                    species3=species[2], species4=species[3],
                    species5=species[4], species6=species[5],
                    significance1=significance[0],
                    significance2=significance[1],
                    significance3=significance[2],
                    significance4=significance[3],
                    significance5=significance[4],
                    significance6=significance[5],
                    wildlife_type1=wildlife_type[0],
                    wildlife_type2=wildlife_type[1],
                    wildlife_type3=wildlife_type[2],
                    wildlife_type4=wildlife_type[3],
                    wildlife_type5=wildlife_type[4],
                    wildlife_type6=wildlife_type[5],
                    wildlife_comments1=wildlife_comments[0],
                    wildlife_comments2=wildlife_comments[1],
                    wildlife_comments3=wildlife_comments[2],
                    wildlife_comments4=wildlife_comments[3],
                    wildlife_comments5=wildlife_comments[4],
                    wildlife_comments6=wildlife_comments[5]
                )


print "Riparian Aquatic Surveys loaded."
