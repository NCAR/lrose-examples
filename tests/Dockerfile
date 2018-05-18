FROM centos
# FROM centos:7

ADD . /tmp/bj
WORKDIR /tmp/bj

# VOLUME ["/tmp/thursday"]
#
# is there a way to pull the source release from github?
#
RUN yum -y install rsync
RUN yum -y install gcc 
RUN yum -y install gcc-gfortran
RUN yum -y install gcc-c++
RUN yum -y install make
RUN yum -y install wget
RUN yum -y install expat-devel
RUN yum -y install m4
RUN yum -y install jasper-devel
RUN yum -y install flex-devel
RUN yum -y install zlib-devel
RUN yum -y install libpng-devel
# RUN yum -y install python-devel
RUN yum -y install bzip2-devel
RUN yum -y install qt5-qtbase-devel
RUN yum -y install fftw3-devel
RUN yum install -y xorg-x11-server-Xorg xorg-x11-xauth xorg-x11-apps

RUN yum -y install libX11-devel
# RUN yum -y install libX11-6
# RUN yum -y install freetype6   # for nice fonts in HawkEye

# I installed libtool, but is it necessary??

# RUN ln -s /usr/lib64/libz.so.1 /usr/lib64/libz.so
#   --------


# Check out, build and install netcdf
# See README_NETCDF_BUILD.md

# Install netcdf into the prefix location.

# Prepare build directory
# Create a directory for the distribution:

RUN  cd /tmp/bj
# RUN  cd /tmp/bj; mkdir lrose_build
# RUN  cd lrose_build

# Download source release for Linux
# Download the source tar file from:

# RUN wget -O lrose-release.src.tgz "https://github.com/NCAR/lrose-core/releases/download/lrose-20180430/lrose-20180430.src.tgz"
# or 

# RUN cp /tmp/bj/lrose-blaze-20180516.src.tgz /tmp/bj/lrose_build/.

# ADD  https://github.com/NCAR/lrose-core/releases/lrose-20180430.src.tgz
# A typical source release would be:
#
#  lrose-20160823.src.tgz
# Untar it
#   cd lrose_build
RUN  tar xvfz lrose-blaze-20180516.src.tgz  #  tar xvfz lrose-release.src.tgz
# The distribution will be unpacked into a subdirectory:
RUN cd lrose-blaze-20180516.src; ./build_src_release.py

# create a user
# RUN useradd -ms /bin/bash lrose 
# USER lrose
# WORKDIR /home/lrose

#The default prefix is /usr/local/lrose.

# Verify the installation

# After the build, you can check the build as follows:

#  ./installDir/bin/RadxPrint -h
#  ./installDir/bin/RadxConvert -h

# -----

# RUN cd lrose-20180430.bin.x86_64; ./install_bin_release.py

# CMD  /usr/local/lrose/bin/RadxPrint -h 
#CMD /tmp/bj/run_tests

#
# this is critical to X11 forwarding
#
CMD dbus-uuidgen > /etc/machine-id 

# CMD xclock&
