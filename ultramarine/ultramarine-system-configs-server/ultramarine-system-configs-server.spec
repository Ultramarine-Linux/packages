Name:           ultramarine-system-configs-server
Version:        45
Release:        1%{?dist}
Summary:        Ultramarine Server default configuration
BuildArch:      noarch
License:        MIT
URL:            https://ultramarine-linux.org
Source0:        ultramarine-caddy-admin.conf
Source1:        ultramarine-server.sysusers
Source2:        ultramarine-server-automatic.conf
Source3:        ultramarine-snapper.actions
Source4:        ultramarine-prune-boot-entries
Source5:        ultramarine-snapper-filters.txt
Source6:        LICENCE.txt

BuildRequires:  /usr/bin/install
BuildRequires:  systemd-rpm-macros
# Reads the automatic.conf shipped here to update mutable installs
Requires:       dnf5-plugin-automatic
# Runs the snapper hook in ultramarine-snapper.actions
Requires:       libdnf5-plugin-actions
# Enables the server's services (Tetra, the Podman socket, automatic updates, snapper cleanup)
Requires:       ultramarine-systemd-presets-server

%description
This package provides the default service configuration for Ultramarine Server,
such as which system services are enabled out of the box.

%prep

%build

%install
install -Dm644 %{SOURCE0} %{buildroot}%{_unitdir}/caddy.service.d/50-ultramarine-admin-socket.conf
install -Dm644 %{SOURCE1} %{buildroot}%{_sysusersdir}/ultramarine-server.conf
install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/dnf/automatic.conf
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dnf/libdnf5-plugins/actions.d/ultramarine-snapper.actions
install -Dm755 %{SOURCE4} %{buildroot}%{_bindir}/ultramarine-prune-boot-entries
install -Dm644 %{SOURCE5} %{buildroot}%{_datadir}/snapper/filters/ultramarine-server.txt
cp %{S:6} .

%post
%systemd_post tetra.socket podman.socket dnf5-automatic.timer snapper-cleanup.timer

%files
%dir %{_unitdir}/caddy.service.d
%{_unitdir}/caddy.service.d/50-ultramarine-admin-socket.conf
%{_sysusersdir}/ultramarine-server.conf
%config(noreplace) %{_sysconfdir}/dnf/automatic.conf
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/actions.d/ultramarine-snapper.actions
%{_bindir}/ultramarine-prune-boot-entries
%dir %{_datadir}/snapper
%dir %{_datadir}/snapper/filters
%{_datadir}/snapper/filters/ultramarine-server.txt
%license LICENCE.txt

%changelog
* Wed Oct 21 2026 Cypress Reed <cypress@fyralabs.com>
- Split out of ultramarine-system-configs
- Move the server preset to ultramarine-systemd-presets-server
- Move the Caddy admin API to a Unix socket
- Create the ultramarine-admin group
- Apply updates automatically on mutable installs
- Snapshot the root filesystem around dnf transactions on mutable installs
- Add ultramarine-prune-boot-entries for cleaning up after a rollback
- Keep accounts and local config out of snapper rollbacks
