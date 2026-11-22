Name:		ultramarine-niri-settings
Version:	0.1.0
Release:	1%{?dist}
Summary:	Default configuration for Ultramarine Niri

License:	GPL-3.0-or-later
URL:		https://github.com/Ultramarine-Linux/niri-settings
Source0:	%{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	niri
BuildRequires:	noctalia

Requires:	niri
Requires:	xwayland-satellite
Requires:	noctalia
Requires:	noctalia-greeter
Requires:	greetd
Requires:	alacritty
Requires:	xdg-terminal-exec
Requires:	nautilus-open-any-terminal
Requires:	adw-gtk3-theme
Requires:	ultramarine-backgrounds-compat

%description
%{summary}.

%prep
%autosetup -n niri-settings-%{version}

%build

%install
cp -a files/. %{buildroot}/
# default niri config but switch to noctalia and include ultramarine/noctalia niri configs
sed -e 's/^spawn-at-startup "waybar"$/spawn-at-startup "noctalia"/' \
    %{_docdir}/niri/default-config.kdl > %{buildroot}%{_sysconfdir}/niri/config.kdl
grep -q '^spawn-at-startup "noctalia"$' %{buildroot}%{_sysconfdir}/niri/config.kdl
cat >> %{buildroot}%{_sysconfdir}/niri/config.kdl <<'EOF'

include "ultramarine.kdl"
include "noctalia-binds.kdl"
EOF

%check
niri validate -c %{buildroot}%{_sysconfdir}/niri/config.kdl
noctalia config validate %{buildroot}%{_sysconfdir}/skel/.config/noctalia

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/niri
%config(noreplace) %{_sysconfdir}/niri/config.kdl
%config(noreplace) %{_sysconfdir}/niri/ultramarine.kdl
%config(noreplace) %{_sysconfdir}/niri/noctalia-binds.kdl
%config(noreplace) %{_sysconfdir}/xdg/niri-xdg-terminals.list
%dir %{_sysconfdir}/skel/.config
%{_sysconfdir}/skel/.config/niri/
%{_sysconfdir}/skel/.config/noctalia/
%{_datadir}/applications/niri-mimeapps.list
%{_datadir}/glib-2.0/schemas/60-ultramarine-niri.gschema.override

%changelog
* Sat Nov 21 2026 Its-J <jonah@fyralabs.com> - 0.1.0-1
- Initial package
