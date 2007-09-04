%define	version 1.4.1
%define	release %mkrel 2
%define	major 1
%define libname	%mklibname pri %{major}

Summary:	An implementation of Primate and Basic Rate ISDN
Name:		libpri
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.asterisk.org/
Source0:	http://ftp.digium.com/pub/libpri/%{name}-%{version}.tar.bz2
Patch0:		libpri-1.2.3-mdv_conf.diff
#BuildConflicts:	libpri-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
libpri is a C implementation of the Primary Rate ISDN
specification. It was based on the Bellcore specification
SR-NWT-002343 for National ISDN. As of May 12, 2001, it has been
tested work with NI-2, Nortel DMS-100, and Lucent 5E Custom
protocols on switches from Nortel and Lucent.

%package -n	%{libname}
Summary:	An implementation of Primate and Basic Rate ISDN
Group:          System/Libraries

%description -n	%{libname}
libpri is a C implementation of the Primary Rate ISDN
specification. It was based on the Bellcore specification
SR-NWT-002343 for National ISDN. As of May 12, 2001, it has been
tested work with NI-2, Nortel DMS-100, and Lucent 5E Custom
protocols on switches from Nortel and Lucent.

%package -n	%{libname}-devel
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Provides:	pri-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
libpri is an implementation of the Primary Rate ISDN specification
(based on the ITU and Bellcore specifications). It supports Lucent
4e and 5e, Nortel DMS-100, and National ISDN switchtypes. 

This package contains all of the development files that you will
need in order to compile %{name} applications.

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

%patch0 -p0 -b .mdk

# lib64 fix
find -name "Makefile" | xargs perl -pi -e 's|\$\(INSTALL_BASE\)/lib|\$\(INSTALL_BASE\)/%{_lib}|g'

%build

%make RPM_OPT_FLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT"
#%%make RPM_OPT_FLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT" pridump pritest testprilib

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}

make \
    INSTALL_PREFIX="%{buildroot}" \
    install

ln -snf libpri.so.%{major}.0 %{buildroot}%{_libdir}/libpri.so.%{major}
ln -snf libpri.so.%{major}.0 %{buildroot}%{_libdir}/libpri.so

#install -m0755 pridump %{buildroot}%{_sbindir}/
#install -m0755 pritest %{buildroot}%{_sbindir}/
#install -m0755 testprilib %{buildroot}%{_sbindir}/

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#%files utils
#%defattr(-,root,root)
#%{_sbindir}/pridump
#%{_sbindir}/pritest
#%{_sbindir}/testprilib

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog README TODO
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a


