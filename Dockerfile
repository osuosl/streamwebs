FROM almalinux:8

RUN dnf -y install epel-release
RUN dnf config-manager --set-enabled powertools
RUN dnf -y install proj postgresql postgresql-devel nodejs npm wget \
    freetype-devel libjpeg-devel libpng-devel python2-pip python2-devel gcc git \
    gdal-devel gcc-c++
RUN ln -s /usr/bin/python2 /usr/bin/python

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN npm install -g bower
RUN bower install --allow-root
RUN pip2 install -r requirements.txt
