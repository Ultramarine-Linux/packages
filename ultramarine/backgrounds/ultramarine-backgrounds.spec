%undefine _disable_source_fetch

Name: ultramarine-backgrounds
Version: 39
Release: 2%{?dist}
BuildArch: noarch
# details for the artworks' licenses can be seen in the COPYING file
License: CC-BY-SA 4.0 and CC0
Summary: Ultramarine Linux backgrounds
Provides: desktop-backgrounds = %{version}-%{release}
Requires: /usr/bin/ln
BuildRequires: make
# licensing information
Source0: https://github.com/Ultramarine-Linux/backgrounds/archive/refs/tags/39.tar.gz
Source1: 30_default_backgrounds.gschema.override
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
%autosetup -n backgrounds-%{version}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
cp -v %{SOURCE1} %{buildroot}%{_datadir}/glib-2.0/schemas/30_default_backgrounds.gschema.override
mkdir -p %{buildroot}%{_datadir}/wallpapers/{"Tortuga Dark","Tortuga Light"}/contents/images

# Symlink the backgrounds for KDE
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/ultramarine/ultramarine-dark.png %{buildroot}%{_datadir}/wallpapers/"Ultramarine Dark"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/ultramarine/ultramarine-dark.png %{buildroot}%{_datadir}/wallpapers/"Ultramarine Dark"/contents/screenshot.png

ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/ultramarine/ultramarine-light.png %{buildroot}%{_datadir}/wallpapers/"Ultramarine Light"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/ultramarine/ultramarine-light.png %{buildroot}%{_datadir}/wallpapers/"Ultramarine Light"/contents/screenshot.png

ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/38/tortuga-dark.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Dark"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/38/tortuga-dark.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Dark"/contents/screenshot.png

ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/38/tortuga-light.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Light"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/38/tortuga-light.png %{buildroot}%{_datadir}/wallpapers/"Tortuga Light"/contents/screenshot.png

ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/39/foresty-skies-d.png %{buildroot}%{_datadir}/wallpapers/"Forresty Skies Dark"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/39/foresty-skies-d.png %{buildroot}%{_datadir}/wallpapers/"Forresty Skies Dark"/contents/screenshot.png

ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/39/foresty-skies-l.png %{buildroot}%{_datadir}/wallpapers/"Forresty Skies Light"/contents/images/3840x2160.png
ln -rsf %{buildroot}%{_datadir}/backgrounds/ultramarine-linux/39/foresty-skies-l.png %{buildroot}%{_datadir}/wallpapers/"Forresty Skies Light"/contents/screenshot.png


%files
%license COPYING

%files common
%{_datadir}/backgrounds/ultramarine-linux/
%{_datadir}/glib-2.0/schemas/30_default_backgrounds.gschema.override
#%%{_datadir}/backgrounds/default
#%%{_datadir}/backgrounds/default.png
/usr/share/wallpapers/Ultramarine*/metadata.desktop

%files gnome
%{_datadir}/gnome-background-properties/ultramarine-wallpapers-extras.xml
%{_datadir}/gnome-background-properties/ultramarine.xml

%files kde
%{_datadir}/wallpapers/Tortuga*
%{_datadir}/wallpapers/Ultramarine*
%{_datadir}/wallpapers/Forresty*


%changelog
%autochangelog -p -l 5 -s -c -o $PWD/ultramarine-backgrounds.spec