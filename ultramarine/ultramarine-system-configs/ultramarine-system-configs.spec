# Dashboard image shipped as a bootc logically bound image. Replace the
# placeholder digest once the dashboard CI publishes a release.
%global dashboard_image ghcr.io/ultramarine-linux/dashboard
%global dashboard_digest sha256:0000000000000000000000000000000000000000000000000000000000000000

Name:           ultramarine-system-configs
Version:        46
Release:        3%{?dist}
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
Source8:        80-ultramarine-server.preset
Source9:        ultramarine-dashboard.container

BuildRequires:  /usr/bin/install
BuildRequires:  systemd-rpm-macros

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

%package server
Summary:        Ultramarine Server default configuration
BuildArch:      noarch

%description server
This package provides the default service configuration for Ultramarine Server,
such as which system services are enabled out of the box.

%package server-dashboard
Summary:        Ultramarine Server dashboard container
BuildArch:      noarch
Requires:       podman

%description server-dashboard
This package provides the Quadlet for the Ultramarine Server dashboard and
registers its container image as a bootc logically bound image, so the image
is pulled alongside each deployment.

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
cp %{S:7} GFDL-1.1-or-later
install -Dm644 %{SOURCE8} %{buildroot}%{_presetdir}/80-ultramarine-server.preset
install -Dm644 %{SOURCE9} %{buildroot}%{_datadir}/containers/systemd/ultramarine-dashboard.container
sed -i -e 's|@DASHBOARD_IMAGE@|%{dashboard_image}|' -e 's|@DASHBOARD_DIGEST@|%{dashboard_digest}|' \
    %{buildroot}%{_datadir}/containers/systemd/ultramarine-dashboard.container
install -dm755 %{buildroot}%{_prefix}/lib/bootc/bound-images.d
ln -s ../../../share/containers/systemd/ultramarine-dashboard.container \
    %{buildroot}%{_prefix}/lib/bootc/bound-images.d/ultramarine-dashboard.container

# The preset may be installed after the packages owning these units, so apply
# it here as well as in their own scriptlets.
%post server
%systemd_post tetra.socket podman.socket

%files

%files core
%defattr(-,root,root,-)
%config /etc/sysctl.d/50-networking-tweaks.conf
%config /etc/modules-load.d/bbr.conf

%files desktop
%defattr(-,root,root,-)
%config /etc/logrotate.d/ultramarine-logrotate.conf
%config /etc/sysctl.d/50-mtu-probing.conf

%files server
%{_presetdir}/80-ultramarine-server.preset

%files server-dashboard
%{_datadir}/containers/systemd/ultramarine-dashboard.container
%dir %{_prefix}/lib/bootc/bound-images.d
%{_prefix}/lib/bootc/bound-images.d/ultramarine-dashboard.container

%files -n ultramarine-bookmarks
%license GFDL-1.1-or-later
# This folder is also needed for all browsers
%dir %{_datadir}/bookmarks
%{_datadir}/bookmarks/ultramarine-default-bookmarks.html

%changelog
* Sat Oct 17 2026 Cypress Reed <cypress@fyralabs.com>
- Add server and server-dashboard subpackages

* Sat Aug 08 2026 Owen Zimmerman <owen@fyralabs.com>
- Add ultramarine-bookmarks subpackage

* Sat Aug 03 2024 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
