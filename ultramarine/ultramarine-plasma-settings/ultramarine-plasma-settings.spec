%global _pkg_extra_ldflags -fuse-ld=lld

Name:    ultramarine-plasma-settings
Version: 0.1.9
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
# merges translations into the desktop files, polkit policies and KCM metadata
BuildRequires: python3
BuildRequires: polkit-devel
BuildRequires: flatpak-devel
BuildRequires: kf6-rpm-macros
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6Service)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KF6NewStuffCore)
BuildRequires: pkgconfig(Qt6DBus)
BuildRequires: pkgconfig(Qt6Core)
BuildRequires: pkgconfig(Qt6Gui)
BuildRequires: pkgconfig(Qt6Qml)
BuildRequires: pkgconfig(Qt6Quick)
BuildRequires: pkgconfig(Qt6Test)
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: desktop-file-utils
BuildRequires: systemd-rpm-macros
BuildRequires: lld

Recommends: %{name}-kcm-updates%{?_isa} = %{evr}
Recommends: %{name}-kcm-tweaks%{?_isa} = %{evr}
Recommends: %{name}-kcm-location%{?_isa} = %{evr}
Recommends: %{name}-dgpu%{?_isa} = %{evr}
Recommends: %{name}-office-apps%{?_isa} = %{evr}

Packager: Cypress Reed <cypress@fyralabs.com>

%description
System Settings modules and desktop helpers for Ultramarine Linux. This is a
metapackage that recommends the Updates, Tweaks and Location Services KCMs, the
dGPU launcher action, and the office suite installer.

%package common
Summary: Shared documentation, license and translations for %{name}
BuildArch: noarch

%description common
Documentation, license and translations shared by the %{name} subpackages.

%package kcm-updates
Summary: Plasma settings pane for Ultramarine system updates
Requires: %{name}-common = %{evr}
Requires: %{name}-updates%{?_isa} = %{evr}
Requires: plasma-systemsettings
Requires: kf6-kcmutils
Requires: kf6-kirigami
Requires: kf6-qqc2-desktop-style

%description kcm-updates
System Settings module for managing updates on Ultramarine Linux. It replaces
Discover's Software Update module and is backed by %{name}-updates.

%package updates
Summary: Backend for Ultramarine system update KCM
Requires: %{name}-common = %{evr}
# privilege escalation, timers and "Ask me" notifications
Requires: polkit
Requires: systemd
Requires: libnotify
# offline updates need pkgcli and packagekit-offline-update.service
Requires: PackageKit >= 1.3.4

%description updates
The ultramarine-updates helper, which installs RPM (or bootc image), Flatpak, Nix,
and plasmoid updates, and the systemd units that run automatic updates.

%package kcm-tweaks
Summary: Plasma settings pane for Ultramarine system tweaks
Requires: %{name}-common = %{evr}
Requires: plasma-systemsettings
Requires: kf6-kcmutils
Requires: kf6-kirigami
Requires: kf6-qqc2-desktop-style
Requires: umcli

%description kcm-tweaks
System Settings module for Ultramarine system tweaks, backed by umcli.

%package kcm-location
Summary: Plasma settings pane for turning location services on or off
Requires: %{name}-common = %{evr}
Requires: plasma-systemsettings
Requires: kf6-kcmutils
Requires: kf6-kirigami
# the page uses org.kde.kirigamiaddons.formcard
Requires: kf6-kirigami-addons
Requires: kf6-qqc2-desktop-style
# the helper masks or unmasks geoclue.service through pkexec
Requires: geoclue2
Requires: polkit
Requires: systemd

%description kcm-location
System Settings module that turns GeoClue location services on or off for the
whole system, until Plasma ships its own switch.

%package dgpu
Summary: Plasma launcher context menu addition to launch on dedicated GPU
Requires: %{name}-common = %{evr}
# ultramarine-dgpu-launch gets the discrete GPU's environment from switcheroo-control
# over D-Bus and runs the app itself. It shows up in app launchers only.
# see https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/4149
# and https://invent.kde.org/plasma/plasma-workspace/-/merge_requests/7333
Requires: switcheroo-control
Requires: systemd-udev

%description dgpu
Adds a "Launch Using Dedicated Graphics Card" action to the Plasma app launchers
on systems with hybrid graphics.

%package office-apps
Summary: Popup for Ultramarine users to install an office suite
Requires: %{name}-common = %{evr}
Requires: flatpak
Requires: PackageKit

%description office-apps
A helper that offers to install an office suite when a document is opened and
none is installed.

%prep
%autosetup -n plasma-patches-%{version}

%conf
%cmake_kf6 \
    -DUM_EXECUTABLE:FILEPATH=%{_bindir}/um \
    -DULTRAMARINE_UPDATES_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-updates \
    -DSYSTEMD_SYSTEM_UNIT_DIR:PATH=%{_unitdir} \
    -DSYSTEMD_USER_UNIT_DIR:PATH=%{_userunitdir} \
    -DUDEV_RULES_DIR:PATH=%{_udevrulesdir} \
    -DULTRAMARINE_LOCATION_HELPER:FILEPATH=%{_libexecdir}/ultramarine-location-helper \
    -DDGPU_DETECT_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-dgpu-detect \
    -DDGPU_LAUNCH_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-dgpu-launch \
    -DOFFICE_INSTALLER_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-office-installer

%build
%cmake_build

%install
%cmake_install

# created by the helper on first use. owned here so they're removed with the package.
install -dm 0755 %{buildroot}%{_sysconfdir}/ultramarine-updates
touch %{buildroot}%{_sysconfdir}/ultramarine-updates/settings.json

# hide Discover's duplicate Software Update KCM
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/kdeglobals

%find_lang %{name} --all-name

%check
%desktop_file_validate %{buildroot}%{_kf6_datadir}/applications/org.ultramarine.OfficeInstaller.desktop

# ultramarine-release's presets enable the automatic update timer.
%post updates
%systemd_post ultramarine-updates-automatic.timer

%preun updates
%systemd_preun ultramarine-updates-automatic.timer

%postun updates
# the service is a oneshot started by the timer, so there's nothing to restart
%systemd_postun ultramarine-updates-automatic.timer

# udev runs the dGPU check at boot and on GPU hotplug. Run it now too, so the
# action shows up without a reboot. (Skipped in image builds w/ no running systemd)
%post dgpu
if [ -d /run/systemd/system ]; then
    systemctl --no-block restart ultramarine-dgpu-detect.service >/dev/null 2>&1 || :
fi

%postun dgpu
if [ $1 -eq 0 ]; then
    rm -rf /run/ultramarine-dgpu-launch
fi

# metapackage, so it has no files of its own
%files

%files common -f %{name}.lang
%doc README.md docs/*
%license LICENSE

%files kcm-updates
%config(noreplace) %{_sysconfdir}/xdg/kdeglobals
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_updates.so
%{_kf6_datadir}/applications/kcm_ultramarine_updates.desktop

%files updates
%{_libexecdir}/ultramarine-updates
%{_datadir}/polkit-1/actions/org.ultramarine.updates.policy
%{_unitdir}/ultramarine-updates-automatic.service
%{_unitdir}/ultramarine-updates-automatic.timer
%{_userunitdir}/ultramarine-updates-user.service
%{_userunitdir}/ultramarine-updates-user.timer
%{_sysconfdir}/xdg/autostart/ultramarine-updates-user.desktop
%dir %{_sysconfdir}/ultramarine-updates
%ghost %config(noreplace) %{_sysconfdir}/ultramarine-updates/settings.json

%files kcm-tweaks
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_tweaks.so
%{_kf6_datadir}/applications/kcm_ultramarine_tweaks.desktop

%files kcm-location
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_location.so
%{_kf6_datadir}/applications/kcm_ultramarine_location.desktop
%{_libexecdir}/ultramarine-location-helper
%{_datadir}/polkit-1/actions/org.ultramarine.location.policy

%files dgpu
%{_libexecdir}/ultramarine-dgpu-detect
%{_libexecdir}/ultramarine-dgpu-launch
%{_udevrulesdir}/90-ultramarine-dgpu.rules
%{_unitdir}/ultramarine-dgpu-detect.service
%dir %{_datadir}/ultramarine
%{_datadir}/ultramarine/ultramarine-dgpu-launch.desktop
%dir %{_datadir}/plasma/kickeractions
# broken symlink until ultramarine-dgpu-detect finds a hybrid GPU setup
%{_datadir}/plasma/kickeractions/ultramarine-dgpu-launch.desktop

%files office-apps
%{_libexecdir}/ultramarine-office-installer
%{_kf6_datadir}/applications/org.ultramarine.OfficeInstaller.desktop

%changelog
* Mon Nov 02 2026 Cypress Reed <cypress@fyralabs.com>
- split into subpackages

* Fri Oct 23 2026 Cypress Reed <cypress@fyralabs.com>
- initial package
