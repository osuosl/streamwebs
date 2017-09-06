FROM osuosl/django-centos:latest

# Point yum to our mirrors
RUN sed -i -e 's/^\(mirrorlist.*\)/#\1/g' /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/epel.repo
RUN sed -i -e 's/^#baseurl=.*pub\/epel\/7\/$basearch$/baseurl=http\:\/\/epel.osuosl.org\/$releasever\/$basearch\//g' /etc/yum.repos.d/epel.repo
RUN sed -i -e 's/^#baseurl=.*$releasever\/os\/$basearch\//baseurl=http\:\/\/centos.osuosl.org\/$releasever\/os\/$basearch\//g' /etc/yum.repos.d/CentOS-Base.repo
RUN sed -i -e 's/^#baseurl=.*$releasever\/updates\/$basearch\//baseurl=http\:\/\/centos.osuosl.org\/$releasever\/updates\/$basearch\//g' /etc/yum.repos.d/CentOS-Base.repo
RUN sed -i -e 's/^#baseurl=.*$releasever\/addons\/$basearch\//baseurl=http\:\/\/centos.osuosl.org\/$releasever\/addons\/$basearch\//g' /etc/yum.repos.d/CentOS-Base.repo
RUN sed -i -e 's/^#baseurl=.*$releasever\/extras\/$basearch\//baseurl=http\:\/\/centos.osuosl.org\/$releasever\/extras\/$basearch\//g' /etc/yum.repos.d/CentOS-Base.repo
RUN sed -i -e 's/^#baseurl=.*$releasever\/centosplus\/$basearch\//baseurl=http\:\/\/centos.osuosl.org\/$releasever\/centosplus\/$basearch\//g' /etc/yum.repos.d/CentOS-Base.repo
RUN sed -i -e 's/^#baseurl=.*$releasever\/contrib\/$basearch\//baseurl=http\:\/\/centos.osuosl.org\/$releasever\/contrib\/$basearch\//g' /etc/yum.repos.d/CentOS-Base.repo

# Workaround for https://bugs.centos.org/view.php?id=13669&nbn=1
RUN yum -y install https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-devel-2.7.1-3.el7.x86_64.rpm

RUN yum -y install gdal-python\
                   geos-python\
                   proj\
                   proj-nad\
                   postgresql-devel\
                   nodejs\
                   npm\
                   vim\
                   freetype-devel\
                   libjpeg-devel\
                   libpng-devel

RUN npm install -g bower

COPY requirements.txt /home/centos/

RUN pip install --upgrade pip

RUN pip install --upgrade -r /home/centos/requirements.txt

#RUN echo 'source /opt/streamwebs/dockerfiles/startup.sh' >> /root/.bashrc
