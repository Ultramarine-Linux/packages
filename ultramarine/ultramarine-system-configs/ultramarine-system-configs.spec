Name:           ultramarine-system-configs
Version:        1
Release:        1%{?dist}
Summary:        Various configuration files for a more comfortable Ultramarine desktop experience
BuildArch:      noarch
License:        MIT
URL:            https://ultramarine-linux.org
Source0:        journal-cleanup.conf
Source1:        tmpfiles-cleanup.conf
Source2:        ultramarine-logrotate.conf
Source3:        networking-tweaks.conf
Source4:        bbr.conf

BuildRequires:  /usr/bin/install
Requires:       systemd


%description
This package provides various systemd configurations
to optimize desktop resource usage and performance on Ultramarine Linux.

The configs attempt to reduce disk usage for journaling and logging, and
cleaning up of unused temporary files periodically.

%prep

%build



%install
install -Dm644 %{SOURCE0} %{buildroot}/etc/systemd/journald.conf.d/journal-cleanup.conf
install -Dm644 %{SOURCE1} %{buildroot}/etc/tmpfiles.d/tmpfiles-cleanup.conf
install -Dm644 %{SOURCE2} %{buildroot}/etc/logrotate.d/ultramarine-logrotate.conf
install -Dm644 %{SOURCE3} %{buildroot}/etc/sysctl.d/50-networking-tweaks.conf
install -Dm644 %{SOURCE4} %{buildroot}/etc/modules-load.d/bbr.conf

%files
%defattr(-,root,root,-)
%config /etc/systemd/journald.conf.d/journal-cleanup.conf
%config /etc/tmpfiles.d/tmpfiles-cleanup.conf
%config /etc/logrotate.d/ultramarine-logrotate.conf
%config /etc/sysctl.d/50-networking-tweaks.conf
%config /etc/modules-load.d/bbr.conf



%changelog
* Sat Aug 03 2024 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
