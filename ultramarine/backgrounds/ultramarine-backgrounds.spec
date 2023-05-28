%undefine _disable_source_fetch

Name: ultramarine-backgrounds
Version: 37
Release: 1%{?dist}
BuildArch: noarch
# details for the artworks' licenses can be seen in the COPYING file
License: CC-BY-SA 4.0 and CC0
Summary: Ultramarine Linux backgrounds
Provides: desktop-backgrounds = %{version}-%{release}
Requires: /usr/bin/ln
BuildRequires: make
# licensing information
Source0: https://github.com/Ultramarine-Linux/backgrounds/archive/refs/heads/main.tar.gz
Source1: 20_default_backgrounds.gschema.override
# CC0 artworks


%description
This package contains desktop backgrounds for the Ultramarine Linux default theme.

%package    common
Summary:    Ultramarine Linux backgrounds: common files
Provides:   ultramarine-backgrounds-common = %{version}-%{release}
Provides:   ultramarine-backgrounds-basic = %{version}-%{release}

Obsoletes:   ultramarine-backgrounds-common < %{version}-%{release}
%description    common
The actual desktop background files for Ultramarine Linux.

%package        gnome
Summary:        The default Fedora wallpaper from GNOME desktop
Requires:   ultramarine-backgrounds-common = %{version}-%{release}
# starting with this release, gnome uses picture-uri instead of picture-filename
# see gnome bz #633983
Requires:       gsettings-desktop-schemas >= 2.91.92
Provides:       system-backgrounds-gnome = %{version}-%{release}
License:        CC0

%description    gnome
The desktop-backgrounds-gnome package sets default background in GNOME-based desktops

%package        kde
Summary:        The default KDE wallpaper from KDE desktop
Requires:   ultramarine-backgrounds-common = %{version}-%{release}
Provides:       system-backgrounds-kde = %{version}-%{release}
License:        CC0

%description    kde
The desktop-backgrounds-kde package sets default background in the KDE Plasma desktop

%prep
%autosetup -n backgrounds-main


%install
rm -rf $RPM_BUILD_ROOT
%make_install

#pushd %{buildroot}%{_datadir}/backgrounds

#mkdir -p %{buildroot}%{_datadir}/backgrounds/
#ln -s ultramarine-linux/default %{buildroot}%{_datadir}/backgrounds/
#ln -s default/default.jpg %{buildroot}%{_datadir}/backgrounds/default.png
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
cp -v %{SOURCE1} %{buildroot}%{_datadir}/glib-2.0/schemas/20_default_backgrounds.gschema.override

# Symlink the backgrounds for KDE
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/tortuga/tortuga-dark.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Dark"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/tortuga/tortuga-dark.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Dark"/contents/screenshot.png

ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/tortuga/tortuga-light.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Light"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/tortuga/tortuga-light.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Light"/contents/screenshot.png


%files
%license COPYING

%files common
%{_datadir}/backgrounds/ultramarine-linux/
%{_datadir}/glib-2.0/schemas/20_default_backgrounds.gschema.override
#%%{_datadir}/backgrounds/default
#%%{_datadir}/backgrounds/default.png

%files gnome
%{_datadir}/gnome-background-properties/ultramarine-wallpapers.xml

%files kde
%{_datadir}/wallpapers/Tortuga*
