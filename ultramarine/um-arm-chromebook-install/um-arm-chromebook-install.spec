Name:           um-arm-chromebook-install
Version:        1.0.0
Release:        1%?dist
Summary:        Shell script to install Ultramarine ARM Chromebook preinstalled images to Chromebook's internal disks
License:        GPLv3
URL:            https://github.com/Ultramarine-Linux/arm-chromebook-install
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Requires:       bash
Requires:       submarine
Requires:       vboot-utils
BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n arm-chromebook-install-%{version}

%install
install -Dm 755 um-arm-chromebook-install.sh %{buildroot}%{_bindir}/um-arm-chromebook-install

%files
%doc README.md
%license LICENSE
%{_bindir}/um-arm-chromebook-install

%changelog
* Sun Oct 05 2025 Owen Zimmerman <owen@fyralabs.com>
- Initial commit

