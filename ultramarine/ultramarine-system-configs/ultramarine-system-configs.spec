Name:           ultramarine-system-configs
Version:        1.1
Release:        1%{?dist}
Summary:        Various configuration files for a more comfortable Ultramarine desktop experience
BuildArch:      noarch
License:        MIT
URL:            https://ultramarine-linux.org
Source2:        ultramarine-logrotate.conf
Source3:        networking-tweaks.conf
Source4:        bbr.conf
Source5:        50-mtu-probing.conf

BuildRequires:  /usr/bin/install

%package core
Summary:        Core system tweaks for Ultramarine Linux

%description core
This package provides various systemd configurations that improve system performance
and resource usage on Ultramarine Linux.

%package desktop
Summary:        Desktop-specific tweaks for Ultramarine Linux

%description desktop
This package provides various systemd configurations that optimize desktop resource usage
and performance on Ultramarine Linux.


%description
This package provides various systemd configurations
to optimize desktop resource usage and performance on Ultramarine Linux.

The configs attempt to reduce disk usage for journaling and logging, and
cleaning up of unused temporary files periodically.

%prep

%build



%install
install -Dm644 %{SOURCE2} %{buildroot}/etc/logrotate.d/ultramarine-logrotate.conf
install -Dm644 %{SOURCE3} %{buildroot}/etc/sysctl.d/50-networking-tweaks.conf
install -Dm644 %{SOURCE4} %{buildroot}/etc/modules-load.d/bbr.conf
install -Dm644 %{SOURCE5} %{buildroot}/etc/sysctl.d/50-mtu-probing.conf

%files


%files core
%defattr(-,root,root,-)
%config /etc/sysctl.d/50-networking-tweaks.conf
%config /etc/modules-load.d/bbr.conf

%files desktop
%defattr(-,root,root,-)
%config /etc/logrotate.d/ultramarine-logrotate.conf
%config /etc/sysctl.d/50-mtu-probing.conf

%changelog
* Sat Aug 03 2024 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
