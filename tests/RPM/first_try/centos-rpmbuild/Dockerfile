#
# start with an image that contains all the packages needed to 
# build lrose-blaze + rpmbuilder
#
FROM centos-rpmbuilder
 
# make the spec file available to the container
#
ADD . /tmp/rpm_files

RUN yum -y install git
RUN yum -y install libtool

# create user rpmbuilder
#RUN useradd -ms /bin/bash rpmbuilder 
#USER rpmbuilder
#WORKDIR /home/rpmbuilder

# build hierarchy for rpmbuild:
RUN cd ~
RUN mkdir BUILD RPMS SOURCES SPECS SRPMS
#
# import the files
#
RUN cp /tmp/rpm_files/lrose-blaze.spec SPECS/lrose-blaze.spec
RUN cp /tmp/bj/lrose-blaze-20180516.src.tgz SOURCES/lrose-blaze-20180516.src.tgz
# 
# RUN cd lrose_blaze/SOURCES
# RUN git clone https://github.com/NCAR/lrose-core
#
# RUN ./build/create_src_release.py --package=lrose-blaze
# RUN mv ~/releases/tmp/lrose-blaze-20180516.src.tgz ~/SOURCES/.
# RUN cd ..
#
RUN rpmbuild -v -bb --define "debug_package %{nil}" SPECS/lrose-blaze.spec
#
# export the package
#
RUN rsync RPMS /tmp/rpm_files/RPMS
