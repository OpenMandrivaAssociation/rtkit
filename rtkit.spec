%define Werror_cflags %{nil}

Summary:	Realtime Policy and Watchdog Daemon
Name:		rtkit
Version:	0.13
Release:	5
Group:		System/Libraries
License:	GPLv3+ and BSD
Url:		https://github.com/heftig/rtkit
Source0:	https://github.com/heftig/rtkit/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:	%{name}.sysusers
Patch0:		https://patch-diff.githubusercontent.com/raw/heftig/rtkit/pull/17.patch
Patch1:		https://patch-diff.githubusercontent.com/raw/heftig/rtkit/pull/18.patch
Patch2:		https://patch-diff.githubusercontent.com/raw/heftig/rtkit/pull/19.patch
Patch3:		https://patch-diff.githubusercontent.com/raw/heftig/rtkit/pull/26.patch
BuildRequires:	meson
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	kernel-release-headers
BuildRequires:	vim-common
Requires:	polkit >= 0.93
Requires(pre):	systemd
%systemd_requires

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
	-Dsystemd_systemunitdir=%{_unitdir}

%meson_build

%install
%meson_install

install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-rtkit.preset << EOF
enable rtkit-daemon.service
EOF

%pre
%sysusers_create_package %{name} %{SOURCE1}

%post
%systemd_post rtkit-daemon.service
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :

%preun
%systemd_preun rtkit-daemon.service

%postun
%systemd_postun_with_restart rtkit-daemon.service

%files
%doc README rtkit.c rtkit.h
%attr(0755,root,root) %{_bindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_sysusersdir}/%{name}.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%{_datadir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
%{_presetdir}/86-rtkit.preset
%{_unitdir}/rtkit-daemon.service
%doc %{_mandir}/man*/rtkitctl.*
