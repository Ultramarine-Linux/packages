%global _pkg_extra_ldflags -fuse-ld=lld

Name:    ultramarine-plasma-settings
Version: 0.1.5
Release: 2%{?dist}
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

Requires: plasma-systemsettings
Requires: kf6-kcmutils
Requires: kf6-kirigami
Requires: kf6-qqc2-desktop-style
# tweaks KCM backend
Requires: umcli
# Update helper: privilege escalation, timers and "Ask me" notifications
Requires: polkit
Requires: systemd
Requires: libnotify
# Launch Using Dedicated Graphics Card: switcherooctl picks the GPU and sets its
# environment, kioclient launches the app. It shows up in the app launchers only.
# see https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/4149
# and https://invent.kde.org/plasma/plasma-workspace/-/merge_requests/7333
Requires: switcheroo-control
Requires: kde-cli-tools
Requires: systemd-udev
# office apps installer
Requires: flatpak
Requires: PackageKit

Packager: Cypress Reed <cypress@fyralabs.com>

%description
System Settings modules for Ultramarine Linux: Updates and Tweaks.
The Updates module is backed by the bundled ultramarine-updates helper,
which installs RPM (or bootc image), Flatpak, Nix, and plasmoid updates and runs
automatic updates. The Tweaks module uses umcli.
It also includes a helper that offers to install an office suite when a document is
opened and none is installed.

%prep
%autosetup -n plasma-patches-%{version}

%conf
%cmake_kf6 \
    -DUM_EXECUTABLE:FILEPATH=%{_bindir}/um \
    -DULTRAMARINE_UPDATES_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-updates \
    -DSYSTEMD_SYSTEM_UNIT_DIR:PATH=%{_unitdir} \
    -DSYSTEMD_USER_UNIT_DIR:PATH=%{_userunitdir} \
    -DUDEV_RULES_DIR:PATH=%{_udevrulesdir} \
    -DDGPU_DETECT_EXECUTABLE:FILEPATH=%{_libexecdir}/ultramarine-dgpu-detect \
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

# Weblate catalogs are optional until translators add PO files
%find_lang kcm_ultramarine_updates || :
%find_lang kcm_ultramarine_tweaks || :
%find_lang ultramarine_office_installer || :
: > %{name}.files
for lang_file in kcm_ultramarine_updates.lang kcm_ultramarine_tweaks.lang ultramarine_office_installer.lang; do
    test ! -f "$lang_file" || cat "$lang_file" >> %{name}.files
done
printf '%s\n' \
    '%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_updates.so' \
    '%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_tweaks.so' \
    '%{_kf6_datadir}/applications/kcm_ultramarine_updates.desktop' \
    '%{_kf6_datadir}/applications/kcm_ultramarine_tweaks.desktop' \
    >> %{name}.files

%check
%desktop_file_validate %{buildroot}%{_kf6_datadir}/applications/org.ultramarine.OfficeInstaller.desktop

# ultramarine-release's presets enable the automatic update timer.
%post
%systemd_post ultramarine-updates-automatic.timer
# udev runs the dGPU check at boot and on GPU hotplug. Run it now too, so the
# action shows up without a reboot. (Skipped in image builds w/ no running systemd)
if [ -d /run/systemd/system ]; then
    systemctl --no-block restart ultramarine-dgpu-detect.service >/dev/null 2>&1 || :
fi

%preun
%systemd_preun ultramarine-updates-automatic.timer

%postun
# the service is a oneshot started by the timer, so there's nothing to restart
%systemd_postun ultramarine-updates-automatic.timer
if [ $1 -eq 0 ]; then
    rm -rf /run/ultramarine-dgpu-launch
fi

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
%{_libexecdir}/ultramarine-dgpu-detect
%{_udevrulesdir}/90-ultramarine-dgpu.rules
%{_unitdir}/ultramarine-dgpu-detect.service
%{_libexecdir}/ultramarine-office-installer
%{_kf6_datadir}/applications/org.ultramarine.OfficeInstaller.desktop
%dir %{_datadir}/ultramarine
%{_datadir}/ultramarine/ultramarine-dgpu-launch.desktop
%dir %{_datadir}/plasma/kickeractions
# broken symlink until ultramarine-dgpu-detect finds a hybrid GPU setup
%{_datadir}/plasma/kickeractions/ultramarine-dgpu-launch.desktop
%dir %{_sysconfdir}/ultramarine-updates
%ghost %config(noreplace) %{_sysconfdir}/ultramarine-updates/settings.json

%changelog
* Fri Oct 23 2026 Cypress Reed <cypress@fyralabs.com>
- initial package
