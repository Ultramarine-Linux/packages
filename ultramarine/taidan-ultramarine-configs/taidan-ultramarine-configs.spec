Name:           taidan-ultramarine-configs
Version:        45
Release:        2%?dist
Summary:        Taidan configuration for Ultramarine
License:        (MIT AND GPL-3.0-or-later)
Supplements:    taidan
Provides:       initial-setup initial-setup-gui
Requires:       umcli

BuildArch:      noarch

%description
This package provides the Taidan configuration files for Ultramarine.

%global tweak(p:) %{quote:
%package tweaks-%1
Summary: Taidan tweaks: %1
Requires: %name = %version-%release
Supplements: taidan-ultramarine-configs
%{?-p*}
%description tweaks-%1
Taidan tweaks: %1.
%files tweaks-%1
%_datadir/taidan/tweaks/%1
}

%tweak cachyos-kernel
%tweak mtu-probing

%prep
%git_clone https://github.com/Ultramarine-Linux/taidan main

%install
mkdir -p %buildroot%_datadir/taidan
cp -r data/tweaks/ %buildroot%_datadir/taidan/

%files
%license LICENSE.md
%dir %_datadir/taidan/
%dir %_datadir/taidan/tweaks/
