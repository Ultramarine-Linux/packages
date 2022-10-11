%undefine _disable_source_fetch

Name:           fluent-icon-theme
Version:        031021
Release:        1%{?dist}
Summary:        Fluent is a Fluent design theme for GNOME/GTK based desktop environments.

License:        GPLv3
URL:            https://github.com/vinceliuice/Fluent-icon-theme/
Source0:        %{url}/archive/refs/tags/2021-10-07.tar.gz

BuildRequires:  gtk-update-icon-cache

%description
Qogir is a flat Design theme for GTK 3, GTK 2 and Gnome-Shell which supports GTK 3 and GTK 2 based desktop environments like Gnome, Unity, Budgie, Cinnamon Pantheon, XFCE, Mate, etc.

%prep
%autosetup -n Fluent-icon-theme-2021-10-07


#%build
#./parse-sass.sh



%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/themes
./install.sh -r -a -d %{buildroot}%{_datadir}/icons

%files
%license COPYING
%doc README.md

%{_datadir}/icons/Fluent*/

%changelog
* Sat Nov 13 2021 korewaChino <cappy@cappuchino.xyz>
- initial release
