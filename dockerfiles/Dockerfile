FROM osuosl/django-centos:latest
RUN yum -y update

RUN yum -y install gdal-python\
                   geos-python\
                   proj\
                   proj-nad\
                   postgresql-devel\

COPY ./requirements.txt /opt/requirements.txt

RUN pip install -r /opt/requirements.txt
