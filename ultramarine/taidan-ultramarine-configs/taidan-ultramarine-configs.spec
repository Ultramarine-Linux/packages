Name:           taidan-ultramarine-configs
Version:        46
Release:        5%?dist
Summary:        Taidan configuration for Ultramarine
License:        (MIT AND GPL-3.0-or-later)
Provides:       taidan-configs
Provides:       initial-setup initial-setup-gui
Conflicts:      taidan-default-configs
Obsoletes:      taidan-default-configs <= 999

BuildArch:      noarch
Source0:        detect-internet

%description
This package provides the Taidan configuration files for Ultramarine Linux.

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

%tweak cachyos-kernel -p %{quote:BuildArch: x86_64_v3}
%tweak mtu-probing

%prep
%git_clone https://github.com/Ultramarine-Linux/taidan main

%install
install -Dpm755 %{S:0} -t %buildroot%_sysconfdir/com.fyralabs.Taidan
mkdir -p %buildroot%_datadir/taidan
cp -r data/tweaks/ %buildroot%_datadir/taidan/

%files
%license LICENSE.md
%config %_sysconfdir/com.fyralabs.Taidan/
