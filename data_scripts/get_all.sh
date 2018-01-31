#!/bin/bash
set -e
# Run all migration scripts in appropriate order
./get_sites.py
./get_site_desc.py
./get_schools.py
./get_users.py
./get_macros.py
./get_wq_basic.py
./get_required_fields.py
./get_additional_wq.py
./set_tools.py
./get_transects.py
./get_cc.py
./get_soil.py
./get_camera_points.py
./get_photo_points.py
./pull-files.sh
# Run twice so that relations are created for renamed schools
./rename_schools.py
./rename_schools.py
./reset_dup_relations.py
./set_schools.py
./get_rip_aquatic_survey.py
./get_photo_point_images.py
./get_site_images.py
./get_gallery_images.py
rm -rf media/
