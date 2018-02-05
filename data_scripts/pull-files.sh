#!/bin/bash
DIR=$PWD
mkdir -p ../media/pp_photos ../streamwebs_frontend/media/
cd ../media/pp_photos
wget -q -O- http://drupal.streamwebs.org/photo_point_image_files/csv | wget -nc -q -i-
cd ${DIR}
cd ../streamwebs_frontend/media/
ln -sf ../../media/pp_photos/ .
echo "Photo Point Images pulled from drupal site."
cd $DIR
mkdir -p ../media/site_photos
cd ../media/site_photos
wget -q -O- http://drupal.streamwebs.org/site_images | wget -nc -q -i-
cd ${DIR}
cd ../streamwebs_frontend/media/
ln -sf ../../media/site_photos/ .
echo "Site Images pulled from drupal site."
cd $DIR
mkdir -p ../media/gallery_images
cd ../media/gallery_images
wget -q -O- http://drupal.streamwebs.org/gallery_csv/images | wget -nc -q -i-
cd ${DIR}
cd ../streamwebs_frontend/media/
ln -sf ../../media/gallery_images/ .
echo "Gallery Images pulled from drupal site."
cd $DIR
mkdir -p ../media/gallery_files
cd ../media/gallery_files
wget -q -O- http://drupal.streamwebs.org/gallery_csv/files | wget -nc -q -i-
cd ${DIR}
cd ../streamwebs_frontend/media/
ln -sf ../../media/gallery_files/ .
echo "Gallery Files pulled from drupal site."
cd $DIR
mkdir -p ../media/gallery_images
cd ../media/gallery_images
wget -q -O- http://drupal.streamwebs.org/album-urls.csv | wget -nc -q -i-
cd ${DIR}
cd ../streamwebs_frontend/media/
ln -sf ../../media/gallery_images/ .
echo "Gallery Album Images pulled from drupal site."