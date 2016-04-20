FROM centos:latest
RUN yum -y update

RUN yum -y install epel-release
RUN yum -y groupinstall "Development Tools"
RUN yum -y install python-pip python34 postgresql-devel python-devel  

COPY ./requirements.txt /opt/requirements.txt

RUN pip install -r /opt/requirements.txt
