%define _with_systemd 1

Name:		rtkit
Version:	0.10
Release:	%mkrel 4
Summary:	Realtime Policy and Watchdog Daemon
Group:		System/Libraries
License:	GPLv3+ and BSD
URL:		http://git.0pointer.de/?p=rtkit.git
Source0:	http://0pointer.de/public/%{name}-%{version}.tar.gz
Requires:	polkit >= 0.93
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	cap-devel
BuildRequires:	polkit-1-devel
%if %{_with_systemd}
BuildRequires:	systemd-units
BuildRequires:	libsystemd-daemon-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%setup -q

%build
%configure2_5x \
%if !%{_with_systemd}
	--without-systemdsystemunitdir
%endif

%make
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
rm -rf %{buildroot}
%makeinstall_std
install -D org.freedesktop.RealtimeKit1.xml %{buildroot}/%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd rtkit /proc /sbin/nologin

%postun
%_postun_userdel rtkit

%post
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%doc README rtkit.c rtkit.h
%attr(0755,root,root) %{_sbindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%{_mandir}/man*/rtkitctl.*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
%if %{_with_systemd}
/lib/systemd/system/rtkit-daemon.service
%endif


%changelog
* Sun Jun 19 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.10-1mdv2011.0
+ Revision: 686010
- update to new version 0.10
- drop patch 0
- spec file clean

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9-3
+ Revision: 669454
- mass rebuild

* Fri Feb 11 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 0.9-2
+ Revision: 637240
- fix cap-devel BR
- new version
- enable systemd
- P0: fix systemd unit (GIT)

* Tue Jul 13 2010 Colin Guthrie <cguthrie@mandriva.org> 0.8-1mdv2011.0
+ Revision: 552108
- New version: 0.8

* Sat May 08 2010 Colin Guthrie <cguthrie@mandriva.org> 0.7-1mdv2010.1
+ Revision: 543610
- New version: 0.7

* Sun Mar 07 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.6-1mdv2010.1
+ Revision: 515357
- Update to 0.6

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 0.5-1mdv2010.1
+ Revision: 484077
- update to new version 0.5

* Wed Aug 05 2009 Colin Guthrie <cguthrie@mandriva.org> 0.4-1mdv2010.0
+ Revision: 410012
- New version: 0.4

* Wed Jul 29 2009 Frederic Crozat <fcrozat@mandriva.com> 0.3-2mdv2010.0
+ Revision: 403990
- Fix incorrect dependency on old policykit version
- Do not call autoreconf, not needed

* Thu Jul 02 2009 Colin Guthrie <cguthrie@mandriva.org> 0.3-1mdv2010.0
+ Revision: 391822
- New version 0.3
- Drop unneeded patches

* Wed Jun 24 2009 Colin Guthrie <cguthrie@mandriva.org> 0.2-1mdv2010.0
+ Revision: 388804
- import rtkit


