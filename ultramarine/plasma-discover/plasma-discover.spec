%global base_name discover
# enable fwupd support (or not)
%global fwupd 0

Name:    plasma-discover
Summary: KDE and Plasma resources management GUI
Version: 6.5.3
Release: 1%{?dist}

License: BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:     https://invent.kde.org/plasma/discover

Source0: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{base_name}-%{version}.tar.xz
Source1: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{base_name}-%{version}.tar.xz.sig

Patch1:  Revert-b7ed897e6842002b195c02c6e89f4e06aee12d09.patch

## downstream patches
# Adjust periodic refresh from 1/24hr to 1/12hr
# This ensures that it is checked at least once during the work day.
# It is double the time that Fedora repos are set to in DNF (6h).
Patch200: discover-pk-refresh-timer.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

BuildRequires: appstream-qt-devel >= 1.0.0~
BuildRequires: libstemmer-devel
BuildRequires: libyaml-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: pkgconfig(libmarkdown)
BuildRequires: cmake(QCoro6)
BuildRequires: cmake(KF6ItemModels)

BuildRequires: extra-cmake-modules
BuildRequires: kf6-rpm-macros

BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6DBusAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KF6Attica)
BuildRequires: cmake(KF6Archive)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Crash)
BuildRequires: cmake(KF6Declarative)
BuildRequires: cmake(KF6IconThemes)
BuildRequires: cmake(KF6IdleTime)
BuildRequires: cmake(KF6Kirigami2)

BuildRequires: pkgconfig(packagekitqt6)

BuildRequires: pkgconfig(Qt6Concurrent)
BuildRequires: pkgconfig(Qt6DBus) >= 5.10.0
BuildRequires: pkgconfig(Qt6Network)
BuildRequires: pkgconfig(Qt6Qml)
BuildRequires: pkgconfig(Qt6QuickWidgets)
BuildRequires: pkgconfig(Qt6Svg)
BuildRequires: pkgconfig(Qt6Test)
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: pkgconfig(Qt6Xml)

%description
KDE and Plasma resources management GUI.
This is a patched build that only provides the PackageKit backend plugin.

%package packagekit
Summary: Plasma Discover PackageKit support
Requires: plasma-discover
Requires: plasma-discover-libs%{?_isa}
Requires: PackageKit
%description packagekit
Plasma Discover PackageKit backend plugin. This provides package management
support for traditional RPM packages through PackageKit.


%prep
%autosetup -n %{base_name}-%{version} -p1


%build
%cmake_kf6 \
  -DPACKAGEKIT_AUTOREMOVE:BOOL=ON \
  -DBUILD_FlatpakBackend:BOOL=OFF \
  -DBUILD_RpmOstreeBackend:BOOL=OFF \
  -DBUILD_SteamOSBackend:BOOL=OFF \
  -DBUILD_SnapBackend:BOOL=OFF \
  -DBUILD_FwupdBackend:BOOL=OFF \
  -DBUILD_KNSBackend:BOOL=OFF

%cmake_build


%install
%cmake_install

# Remove everything except the PackageKit plugin files
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_libexecdir}
rm -rf %{buildroot}%{_kf6_metainfodir}/org.kde.discover.appdata.xml
rm -rf %{buildroot}%{_kf6_metainfodir}/org.kde.discover.flatpak.appdata.xml
rm -rf %{buildroot}%{_datadir}/applications
rm -rf %{buildroot}%{_datadir}/icons
rm -rf %{buildroot}%{_datadir}/kxmlgui5
rm -rf %{buildroot}%{_datadir}/knotifications6
rm -rf %{buildroot}%{_sysconfdir}
rm -rf %{buildroot}%{_kf6_datadir}/qlogging-categories6
rm -rf %{buildroot}%{_libdir}/plasma-discover
rm -rf %{buildroot}%{_kf6_qtplugindir}/plasma
rm -rf %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{_kf6_qtplugindir}/discover/kns-backend.so



%files packagekit
%license LICENSES/*.txt
%{_kf6_metainfodir}/org.kde.discover.packagekit.appdata.xml
%dir %{_kf6_qtplugindir}/discover
%dir %{_kf6_qtplugindir}/discover-notifier
%{_kf6_qtplugindir}/discover-notifier/DiscoverPackageKitNotifier.so
%{_kf6_qtplugindir}/discover/packagekit-backend.so
%{_datadir}/libdiscover/categories/packagekit-backend-categories.xml


%changelog
%autochangelog
