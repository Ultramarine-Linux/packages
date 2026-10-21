Name:           ultramarine-system-configs-server
Version:        46
Release:        1%{?dist}
Summary:        Ultramarine Server default configuration
BuildArch:      noarch
License:        MIT
URL:            https://ultramarine-linux.org
Source0:        80-ultramarine-server.preset
Source1:        ultramarine-caddy-admin.conf
Source2:        ultramarine-server.sysusers
Source3:        ultramarine-server-automatic.conf
Source4:        ultramarine-snapper.actions
Source5:        ultramarine-prune-boot-entries
Source6:        ultramarine-snapper-filters.txt

BuildRequires:  /usr/bin/install
BuildRequires:  systemd-rpm-macros
# Reads the automatic.conf shipped here to update mutable installs
Requires:       dnf5-plugin-automatic
# Runs the snapper hook in ultramarine-snapper.actions
Requires:       libdnf5-plugin-actions

%description
This package provides the default service configuration for Ultramarine Server,
such as which system services are enabled out of the box.

%prep

%build

%install
install -Dm644 %{SOURCE0} %{buildroot}%{_presetdir}/80-ultramarine-server.preset
install -Dm644 %{SOURCE1} %{buildroot}%{_unitdir}/caddy.service.d/50-ultramarine-admin-socket.conf
install -Dm644 %{SOURCE2} %{buildroot}%{_sysusersdir}/ultramarine-server.conf
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dnf/automatic.conf
install -Dm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnf/libdnf5-plugins/actions.d/ultramarine-snapper.actions
install -Dm755 %{SOURCE5} %{buildroot}%{_bindir}/ultramarine-prune-boot-entries
install -Dm644 %{SOURCE6} %{buildroot}%{_datadir}/snapper/filters/ultramarine-server.txt

%post
%systemd_post tetra.socket podman.socket dnf5-automatic.timer snapper-cleanup.timer

%files
%{_presetdir}/80-ultramarine-server.preset
%dir %{_unitdir}/caddy.service.d
%{_unitdir}/caddy.service.d/50-ultramarine-admin-socket.conf
%{_sysusersdir}/ultramarine-server.conf
%config(noreplace) %{_sysconfdir}/dnf/automatic.conf
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/actions.d/ultramarine-snapper.actions
%{_bindir}/ultramarine-prune-boot-entries
%dir %{_datadir}/snapper
%dir %{_datadir}/snapper/filters
%{_datadir}/snapper/filters/ultramarine-server.txt

%changelog
* Wed Oct 21 2026 Cypress Reed <cypress@fyralabs.com>
- Split out of ultramarine-system-configs
- Move the Caddy admin API to a Unix socket
- Create the ultramarine-admin group
- Apply updates automatically on mutable installs
- Snapshot the root filesystem around dnf transactions on mutable installs
- Add ultramarine-prune-boot-entries for cleaning up after a rollback
- Keep accounts and local config out of snapper rollbacks
