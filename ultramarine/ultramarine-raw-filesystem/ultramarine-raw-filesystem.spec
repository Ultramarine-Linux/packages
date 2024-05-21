Name:           ultramarine-raw-filesystem
Version:        1.0
Release:        1%{?dist}
Summary:        systemd-repart config to automatically extend the root filesystem on raw images
URL:            ultramarine-linux.org
Source0:        50-root.conf
License:        MIT
BuildArch:      noarch

%description
%{summary}

%prep

%build

%install
mkdir -p %{buildroot}/usr/lib/repart.d
cp -v %{SOURCE0} %{buildroot}/usr/lib/repart.d


%files
/usr/lib/repart.d/*

%changelog
* Mon May 20 2024 Jaiden Riordan <jade@fyralabs.com>
- Initial commit