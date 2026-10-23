# Dashboard image shipped as a bootc logically bound image, pinned by digest so
# the dashboard always matches the OS release. update.rhai bumps the digest.
%global dashboard_image ghcr.io/ultramarine-linux/dashboard
%global dashboard_digest sha256:0000000000000000000000000000000000000000000000000000000000000000

# Fixed UID/GID of the ultramarine-dashboard account. The Quadlet runs the
# container under these numeric IDs and Tetra identifies the dashboard by its
# UID, so they cannot be allocated dynamically. 0-200 is reserved for Fedora's
# static IDs (setup's uidgid list), and sysusers/useradd allocate dynamic system
# IDs downwards from 999, so take one from the bottom of 201-999 where neither
# should land.
%global dashboard_id 300
# Fixed GID of the tetra group (tetra's sysusers file), which owns
# /run/tetra/tetra.sock.
%global tetra_gid 241

Name:           ultramarine-server-dashboard
Version:        0.0.0
Release:        1%{?dist}
Summary:        Web dashboard for Ultramarine Server
License:        AGPL-3.0-or-later
URL:            https://github.com/Ultramarine-Linux/dashboard
Source0:        ultramarine-dashboard.container
Source1:        ultramarine-server-dashboard.sysusers
Source2:        ultramarine-server-dashboard.tmpfiles
Source3:        https://raw.githubusercontent.com/Ultramarine-Linux/dashboard/main/LICENSE

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros

Requires:       podman
Requires:       tetra

Packager:       Cypress Reed <cypress@fyralabs.com>

%description
This package provides the Quadlet for the Ultramarine Server dashboard and
registers its container image as a bootc logically bound image, so the image
is pulled alongside each deployment.

%prep

%build

%install
install -Dpm644 %{SOURCE0} %{buildroot}%{_datadir}/containers/systemd/ultramarine-dashboard.container
sed -i \
    -e 's|@DASHBOARD_IMAGE@|%{dashboard_image}|' \
    -e 's|@DASHBOARD_DIGEST@|%{dashboard_digest}|' \
    -e 's|@DASHBOARD_ID@|%{dashboard_id}|g' \
    -e 's|@TETRA_GID@|%{tetra_gid}|' \
    %{buildroot}%{_datadir}/containers/systemd/ultramarine-dashboard.container
install -dm755 %{buildroot}%{_prefix}/lib/bootc/bound-images.d
ln -s ../../../share/containers/systemd/ultramarine-dashboard.container \
    %{buildroot}%{_prefix}/lib/bootc/bound-images.d/ultramarine-dashboard.container

install -Dpm644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
sed -i 's|@DASHBOARD_ID@|%{dashboard_id}|' %{buildroot}%{_sysusersdir}/%{name}.conf
install -Dpm644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# Container environment, rewritten by Tetra (e.g. ORIGIN once the server's
# hostname is set).
install -Dpm644 /dev/null %{buildroot}%{_sysconfdir}/ultramarine-dashboard/env

cp %{S:3} LICENSE

%files
%license LICENSE
%dir %{_sysconfdir}/ultramarine-dashboard
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/ultramarine-dashboard/env
%{_datadir}/containers/systemd/ultramarine-dashboard.container
%dir %{_prefix}/lib/bootc/bound-images.d
%{_prefix}/lib/bootc/bound-images.d/ultramarine-dashboard.container
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%ghost %dir %attr(0700, ultramarine-dashboard, ultramarine-dashboard) %{_sharedstatedir}/ultramarine-dashboard

%changelog
* Sun Oct 18 2026 Cypress Reed <cypress@fyralabs.com>
- Initial package release
