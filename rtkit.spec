%define Werror_cflags %{nil}
%define snap 20190227

Summary:	Realtime Policy and Watchdog Daemon
Name:		rtkit
Version:	0.11
Release:	19.%{snap}.6
Group:		System/Libraries
License:	GPLv3+ and BSD
Url:		http://git.0pointer.de/?p=rtkit.git
Source0:	http://0pointer.de/public/%{name}-%{version}-%{snap}.tar.xz
BuildRequires:	rpm-helper
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
Requires(pre,post,postun):	rpm-helper
Requires:	polkit >= 0.93

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%autosetup -n %{name}-%{version}-%{snap} -p1
./autogen.sh

%build
%configure \
	--with-systemdsystemunitdir=%{_unitdir}

%make_build
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
%make_install
install -D org.freedesktop.RealtimeKit1.xml %{buildroot}/%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-rtkit.preset << EOF
enable rtkit-daemon.service
EOF

%pre
%_pre_useradd rtkit /proc /sbin/nologin

%postun
%_postun_userdel rtkit

%files
%doc README rtkit.c rtkit.h
%attr(0755,root,root) %{_sbindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%{_mandir}/man*/rtkitctl.*
%{_datadir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
%{_presetdir}/86-rtkit.preset
%{_unitdir}/rtkit-daemon.service
