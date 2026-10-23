Name:    ultramarine-plasma-settings
Version: 0.1.0
Release: 1%{?dist}
Summary: Ultramarine Plasma System Settings modules

License: GPL-3.0-only
URL:     https://github.com/Ultramarine-Linux/plasma-patches
Source0: https://github.com/Ultramarine-Linux/plasma-patches/archive/refs/tags/%{version}.tar.gz

BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: gcc-c++
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
    -DBUILD_TESTING:BOOL=ON \
    -DUM_EXECUTABLE:FILEPATH=%{_bindir}/um

%build
%cmake_build

%install
%cmake_install

%find_lang kcm_ultramarine_updates || :
%find_lang kcm_ultramarine_tweaks || :
: > %{name}.lang
for f in kcm_ultramarine_updates.lang kcm_ultramarine_tweaks.lang; do
    test ! -f "$f" || cat "$f" >> %{name}.lang
done

# add `-f %{name}.lang` to %files once we have some translations

%files
%doc README.md docs/*
%license LICENSE
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_updates.so
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_ultramarine_tweaks.so
%{_appsdir}/kcm_ultramarine_updates.desktop
%{_appsdir}/kcm_ultramarine_tweaks.desktop

%changelog
* Fri Oct 23 2026 Cypress Reed <cypress@fyralabs.com>
- initial package
