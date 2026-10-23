Name:    ultramarine-plasma-settings
Version: 0.1.0
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

Requires: plasma-systemsettings
Requires: kf6-kcmutils
Requires: kf6-kirigami
Requires: kf6-qqc2-desktop-style
Requires: umcli

Packager: Cypress Reed <cypress@fyralabs.com>

%description
System Settings modules for Ultramarine Linux: Updates and Tweaks.
Both modules use umcli for their backend.

%prep
%autosetup -n plasma-patches-%{version}

%conf
%cmake_kf6 \
    -DUM_EXECUTABLE:FILEPATH=%{_bindir}/um

%build
%cmake_build

%install
%cmake_install

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

%files -f %{name}.files
%doc README.md docs/*
%license LICENSE
%config(noreplace) %{_sysconfdir}/xdg/kdeglobals

%changelog
* Fri Oct 23 2026 Cypress Reed <cypress@fyralabs.com>
- initial package
