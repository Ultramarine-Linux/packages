Name:           ultramarine-systemd-presets
Version:        1
Release:        3%{?dist}
Summary:        Ultramarine systemd presets
URL:            https://src.fedoraproject.org/rpms/redhat-systemd-presets
License:        MIT

Source1:        LICENSE

# Common preset files
Source10:       85-display-manager.preset
Source11:       90-default.preset
Source12:       90-default-user.preset
Source13:       99-default-disable.preset

# Ultramarine exclusive preset files

Source20:       80-server.preset
Source21:       88-ultramarine-chromebook-default.preset
Source22:       91-ultramarine-surface-default.preset

# Desktop preset files
Source27:       81-desktop.preset

# Atomic desktop preset files
Source37:       81-atomic-desktop.preset

BuildRequires:  systemd-rpm-macros

BuildArch:      noarch

# Allow only one provider
Provides:       distribution-systemd-presets
Conflicts:      distribution-systemd-presets

Requires:       %{name}-common = %{version}-%{release}

%description
Ultramarine systemd preset files that determine which services are enabled by default.
# See https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/ for details.
# NOTE - this should still be in sync with upstream, and divert only as needed.

%files
%license LICENSE

%package common
Summary:        Common systemd presets for Ultramarine
# Ensures that this is considered merely a separation detail
Requires:       %{name} = %{evr}
# From the split from fedora-release
Conflicts:      ultramarine-release-common < 44-10
Obsoletes:      ultramarine-release-common < 44-10
# Allow only one provider
Provides:       distribution-systemd-presets-common
Conflicts:      distribution-systemd-presets-common

%description common
Ultramarine systemd preset files common to all distributions and variants
that determine which services are enabled by default.

%files common
%dir %{_presetdir}
%{_presetdir}/85-display-manager.preset
%{_presetdir}/90-default.preset
%{_presetdir}/99-default-disable.preset
%dir %{_userpresetdir}
%{_userpresetdir}/90-default-user.preset
%{_userpresetdir}/99-default-disable.preset

%package desktop
Summary:        Desktop systemd presets for the Red Hat family
Requires:       %{name}-common = %{version}-%{release}
# From the split from fedora-release
Conflicts:      ultramarine-release-common < 44-10
# Deal with all the identity flavors that had this file
%global ultramarine_flavor_obsoletes() \
Obsoletes:      ultramarine-release-identity-%{1} < 44-10

%ultramarine_flavor_obsoletes budgie
%ultramarine_flavor_obsoletes plasma
%ultramarine_flavor_obsoletes gnome
%ultramarine_flavor_obsoletes xfce

# Allow only one provider
Provides:       distribution-systemd-presets-desktop
Conflicts:      distribution-systemd-presets-desktop

%description desktop
Ultramarine systemd preset files for all desktop variants
that determine which services are enabled by default.

%files desktop
%{_presetdir}/81-desktop.preset

%package desktop-atomic
Summary:        Atomic Desktop systemd presets for Ultramarine
Requires:       %{name}-desktop = %{version}-%{release}
# These packages currently do not exist
%dnl Conflicts:      ultramarine-release-ostree-desktop < 45-0.5
%dnl Obsoletes:      ultramarine-release-ostree-desktop < 45-0.5
# Allow only one provider
Provides:       distribution-systemd-presets-desktop-atomic
Conflicts:      distribution-systemd-presets-desktop-atomic

%description desktop-atomic
Ultramarine systemd preset files for all atomic desktop variants
that determine which services are enabled by default.

%files desktop-atomic
%{_presetdir}/81-atomic-desktop.preset

%package chromebook
Summary:        Chromebook systemd presets for Ultramarine
Requires:       %{name}-common = %{evr}
# From the split from Ultramarine-release
Conflicts:      ultramarine-release-chromebook < 44-10
# Deal with all the identity flavors that had this file
Obsoletes:      ultramarine-release-chromebook < 44-10
# Allow only one provider
Provides:       distribution-systemd-presets-chromebook
Conflicts:      distribution-systemd-presets-chromebook

%description chromebook
Ultramarine systemd preset files for all chromebook variants
that determine which services are enabled by default.

%files chromebook
%{_presetdir}/88-ultramarine-chromebook-default.preset

%package server
Summary:        Server systemd presets for Ultramarine
Requires:       %{name}-common = %{evr}
# Allow only one provider
Provides:       distribution-systemd-presets-server
Conflicts:      distribution-systemd-presets-server

%description server
Ultramarine systemd preset files for all server variants
that determine which services are enabled by default.

%files server
%{_presetdir}/80-server.preset

%package surface
Summary:        Surface systemd presets for Ultramarine
Requires:       %{name}-common = %{evr}
# From the split from Ultramarine-release
Conflicts:      ultramarine-release-surface < 44-10
# Deal with all the identity flavors that had this file
Obsoletes:      ultramarine-release-surface < 44-10
# Allow only one provider
Provides:       distribution-systemd-presets-surface
Conflicts:      distribution-systemd-presets-surface

%description surface
Ultramarine systemd preset files for all surface variants
that determine which services are enabled by default.

%files surface
%{_presetdir}/91-ultramarine-surface-default.preset

%prep
%autosetup -T -c

%build

%install
install -pm 0644 %{SOURCE1} LICENSE

# Default system wide
install -Dm0644 %{SOURCE10} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE12} -t %{buildroot}%{_userpresetdir}/
# The same file is installed in two places with identical contents
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_userpresetdir}/

install -Dm0644 %{SOURCE20} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE21} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE22} -t %{buildroot}%{_presetdir}/

# Common desktop preset
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_presetdir}/

# Atomic Desktop specific preset
install -Dm0644 %{SOURCE37} -t %{buildroot}%{_presetdir}/


%changelog
* Mon Oct 26 2026 Cypress Reed <cypress@fyralabs.com> - 1-3
- Switch from System76 scheduler to scx
- Enable falcond.service

* Sat Oct 24 2026 Cypress Reed <cypress@fyralabs.com> - 1-2
- Enable ultramarine-updates-automatic.timer

* Tue Oct 20 2026 Owen Zimmerman <owen@fyralabs.com> - 1-1
- Initial commit, based on Fedora redhat-systemd-presets


%dnl %if %{with gnome} || %{with atomic_gnome}

%dnl %endif
