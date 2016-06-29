FROM osuosl/django-centos:latest
RUN yum -y update

RUN yum -y install gdal-python\
                   geos-python\
                   proj\
                   proj-nad\
                   postgresql-devel\
                   nodejs\
                   npm\
                   freetype-devel\
                   libjpeg-devel\
                   libpng-devel
                       
RUN npm install -g bower

COPY requirements.txt /opt/

RUN pip install -r /opt/requirements.txt

#RUN echo 'source /opt/streamwebs/dockerfiles/startup.sh' >> /root/.bashrc
