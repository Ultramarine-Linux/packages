Name: gs-plugin-ultramarine-pkgdb-collections
Version: 0.1.0
Release: 1%{?dist}
URL: https://ultramarine-linux.org
Source0: https://github.com/Ultramarine-Linux/gs-plugin-ultramarine-pkgdb-collections/archive/refs/tags/v%version.tar.gz
License: GPL-2.0-or-later
Summary: Ultramarine pkgdb collections plugin for GNOME Software
Supplements: gnome-software

BuildRequires: meson
BuildRequires: gcc
BuildRequires: pkgconfig(gnome-software)

%description
A GNOME Software plugin for the ultramarine pkgdb collections, allowing for system upgrades between major UM versions.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%files
%{_libdir}/gnome-software/plugins-20/libgs_plugin_ultramarine-pkgdb-collections.so
%{_metainfodir}/org.gnome.Software.Plugin.UltramarinePkgdbCollections.metainfo.xml

%changelog
* Fri Apr 5 2024 Lleyton Gray <lleyton@fyralabs.com> - 0.1.0-1
- Initial version

