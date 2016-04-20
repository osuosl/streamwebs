FROM centos:latest
RUN yum -y update

RUN yum -y install epel-release
RUN yum -y groupinstall "Development Tools"
RUN yum -y install gdal-python\
                   geos-python\
                   proj\
                   proj-nad\
                   postgresql-devel\
                   python-pip\
                   python34\
                   python-devel

COPY ./requirements.txt /opt/requirements.txt

RUN pip install -r /opt/requirements.txt
