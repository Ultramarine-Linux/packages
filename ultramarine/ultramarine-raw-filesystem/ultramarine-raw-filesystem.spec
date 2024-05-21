Name:           ultramarine-raw-filesystem
Version:        1.0
Release:        2%{?dist}
Summary:        Automatically extend the root filesystem on raw images
URL:            ultramarine-linux.org
Source0:        grow-root.service
Source1:        grow-root.sh
License:        MIT
BuildArch:      noarch

%description
%{summary}

%prep

%build

%install
cp -v %{SOURCE0} %{buildroot}/etc/systemd/system
cp -v %{SOURCE1} %{buildroot}/sbin

%files
/etc/systemd/system/grow-root.service
/sbin/grow-root.sh

%changelog
* Tue May 21 2024 Jaiden Riordan <jade@fyralabs.com>
- Switch to custom script
* Mon May 20 2024 Jaiden Riordan <jade@fyralabs.com>
- Initial commit