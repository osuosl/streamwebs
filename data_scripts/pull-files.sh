#!/bin/bash
DIR=$PWD
mkdir -p ../media/pp_photos
cd ../media/pp_photos
wget -q -O- http://drupal.streamwebs.org/photo_point_image_files/csv | wget -nc -q -i-
echo "Photo Point Images pulled from drupal site."
cd $DIR
mkdir -p ../media/site_photos
cd ../media/site_photos
wget -q -O- http://drupal.streamwebs.org/site_images | wget -nc -q -i-
echo "Site Images pulled from drupal site."
