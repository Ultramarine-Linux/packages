Name:           ultramarine-budgie-filesystem
Version:        46
Release:        1%{?dist}
Summary:        Assets for Ultramarine Linux Budgie

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        40_ultramarine-budgie.gschema.override
Source1:        ultramarine-marina.layout

Requires:       budgie-desktop
Requires:       budgie-applet-visualspace
Recommends:     budgie-extras
Suggests:       fluent-theme
Suggests:       fluent-icon-theme
Requires:       fyra-labs-natrium-fonts
Requires:       fyra-labs-natrium-mono-fonts

Provides:       budgie-desktop-defaults
Conflicts:      budgie-desktop-defaults

Obsoletes:      ultramarine-flagship-filesystem < 43-3

%description

%install
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install %{SOURCE0} %{buildroot}%{_datadir}/glib-2.0/schemas/

mkdir -p %{buildroot}%{_datadir}/budgie-desktop/layouts/
install %{SOURCE1} %{buildroot}%{_datadir}/budgie-desktop/layouts/
install %{SOURCE1} %{buildroot}%{_datadir}/budgie-desktop/panel.ini


%files
%{_datadir}/glib-2.0/schemas/40_ultramarine-budgie.gschema.override
%{_datadir}/budgie-desktop/layouts/ultramarine-marina.layout
%{_datadir}/budgie-desktop/panel.ini



%changelog
* Fri Apr 11 2025 Jaiden Riordan <jade@fyralabs.com> - 7
- Fix the missing logo on start menu

* Wed Jun 08 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 0.1.1
- Updated layouts and config files

* Wed May 18 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
