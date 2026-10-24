%global _pkg_extra_ldflags -fuse-ld=lld

Name:    ultramarine-plasma-settings
Version: 0.1.2
Release: 1%{?dist}
Summary: Ultramarine Plasma System Settings modules

License: GPL-3.0-only
URL:     https://github.com/Ultramarine-Linux/plasma-patches
Source0: https://github.com/Ultramarine-Linux/plasma-patches/archive/refs/tags/%{version}.tar.gz
Source1: kdeglobals

BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: kf6-rpm-macros
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6I18n)
BuildRequires: pkgconfig(Qt6Core)
BuildRequires: pkgconfig(Qt6Gui)
BuildRequires: pkgconfig(Qt6Qml)
BuildRequires: pkgconfig(Qt6Quick)
BuildRequires: pkgconfig(Qt6Test)
BuildRequires: systemd-rpm-macros
BuildRequires: lld

Requires: plasma-systemsettings
Requires: kf6-kcmutils
Requires: kf6-kirigami
Requires: kf6-qqc2-desktop-style
# Tweaks KCM backend
Requires: umcli
# Update helper: privilege escalation, timers and "Ask me" notifications
Requires: polkit
Requires: systemd
Requires: libnotify

Packager: Cypress Reed <cypress@fyralabs.com>

%description
System Settings modules for Ultramarine Linux: Updates and Tweaks.
The Updates module is backed by the bundled ultramarine-updates helper,
which installs RPM (or bootc image), Flatpak and Nix updates and runs
automatic updates. The Tweaks module uses umcli.

%prep
%autosetup -n plasma-patches-%{version}

%conf
%cmake_kf6 \
    -DUM_EXECUTABLE:FILEPATH=%{_bindir}/um \
    -DULTRAMARINE_UPDATES_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-updates \
    -DSYSTEMD_SYSTEM_UNIT_DIR:PATH=%{_unitdir} \
    -DSYSTEMD_USER_UNIT_DIR:PATH=%{_userunitdir}

%build
%cmake_build

%install
%cmake_install

# Created by the helper on first use; owned here so they're removed with the package.
install -dm 0755 %{buildroot}%{_sysconfdir}/ultramarine-updates
install -dm 0755 %{buildroot}%{_sharedstatedir}/ultramarine-updates
touch %{buildroot}%{_sysconfdir}/ultramarine-updates/settings.json

# Hide Discover's duplicate Software Update KCM
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/kdeglobals

# Weblate catalogs are optional until translators add PO files.
%find_lang kcm_ultramarine_updates || :
%find_lang kcm_ultramarine_tweaks || :
: > %{name}.files
for lang_file in kcm_ultramarine_updates.lang kcm_ultramarine_tweaks.lang; do
    test ! -f "$lang_file" || cat "$lang_file" >> %{name}.files
done
printf '%s\n' \
    '%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_updates.so' \
    '%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_tweaks.so' \
    '%{_kf6_datadir}/applications/kcm_ultramarine_updates.desktop' \
    '%{_kf6_datadir}/applications/kcm_ultramarine_tweaks.desktop' \
    >> %{name}.files

# ultramarine-release's presets enable the automatic update timer.
%post
%systemd_post ultramarine-updates-automatic.timer

%preun
%systemd_preun ultramarine-updates-automatic.timer

%postun
# The service is a oneshot started by the timer: nothing to restart.
%systemd_postun ultramarine-updates-automatic.timer

%files -f %{name}.files
%doc README.md docs/*
%license LICENSE
%config(noreplace) %{_sysconfdir}/xdg/kdeglobals
%{_libexecdir}/ultramarine-updates
%{_datadir}/polkit-1/actions/org.ultramarine.updates.policy
%{_unitdir}/ultramarine-updates-automatic.service
%{_unitdir}/ultramarine-updates-automatic.timer
%{_userunitdir}/ultramarine-updates-user.service
%{_userunitdir}/ultramarine-updates-user.timer
%{_sysconfdir}/xdg/autostart/ultramarine-updates-user.desktop
%dir %{_sysconfdir}/ultramarine-updates
%ghost %config(noreplace) %{_sysconfdir}/ultramarine-updates/settings.json
%dir %{_sharedstatedir}/ultramarine-updates

%changelog
* Fri Oct 23 2026 Cypress Reed <cypress@fyralabs.com>
- initial package
