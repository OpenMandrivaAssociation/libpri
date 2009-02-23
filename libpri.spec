%define	major 1
%define libname %mklibname pri %{major}
%define develname %mklibname pri -d

Summary:	An implementation of Primate and Basic Rate ISDN
Name:		libpri
Version:	1.4.9
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www.asterisk.org/
Source0:	http://ftp.digium.com/pub/libpri/%{name}-%{version}.tar.gz
Patch0:		libpri-mdv_conf.diff
Patch1:		libpri-1.4.8-dahdi_fix.diff
BuildConflicts:	libpri-devel
BuildRequires:	dahdi-devel
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
%patch1 -p1

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


%changelog
* Fri Feb 23 2009 Gergely Lonyai <aleph@mandriva.org> 1.4.9-1mdv2009.1
- 1.4.9

* Wed Dec 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.8-1mdv2009.1
+ Revision: 312532
- 1.4.8
- rediffed P0

* Wed Aug 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.7-1mdv2009.0
+ Revision: 264215
- 1.4.7

* Mon Aug 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-2mdv2009.0
+ Revision: 263016
- rebuild

* Sat Aug 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-1mdv2009.0
+ Revision: 260711
- 1.4.5

* Thu Jun 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-2mdv2009.0
+ Revision: 226557
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-1mdv2009.0
+ Revision: 207168
- fix deps
- 1.4.4
- rediff P0
- re-introduce some of the pri tools

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Dec 15 2007 Stefan van der Eijk <stefan@mandriva.org> 1.4.3-1mdv2008.1
+ Revision: 120329
- 1.4.3

* Thu Oct 18 2007 Stefan van der Eijk <stefan@mandriva.org> 1.4.2-1mdv2008.1
+ Revision: 99929
- 1.4.2

* Tue Sep 04 2007 David Walluck <walluck@mandriva.org> 1.4.1-2mdv2008.0
+ Revision: 79137
- provide pri-devel, and do not provide liblibpri-devel

* Tue Jul 10 2007 Stefan van der Eijk <stefan@mandriva.org> 1.4.1-1mdv2008.0
+ Revision: 50817
- 1.4.1


* Sun Dec 24 2006 Stefan van der Eijk <stefan@mandriva.org> 1.4.0-1mdv2007.0
+ Revision: 101976
- 1.4.0

* Fri Oct 20 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.1.beta1mdv2007.1
+ Revision: 71208
- Import libpri

* Sat Oct 07 2006 Stefan van der Eijk <stefan@mandriva.org> 1.4.0-0.1.beta1
- 1.4.0-beta1

* Thu Jun 01 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-1mdv2007.0
- 1.2.3
- rediffed P0

* Wed Mar 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-3mdk
- drop the bristuff patch, use visdn instead as it is less intrusive
- rediffed P0

* Sun Feb 19 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-2mdk
- bristuff-0.3.0-PRE-1l
- rediffed P0

* Sat Feb 04 2006 Stefan van der Eijk <stefan@eijk.nu> 1.2.2-1mdk
- 1.2.2
- update bristuff to 0.3.0-PRE-1k
- rediffed patch1

* Mon Dec 26 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.1-2mdk
- update bristuff to 0.3.0-PRE-1d and enable

* Mon Dec 12 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.1-1mdk
- 1.2.1
- update bristuff to 0.3.0-PRE-1c, but don't enable

* Sun Nov 20 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-1mdk
- 1.2.0
- drop insane dep names

* Sat Nov 12 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-0.rc2.1mdk
- 1.2.0-rc2

* Wed Nov 09 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-0.rc1.1mdk
- 1.2.0-rc1

* Fri Nov 04 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-0.beta2.1mdk
- 1.2.0-beta2

* Thu Oct 20 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-0.beta1.1mdk
- 1.2.0-beta1
- disable patch1 for now

* Sat Sep 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1-0.20050529.2mdk
- rebuild
- use sane deps names

* Thu Jun 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1-20050529.1mdk
- use a more appropriate version because this is really HEAD and not 1.0.8

* Wed Jun 01 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.20050529.1mdk
- new snap (20050529)
- rediff P0
- bristuff-0.2.0-RC8f-CVS (P1)
- the utils won't compile, deactivate it for now

* Fri May 06 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.20050420.4mdk
- rebuilt with gcc4

* Fri Apr 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.20050420.3mdk
- bristuff-0.2.0-RC8a-CVS (P1)
- mention the bristuff version in the description

* Thu Apr 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.20050420.2mdk
- don't short circuit

* Thu Apr 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.20050420.1mdk
- use a recent snap
- update P0 to bristuff-0.2.0-RC8-CVS
- added the utils sub package

* Sat Apr 23 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-2mdk
- update P0 to bristuff-0.2.0-RC8

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.7-1mdk
- 1.0.7

* Sun Mar 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.6-1mdk
- 1.0.6
- use the %%mkrel macro
- update P0 to bristuff-0.2.0-RC7k

* Sun Feb 06 2005 Stefan van der Eijk <stefan@eijk.nu> 1.0.4-1mdk
- New release 1.0.4
- rpmlint fix: requires-on-release

* Sun Dec 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.3-2mdk
- lib64 fix

* Wed Nov 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.3-1mdk
- 1.0.3
- bristuff-0.2.0-RC3 (P0)

* Wed Nov 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2-3mdk
- bristuff-0.2.0-rc2a (P0)

* Mon Nov 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2-2mdk
- bristuff-0.2.0-rc2 (P0)

* Thu Oct 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2-1mdk
- 1.0.2
- reorder patches
- added P0
- bristuff-0.2.0-rc1 (P2)

* Mon Sep 27 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.0-2mdk
- added P1 by Klaus-Peter Junghanns

* Sat Sep 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.0-1mdk
- 1.0.0
- fix url

* Sat Sep 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-0.RC2.1mdk
- 1.0 RC2
- fix P0

