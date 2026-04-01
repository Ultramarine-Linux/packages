# These configuration files and specs are based off of:
# - https://learn.microsoft.com/en-us/windows/wsl/build-custom-distro
# - https://src.fedoraproject.org/rpms/wsl-setup/blob/rawhide
# - https://salsa.debian.org/debian/WSL

Name:           ultramarine-wsl-filesystem
Version:        %{?fedora}
Release:        1%{?dist}
Summary:        Ultramarine for WSL configuration files
URL:            ultramarine-linux.org

Source0:        wsl.conf
Source1:        wsl-distribution.conf
Source2:        oobe.sh
Source3:        wsl-filesystem-tmpfiles.conf
Source4:        wsl-filesystem-user-tmpfiles.conf

Requires:       system-logos

BuildRequires:  systemd-rpm-macros

License:        MIT
BuildArch:      noarch

%description
%{summary}

%prep

%build

%install
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/ %{SOURCE0}
install -Dpm0644 -t %{buildroot}%{_prefix}/lib/ %{SOURCE1}
install -Dpm0755 -T %{SOURCE2} %{buildroot}%{_libexecdir}/wsl/oobe.sh
ln -s ..%{_prefix}/lib/wsl-distribution.conf %{buildroot}%{_sysconfdir}/wsl-distribution.conf

# While WSL does not support systemd-tmpfiles, we're going to use it as that is what Fedora does as well.
# This workaround should make tmpfiles work as expected, while still supporting WSLg (graphical application integration)
install -Dpm0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -Dpm0644 %{SOURCE4} %{buildroot}%{_user_tmpfilesdir}/%{name}.conf

%files
%config(noreplace) %{_sysconfdir}/wsl.conf
%{_prefix}/lib/wsl-distribution.conf
%{_sysconfdir}/wsl-distribution.conf
%{_libexecdir}/wsl/oobe.sh
%{_tmpfilesdir}/%{name}.conf
%{_user_tmpfilesdir}/%{name}.conf

%changelog
* Mon Apr 24 2025 Lleyton Gray <lleyton@fyralabs.com>
- Initial commit
