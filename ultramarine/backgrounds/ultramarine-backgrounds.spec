%define ver 41
%undefine _disable_source_fetch

Name: ultramarine-backgrounds
Version: %(echo %ver | sed 's/-/~/g')
Release: 1%{?dist}
BuildArch: noarch
# details for the artworks' licenses can be seen in the COPYING file
License: CC-BY-SA 4.0 and CC0
Summary: Ultramarine Linux backgrounds
Provides: desktop-backgrounds = %{version}-%{release}
Requires: /usr/bin/ln
Recommends: ultramarine-backgrounds-compat = %{version}-%{release}
BuildRequires: make
# licensing information
Source0: https://github.com/Ultramarine-Linux/backgrounds/archive/refs/tags/%ver.tar.gz
#Source1: 30_default_backgrounds.gschema.override
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

%package        compat
Summary:        Compatibility package for ultramarine-backgrounds
Requires:   ultramarine-backgrounds-common = %{version}-%{release}
Provides: desktop-backgrounds-compat = %{version}-%{release}
License:        CC0
Obsoletes:		desktop-backgrounds-compat = 40.0.0-1
Conflicts:    desktop-backgrounds-compat

%description    compat
The desktop-backgrounds-compat package contains compatibility symlinks for other desktop environments.

%prep
%autosetup -n backgrounds-%{ver}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/


# Symlink the backgrounds for KDE


kde_link() {
    local file=$1
    local wallname=$2
    ln -rsf "%{buildroot}%{_datadir}/backgrounds/ultramarine-linux/$file" "%{buildroot}%{_datadir}/wallpapers/$wallname/contents/images/3840x2160.png"
    ln -rsf "%{buildroot}%{_datadir}/backgrounds/ultramarine-linux/$file" "%{buildroot}%{_datadir}/wallpapers/$wallname/contents/screenshot.png"
}


kde_link 38/tortuga-dark.png "Tortuga Dark"
kde_link 38/tortuga-light.png "Tortuga Light"

kde_link 39/foresty-skies-d.png "Forresty Skies Dark"
kde_link 39/foresty-skies-l.png "Forresty Skies Light"

kde_link 40/lost-dark.png "Lost Dark"
kde_link 40/lost-light.png "Lost Light"

kde_link 40/umbrella-dark.png "Umbrella Dark"
kde_link 40/umbrella-light.png "Umbrella Light"

kde_link 41~beta/um41-beta.png "Ultramarine 41 Beta"

kde_link 41/viewports-light.png "Viewports Light"
kde_link 41/viewports-dark.png "Viewports Dark"
kde_link 41/viewport-fake-dark.png "Viewports Fake Dark"

kde_link preview/blueprint.png "Ultramarine Preview"

kde_link ultramarine/ultramarine-dark.png "Ultramarine Dark"
kde_link ultramarine/ultramarine-light.png "Ultramarine Light"

# Compat files

compat_link() {
    local file=$1
    local dest=$2
    ln -rsf "%{buildroot}%{_datadir}/backgrounds/ultramarine-linux/$file" "%{buildroot}%{_datadir}/backgrounds/$dest"
}


DEFAULT_WALL="41/viewports-light.png"
DEFAULT_DARK_WALL="41/viewports-dark.png"
DEFAULT_XML="41/lost.xml"

# Let's generate our default gschema override file

cat << EOF > %{buildroot}%{_datadir}/glib-2.0/schemas/30_default_backgrounds.gschema.override
[org.gnome.desktop.background]
picture-uri='file://%{_datadir}/backgrounds/ultramarine-linux/$DEFAULT_WALL'
picture-uri-dark='file:///%{_datadir}/backgrounds/ultramarine-linux/$DEFAULT_DARK_WALL'
EOF


compat_link $DEFAULT_WALL default.png
compat_link $DEFAULT_DARK_WALL default-dark.png
compat_link $DEFAULT_XML default.xml

mkdir -p %{buildroot}%{_datadir}/backgrounds/images/

compat_link $DEFAULT_WALL images/default.png
compat_link $DEFAULT_WALL images/default-5_4.png
compat_link $DEFAULT_WALL images/default-16_9.png
compat_link $DEFAULT_WALL images/default-16_10.png

compat_link $DEFAULT_DARK_WALL images/default-dark.png
compat_link $DEFAULT_DARK_WALL images/default-dark-5_4.png
compat_link $DEFAULT_DARK_WALL images/default-dark-16_9.png
compat_link $DEFAULT_DARK_WALL images/default-dark-16_10.png

%files
%license COPYING

%files common
%{_datadir}/backgrounds/ultramarine-linux/
%{_datadir}/glib-2.0/schemas/30_default_backgrounds.gschema.override
/usr/share/wallpapers/Ultramarine*/metadata.desktop

%files gnome
%{_datadir}/gnome-background-properties/ultramarine-wallpapers-extras.xml
%{_datadir}/gnome-background-properties/ultramarine.xml

%files kde
%{_datadir}/wallpapers/*

%files compat
%dir %{_datadir}/backgrounds/images/
%{_datadir}/backgrounds/images/default*
%{_datadir}/backgrounds/default.png
%{_datadir}/backgrounds/default-dark.png
%{_datadir}/backgrounds/default.xml


%changelog
%autochangelog -p -l 5 -s -c -o $PWD/ultramarine-backgrounds.spec
