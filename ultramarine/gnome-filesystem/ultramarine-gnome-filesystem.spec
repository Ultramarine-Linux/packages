Name:           ultramarine-gnome-filesystem
Version:        0.1.2
Release:        1%{?dist}
Summary:        GNOME settings for Ultramarine Linux

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        50_ultramarine-gnome.gschema.override

%description
%summary



%install
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install %{SOURCE0} %{buildroot}%{_datadir}/glib-2.0/schemas/

%files
%{_datadir}/glib-2.0/schemas/50_ultramarine-gnome.gschema.override



%changelog
* Thu May 19 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- owo
