%define	major 1
%define libname %mklibname pri %{major}
%define develname %mklibname pri -d

Summary:	An implementation of Primate and Basic Rate ISDN
Name:		libpri
Version:	1.4.7
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www.asterisk.org/
Source0:	http://ftp.digium.com/pub/libpri/%{name}-%{version}.tar.gz
Patch0:		libpri-mdv_conf.diff
BuildConflicts:	libpri-devel
BuildRequires:	tonezone-devel
BuildRequires:	zapata-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libpri is a C implementation of the Primary Rate ISDN specification. It was
based on the Bellcore specification SR-NWT-002343 for National ISDN. As of May
12, 2001, it has been tested work with NI-2, Nortel DMS-100, and Lucent 5E
Custom protocols on switches from Nortel and Lucent.

%package -n	%{libname}
Summary:	An implementation of Primate and Basic Rate ISDN
Group:          System/Libraries

%description -n	%{libname}
libpri is a C implementation of the Primary Rate ISDN specification. It was
based on the Bellcore specification SR-NWT-002343 for National ISDN. As of May
12, 2001, it has been tested work with NI-2, Nortel DMS-100, and Lucent 5E
Custom protocols on switches from Nortel and Lucent.

%package -n	%{develname}
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Provides:	pri-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname pri -d 1}

%description -n	%{develname}
libpri is an implementation of the Primary Rate ISDN specification (based on
the ITU and Bellcore specifications). It supports Lucent 4e and 5e, Nortel
DMS-100, and National ISDN switchtypes.

This package contains all of the development files that you will need in order
to compile %{name} applications.

%package	utils
Summary:	Various tools for %{name} diagnostics
Group:		System/Libraries

%description	utils
Various tools for %{name} diagnostics

%prep

%setup -q

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p0

# lib64 fix
find -name "Makefile" | xargs perl -pi -e 's|\$\(INSTALL_BASE\)/lib|\$\(INSTALL_BASE\)/%{_lib}|g'

%build

%make RPM_OPT_FLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT"
%make RPM_OPT_FLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT" pridump pritest

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}

make \
    INSTALL_PREFIX="%{buildroot}" \
    install

install -m0755 pridump %{buildroot}%{_sbindir}/
install -m0755 pritest %{buildroot}%{_sbindir}/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files utils
%defattr(-,root,root)
%{_sbindir}/pridump
%{_sbindir}/pritest

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog README TODO
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
