FROM centos

ADD . /tmp/bj
WORKDIR /tmp/bj

#
RUN yum -y install gcc
RUN yum -y install gcc-gfortran
RUN yum -y install jasper
RUN yum -y install libpng
RUN yum -y install qt
RUN yum -y install fftw3
RUN yum -y install qt5-qtbase
RUN dbus-uuidgen > /etc/machine-id

RUN yum -y install xorg-x11-server-Xorg xorg-x11-xauth xorg-x11-apps

