%define perseussdr_group perseususb
%define major 0
%define libname %mklibname perseus-sd %{major}
%define devname %mklibname -d perseus-sdr

Name:           libperseus-sdr
Version:        0.8.2
Release:        1%{?dist}
Summary:        Perseus Software Defined Radio Control Library
License:        GPL-3.0-only
Group:          Productivity/Hamradio/Other
URL:            https://github.com/Microtelecom/libperseus-sdr
#Git-Clone:     https://github.com/Microtelecom/libperseus-sdr.git
Source:         https://github.com/Microtelecom/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  git-core
BuildRequires:  libtool
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(udev)
Requires:       udev

%description
Perseus Software Defined Radio Control Library.

%package -n	%{libname}
Summary:        Perseus Software Defined Radio Control Library
Group:          System/Libraries


%description -n	%{libname}
Libraries for applications that want to
make use of libperseus-sdr.

%package -n	%{devname}
Summary:        Development files for libperseus-sdr
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{EVRD}

%description -n	%{devname}
Libraries and header files for developing applications that want to
make use of libperseus-sdr.

%package tools
Summary:        Tools for Perseus SDR
Group:          Hardware/Other

%description tools
Tools for Perseus SDR devices.

%package doc
Summary:        Documentation for Perseus SDR

%description doc
Documentation for Perseus SDR

%prep
%autosetup -p1

sed -i 's!UNKNOWNx!%{version}!g' build-aux/git-version-gen
#
%build
# Do not optimize for current cpu
sed -i "s|-march=native||g" configure.ac
autoreconf -iv
%configure
%make_build 

%install
%make_install
find %{buildroot} -type f \( -name '*.a' -o -name '*.la' \) -delete -print
install -Dm0644 95-perseus.rules %{buildroot}%{_udevrulesdir}/95-perseus.rules
cp %{_builddir}/%{name}-%{version}/*.h %{buildroot}/%{_includedir}
rm %{buildroot}/%{_bindir}/*

%pre tools
getent group %{perseussdr_group} >/dev/null || groupadd -r %{perseussdr_group}

%files -n %{libname}
%{_libdir}/libperseus-sdr.so.%{major}*

%files tools
%{_udevrulesdir}/95-perseus.rules

%files -n %{devname}
%license COPYING.LESSER
%{_libdir}/pkgconfig/libperseus-sdr.pc
%{_libdir}/libperseus-sdr.so
%{_includedir}/perseus-sdr.h
%{_includedir}/perseus-in.h
%{_includedir}/perseus-sdr.h
%{_includedir}/perseusfx2.h
%{_includedir}/config.h
%{_includedir}/fpga_data.h

%files doc
%doc AUTHORS README.md
