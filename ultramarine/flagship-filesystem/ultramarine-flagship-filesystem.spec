Name:           ultramarine-flagship-filesystem
Version:        39
Release:        5.1%{?dist}
Summary:        Assets for Ultramarine Linux Flagship

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        01_ultramarine-budgie.gschema.override
Source1:        ultramarine-marina.layout

Requires:       budgie-desktop
Requires:       budgie-extras
Requires:       budgie-extras-daemon
Suggests:       fluent-theme
#Suggests:       papirus-icon-theme
Requires:       tau-hydrogen
Requires:       rsms-inter-fonts

%description

%install
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install %{SOURCE0} %{buildroot}%{_datadir}/glib-2.0/schemas/

mkdir -p %{buildroot}%{_datadir}/budgie-desktop/layouts/
install %{SOURCE1} %{buildroot}%{_datadir}/budgie-desktop/layouts/
install %{SOURCE1} %{buildroot}%{_datadir}/budgie-desktop/panel.ini


%files
%{_datadir}/glib-2.0/schemas/01_ultramarine-budgie.gschema.override
%{_datadir}/budgie-desktop/layouts/ultramarine-marina.layout
%{_datadir}/budgie-desktop/panel.ini



%changelog
* Wed Jun 08 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 0.1.1
- Updated layouts and config files

* Wed May 18 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
