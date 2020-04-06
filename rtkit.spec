%define Werror_cflags %{nil}

Summary:	Realtime Policy and Watchdog Daemon
Name:		rtkit
Version:	0.13
Release:	1
Group:		System/Libraries
License:	GPLv3+ and BSD
Url:		https://github.com/heftig/rtkit
Source0:	https://github.com/heftig/rtkit/releases/download/v%{version}/%{name}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	rpm-helper
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
BuildRequires:	kernel-release-headers
BuildRequires:	vim-common
Requires(pre,post,postun):	rpm-helper
Requires:	polkit >= 0.93

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%autosetup -p1

%build
%meson \
	-Dinstalled_tests=false \
	-Dsystemd_systemunitdir=%{_unitdir} \
	-G Ninja

%ninja_build

%install
%ninja_install

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
%dir %{_libexecdir}/installed-tests/rtkit
%{_libexecdir}/installed-tests/rtkit/rtkit-test
