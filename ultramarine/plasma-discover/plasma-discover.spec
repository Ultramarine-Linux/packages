# UM45 bootc package: ship the patched Discover application and its supported
# backends together. Updates are managed by um and System Settings.
%global stable_kf6 stable
%global base_name discover
%global flatpak_version 0.8.0
# fwupd stays off as before. Firmware updates are out of scope for Discover on Ultramarine.
%global fwupd 0

Name:    plasma-discover
Summary: KDE and Plasma resources management GUI
Version: 6.8.1
Release: 1%{?dist}

License: BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:     https://invent.kde.org/plasma/discover

Source0: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{base_name}-%{version}.tar.xz
Source1: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{base_name}-%{version}.tar.xz.sig

## downstream patches
# Updates are handled by um and System Settings > Updates (kcm_ultramarine_updates).
# Source: https://github.com/Ultramarine-Linux/plasma-patches/tree/main/discover
Patch300: 0001-Remove-Discover-updates-UI-in-favor-of-um.patch

# Dropped from the 6.7 spec:
# - Revert-b7ed897e... (KDE bug 512957): fixed upstream; 6.8.1 includes the fix.
# - discover-pk-refresh-timer.patch: only affects the update notifier, which is no longer shipped.

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

BuildRequires: appstream-qt-devel >= 1.0.0~
BuildRequires: flatpak-devel >= %{flatpak_version}
BuildRequires: libstemmer-devel
BuildRequires: libyaml-devel
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: pkgconfig(libmarkdown)
BuildRequires: cmake(QCoro6)
BuildRequires: cmake(KF6ItemModels)
%if 0%{?fwupd}
BuildRequires: pkgconfig(fwupd)
%endif

BuildRequires: extra-cmake-modules
BuildRequires: kf6-rpm-macros

BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6DBusAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6KirigamiAddons)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6Purpose)
BuildRequires: cmake(KF6StatusNotifierItem)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KF6Attica)
BuildRequires: cmake(KF6Archive)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Crash)
BuildRequires: cmake(KF6Declarative)
BuildRequires: cmake(KF6IconThemes)
BuildRequires: cmake(KF6IdleTime)
BuildRequires: cmake(KF6NewStuff)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: cmake(KF6UserFeedback)
BuildRequires: cmake(KF6XmlGui)
BuildRequires: cmake(KF6GuiAddons)

BuildRequires: pkgconfig(packagekitqt6)
BuildRequires: pkgconfig(phonon4qt6)

BuildRequires: pkgconfig(Qt6Concurrent)
BuildRequires: pkgconfig(Qt6DBus) >= 5.10.0
BuildRequires: pkgconfig(Qt6Network)
BuildRequires: pkgconfig(Qt6Qml)
BuildRequires: pkgconfig(Qt6QuickWidgets)
BuildRequires: pkgconfig(Qt6Svg)
BuildRequires: pkgconfig(Qt6Test)
%ifarch %{qt6_qtwebengine_arches}
BuildRequires: pkgconfig(Qt6WebView)
%endif
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: pkgconfig(Qt6Xml)

Requires: kf6-kirigami2
Requires: kf6-kitemmodels
# The patched QML imports org.kde.kcmutils to open System Settings > Updates.
Requires: kf6-kcmutils%{?_isa}
Requires: kf6-purpose
Requires: kf6-qqc2-desktop-style
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Recommends: %{name}-packagekit = %{version}-%{release}
Recommends: %{name}-flatpak = %{version}-%{release}
Recommends: fedora-appstream-metadata
# TODO: Recommends the package that provides kcm_ultramarine_updates once it has a name.

# Update functionality is removed. Get rid of Fedora's update subpackages and
# the ones Ultramarine doesn't build.
Obsoletes: plasma-discover-notifier < %{version}-%{release}
Obsoletes: plasma-discover-offline-updates < %{version}-%{release}
Obsoletes: plasma-discover-rpm-ostree < %{version}-%{release}
Obsoletes: plasma-discover-snap < %{version}-%{release}

%description
KDE and Plasma resources management GUI.

On Ultramarine, system and app updates are handled by um and
System Settings > Updates rather than by Discover.

%package libs
Summary: Runtime libraries for %{name}
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.

%package packagekit
Summary: Plasma Discover PackageKit support
Requires: %{name} = %{version}-%{release}
Requires: PackageKit
%description packagekit
Plasma Discover PackageKit backend plugin. This provides package management
support for traditional RPM packages through PackageKit.

%package flatpak
Summary: Plasma Discover flatpak support
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: flatpak >= %{flatpak_version}
Requires: flatpak-libs%{?_isa} >= %{flatpak_version}
Requires: (flatpak-kcm if plasma-systemsettings)
Supplements: (%{name} and flatpak)
%description flatpak
%{summary}.

%package kns
Summary: Plasma Discover KNewStuff support
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Supplements: (%{name} and plasma-workspace%{?_isa})
%description kns
%{summary}.


%prep
%autosetup -n %{base_name}-%{version} -p1


%build
%cmake_kf6 \
  -DPACKAGEKIT_AUTOREMOVE:BOOL=ON \
  -DWITH_KCM:BOOL=OFF \
  -DWITH_NOTIFIER:BOOL=OFF \
  -DBUILD_RpmOstreeBackend:BOOL=OFF \
  -DBUILD_SnapBackend:BOOL=OFF \
%if ! 0%{?fwupd}
  -DBUILD_FwupdBackend:BOOL=OFF \
%endif
  -DBUILD_FlatpakBackend:BOOL=ON \
  -DBUILD_KNSBackend:BOOL=ON

%cmake_build


%install
%cmake_install

# WITH_NOTIFIER=OFF only skips the daemon. The backends still install their
# discover-notifier plugins (DiscoverPackageKitNotifier, FlatpakNotifier), the
# notifier knotifications config, and the notifier/kcm_updates translations.
# Remove them; nothing loads them without the daemon.
# The kcm_updates.so, DiscoverNotifier, autostart and notifier/kcm .desktop removals below are
# no-ops on 6.8.1 (verified in a build). They are kept as cheap insurance in case upstream changes the flags.
rm -fv %{buildroot}%{_kf6_qtplugindir}/discover-notifier/*.so
rm -fv %{buildroot}%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_updates.so
rm -fv %{buildroot}%{_libexecdir}/DiscoverNotifier
rm -fv %{buildroot}%{_sysconfdir}/xdg/autostart/org.kde.discover.notifier.desktop
rm -fv %{buildroot}%{_datadir}/applications/org.kde.discover.notifier.desktop
rm -fv %{buildroot}%{_datadir}/applications/kcm_updates.desktop
# The snap backend is off but its desktop file is still installed.
rm -fv %{buildroot}%{_datadir}/applications/org.kde.discover.snap.desktop
rm -fv %{buildroot}%{_datadir}/knotifications6/discoverabstractnotifier.notifyrc
find %{buildroot}%{_datadir}/locale -name 'kcm_updates.mo' -delete -print
find %{buildroot}%{_datadir}/locale -name 'plasma-discover-notifier.mo' -delete -print

%find_lang libdiscover
%find_lang plasma-discover --with-html


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf6_metainfodir}/org.kde.discover.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_kf6_metainfodir}/org.kde.discover.flatpak.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_kf6_metainfodir}/org.kde.discover.packagekit.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.discover.desktop


%files -f plasma-discover.lang
%{_bindir}/plasma-discover
%{_kf6_metainfodir}/org.kde.discover.appdata.xml
%{_datadir}/applications/org.kde.discover.desktop
%{_datadir}/applications/org.kde.discover.urlhandler.desktop
%{_datadir}/icons/hicolor/*/apps/plasmadiscover.*
%{_datadir}/icons/hicolor/*/apps/flatpak-discover.*
# snapdiscover.svg is not installed with the snap backend off, so it's not listed.
%{_datadir}/kxmlgui5/plasmadiscover/
%{_kf6_datadir}/config.kcfg/discover*.kcfg
# appstreampreview (open a local AppStream file in Discover): the desktop file and metainfo
# are not notifier-related, so they stay in the main package. Fedora puts the desktop file in -notifier,
# which we don't build.
%{_datadir}/applications/org.kde.discover.appstreampreview.desktop
%{_kf6_metainfodir}/org.kde.discover.appstreampreview.metainfo.xml

%files libs -f libdiscover.lang
%license LICENSES/*.txt
%{_kf6_datadir}/qlogging-categories6/discover.categories
%dir %{_libdir}/plasma-discover/
%{_libdir}/plasma-discover/libDiscoverNotifiers.so
%{_libdir}/plasma-discover/libDiscoverCommon.so
%dir %{_kf6_qtplugindir}/discover
# Used by the appstreampreview desktop file in the main package, so it lives in -libs like Fedora.
%{_kf6_qtplugindir}/discover/appstream-preview-backend.so
%if 0%{?fwupd}
%{_kf6_qtplugindir}/discover/fwupd-backend.so
%endif
%dir %{_datadir}/libdiscover
%dir %{_datadir}/libdiscover/categories

%files packagekit
%{_kf6_metainfodir}/org.kde.discover.packagekit.appdata.xml
%{_kf6_qtplugindir}/discover/packagekit-backend.so
%{_datadir}/libdiscover/categories/packagekit-backend-categories.xml

%files flatpak
%{_kf6_metainfodir}/org.kde.discover.flatpak.appdata.xml
%{_kf6_qtplugindir}/discover/flatpak-backend.so
%{_datadir}/libdiscover/categories/flatpak-backend-categories.xml
%{_datadir}/applications/org.kde.discover.flatpak.desktop

%files kns
%{_kf6_qtplugindir}/discover/kns-backend.so


%changelog
* Fri Oct 23 2026 Cypress Reed <cypress@fyralabs.com>
- add plasma-discover with patches to remove update functionality
