Name:          rtkit
Version:       0.6
Release:       %mkrel 1
Summary:       Realtime Policy and Watchdog Daemon
Group:         System/Libraries
License:       GPLv3+ and BSD
URL:           http://git.0pointer.de/?p=rtkit.git
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:      polkit >= 0.93
BuildRequires: dbus-devel >= 1.2
BuildRequires: libcap-devel
BuildRequires: polkit-1-devel
Source0:       http://0pointer.de/public/%{name}-%{version}.tar.gz

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%setup -q

%build
%configure2_5x
%make
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
rm -rf %{buildroot}
%makeinstall_std
install -D org.freedesktop.RealtimeKit1.xml %{buildroot}/%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
