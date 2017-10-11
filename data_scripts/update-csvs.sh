set -x
curl http://streamwebs.org/site_lat_long/csv > sites.csv
curl http://streamwebs.org/schools/csv > schools_info.csv
# This requires being logged into the site to pull down all of the data
# curl http://streamwebs.org/active_users/csv > users.csv
curl http://streamwebs.org/macro_ds/csv > macros.csv
mkdir -p wq_csvs
curl http://streamwebs.org/water_quality/csv > wq_csvs/water_quality.csv
curl http://streamwebs.org/wq_water_temp/csv > wq_csvs/WQ_water_temp.csv
curl http://streamwebs.org/wq_air_temp/csv > wq_csvs/WQ_air_temp.csv
curl http://streamwebs.org/wq_oxygen/csv > wq_csvs/WQ_oxygen.csv
curl http://streamwebs.org/wq_pH/csv > wq_csvs/WQ_pH.csv
curl http://streamwebs.org/wq_turvbidity/csv > wq_csvs/WQ_turbidity.csv
curl http://streamwebs.org/wq_salt/csv > wq_csvs/WQ_salinity.csv
curl http://streamwebs.org/wq_conductivity/csv > wq_csvs/WQ_conductivity.csv
curl http://streamwebs.org/wq_total_solids/csv > wq_csvs/WQ_total_solids.csv
curl http://streamwebs.org/wq_bod/csv > wq_csvs/WQ_bod.csv
curl http://streamwebs.org/wq_ammonia/csv > wq_csvs/WQ_ammonia.csv
curl http://streamwebs.org/wq_nitrite/csv > wq_csvs/WQ_nitrite.csv
curl http://streamwebs.org/wq_nitrate/csv > wq_csvs/WQ_nitrate.csv
curl http://streamwebs.org/wq_phosphates/csv > wq_csvs/WQ_phosphates.csv
curl http://streamwebs.org/wq_fecal_col/csv > wq_csvs/WQ_fecal_col.csv
curl http://streamwebs.org/wq_sample_tools/csv > wq_csvs/WQ_sample_tools.csv
curl http://streamwebs.org/transect/csv > rip_transect.csv
curl http://streamwebs.org/zones/csv > transect_zones.csv
curl http://streamwebs.org/cc_north/csv > cc_north.csv
curl http://streamwebs.org/cc_east/csv > cc_east.csv
curl http://streamwebs.org/cc_south/csv > cc_south.csv
curl http://streamwebs.org/cc_west/csv > cc_west.csv
curl http://streamwebs.org/soil_survey/csv > soil_survey.csv
curl http://streamwebs.org/active_schools_new/csv > active_schools.csv

sed -i '2s;^;"0","Unknown School","Elementary","2009-02-03 14:16","2009-02-03 14:16","1234 Unknown Street","Corvallis","Oregon","97330","United States"\n;' schools_info.csv
