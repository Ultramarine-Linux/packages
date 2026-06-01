Name:           budgie-sddm-switch
Version:        1.0
Release:        1%{?dist}
Summary:        LightDM/Slick config + SDDM switching for Ultramarine Budgie

License:        GPL-3.0-or-later
URL:            https://ultramarine-linux.org
Source0:        slick-greeter-budgie.conf
Source1:        sddm-warning.sh
Source2:        switch2sddm.sh
Source3:        sddm-warning.desktop

Requires:       ultramarine-budgie-filesystem bash sddm libnotify xdg-utils
Requires:       ultramarine-release-identity-budgie >= 43

%description
This package is for the LightDM->SDDM switch on Budgie Edition in UM44, we don't automatically migrate users, so this package exists to avoid breaking systems.

This package does 3 things:
- Provides the Budgie LightDM configs
- Notifies the user on every login that they should switch to SDDM
- Gives the user a command to switch to SDDM and stop the notifications

%install
install -Dm644 %{SOURCE0} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-budgie-slick-greeter.conf
install -Dm755 %{SOURCE1} %{buildroot}%{_libexecdir}/sddm-warning
install -Dm755 %{SOURCE2} %{buildroot}%{_bindir}/switch2sddm
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/xdg/autostart/sddm-warning.desktop

%files
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-budgie-slick-greeter.conf
%{_libexecdir}/sddm-warning
%{_sbindir}/switch2sddm
%{_sysconfdir}/xdg/autostart/sddm-warning.desktop



%changelog
* Sun May 31 2025 Jaiden Riordan <jade@fyralabs.com> - 1
- Initial package
