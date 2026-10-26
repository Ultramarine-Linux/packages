Name:           ultramarine-system-configs
Version:        45
Release:        2%{?dist}
Summary:        Various configuration files for a more comfortable Ultramarine desktop experience
BuildArch:      noarch
License:        MIT OR GFDL-1.1-or-later
URL:            https://ultramarine-linux.org
Source2:        ultramarine-logrotate.conf
Source3:        networking-tweaks.conf
Source4:        bbr.conf
Source5:        50-mtu-probing.conf
Source6:        ultramarine-default-bookmarks.html
Source7:        GFDL-1.1-or-later.txt
Source8:        scx_loader.toml

BuildRequires:  /usr/bin/install

%package core
Summary:        Core system tweaks for Ultramarine Linux
BuildArch:      noarch

%description core
This package provides various systemd configurations that improve system performance
and resource usage on Ultramarine Linux.

%package desktop
Summary:        Desktop-specific tweaks for Ultramarine Linux
BuildArch:      noarch

%description desktop
This package provides various systemd configurations that optimize desktop resource usage
and performance on Ultramarine Linux.

%package -n ultramarine-bookmarks
# Based on https://src.fedoraproject.org/rpms/fedora-bookmarks/blob/rawhide/f/fedora-bookmarks.spec
Summary:    Ultramarine default Firefox settings
License:    GFDL-1.1-or-later
BuildArch:  noarch
Provides:   system-bookmarks
Conflicts:  fedora-bookmarks
Obsoletes:  fedora-bookmarks
Obsoletes:  ultramarine-phony-bookmarks

%description -n ultramarine-bookmarks
This package contains the default Firefox bookmarks for Ultramarine.

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
install -Dm644 %{SOURCE6} %{buildroot}%{_datadir}/bookmarks/ultramarine-default-bookmarks.html
install -Dm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/scx_loader/config.toml
cp %{S:7} GFDL-1.1-or-later

%files

%files core
%defattr(-,root,root,-)
%config /etc/sysctl.d/50-networking-tweaks.conf
%config /etc/modules-load.d/bbr.conf

%files desktop
%defattr(-,root,root,-)
%config /etc/logrotate.d/ultramarine-logrotate.conf
%config /etc/sysctl.d/50-mtu-probing.conf
%dir %{_sysconfdir}/scx_loader
%config(noreplace) %{_sysconfdir}/scx_loader/config.toml

%files -n ultramarine-bookmarks
%license GFDL-1.1-or-later
# This folder is also needed for all browsers
%dir %{_datadir}/bookmarks
%{_datadir}/bookmarks/ultramarine-default-bookmarks.html

%changelog
* Mon Oct 26 2026 Cypress Reed <cypress@fyralabs.com>
- Ship scx_loader config, defaulting to scx_lavd

* Sat Aug 08 2026 Owen Zimmerman <owen@fyralabs.com>
- Add ultramarine-bookmarks subpackage

* Sat Aug 03 2024 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
