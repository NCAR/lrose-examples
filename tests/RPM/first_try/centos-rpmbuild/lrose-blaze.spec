%define _topdir     /tmp/bj
%define name        lrose 
%define release     20180516
%define version     blaze 
%define buildroot %{_topdir}/%{name}-%{version}-%{release}-root
 
BuildRoot:      %{_topdir}/installedhere
Summary:        LROSE
License:        BSD LICENSE
Name:           %{name}
Version:        %{version}
Release:        %{release}
Source:         %{name}-%{version}-%{release}.src.tgz
Prefix:         /usr/local/lrose
Group:          Scientific Tools
 
%description
LROSE - Lidar Radar Open Software Environment
 
%prep
%setup -q -n lrose-blaze-20180516.src
 
%build
./build_src_release.py
rm -f %{_topdir}/SPECS/lrose-pkg-files
find /usr/local/lrose -type d > %{_topdir}/SPECS/lrose-pkg-files
find /usr/local/lrose -type l >> %{_topdir}/SPECS/lrose-pkg-files

%install
mkdir -p %{buildroot}/usr/local/lrose
rsync -ra /usr/local/lrose %{buildroot}/usr/local

%files -f %{_topdir}/SPECS/lrose-pkg-files
