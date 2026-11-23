Name:		ultramarine-niri-settings
Version:	0.1.1
Release:	1%{?dist}
Summary:	Default configuration for Ultramarine Niri

License:	GPL-3.0-or-later
URL:		https://github.com/Ultramarine-Linux/%{name}
Source0:	%{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	make
BuildRequires:	systemd-rpm-macros

Requires:	niri
Requires:	noctalia
Requires:	noctalia-greeter

%description
%{summary}.

%prep
%autosetup

%build

%install
%make_install

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/niri
%config(noreplace) %{_sysconfdir}/niri/config.kdl
%config(noreplace) %{_sysconfdir}/xdg/niri-xdg-terminals.list
%config(noreplace) %{_sysconfdir}/greetd/ultramarine-niri.toml
%dir %{_unitdir}/greetd.service.d
%{_unitdir}/greetd.service.d/ultramarine-niri.conf
%{_sysconfdir}/skel/.config/niri/
%{_sysconfdir}/skel/.config/noctalia/
%{_datadir}/applications/niri-mimeapps.list
%{_datadir}/glib-2.0/schemas/60-ultramarine-niri.gschema.override
%{_datadir}/ultramarine-niri/

%changelog
* Sat Nov 21 2026 Its-J <jonah@fyralabs.com> - 0.1.1-1
- Initial package
