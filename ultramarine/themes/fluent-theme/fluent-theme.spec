
Name:           fluent-theme
Version:        20220615
Release:        1%{?dist}
Summary:        Fluent is a Fluent design theme for GNOME/GTK based desktop environments.

License:        GPLv3
URL:            https://github.com/vinceliuice/Fluent-gtk-theme
Source0:        https://github.com/vinceliuice/Fluent-gtk-theme/archive/refs/tags/2022-06-15.tar.gz

BuildRequires:  sassc
Requires:       gtk-murrine-engine

%description
Qogir is a flat Design theme for GTK 3, GTK 2 and Gnome-Shell which supports GTK 3 and GTK 2 based desktop environments like Gnome, Unity, Budgie, Cinnamon Pantheon, XFCE, Mate, etc.

%prep
%autosetup -n Fluent-gtk-theme-2022-06-15


#%build
#./parse-sass.sh



%install
./parse-sass.sh
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/themes
./install.sh --tweaks round -d %{buildroot}%{_datadir}/themes

%files
%license COPYING
%doc README.md

%{_datadir}/themes/Fluent*/



%changelog
* Tue Oct 11 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 20220605-1
- Update to 2022-06-15
- Change versioning scheme to YYYYMMDD

* Sat Nov 13 2021 korewaChino <cappy@cappuchino.xyz>
- initial release
