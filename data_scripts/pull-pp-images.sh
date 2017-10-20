#!/bin/bash
mkdir -p ../media/pp_photos
cd ../media/pp_photos
wget -q -O- http://drupal.streamwebs.org/photo_point_image_files/csv | wget -nc -q -i-
echo "Photo Point Images pulled from drupal site."
