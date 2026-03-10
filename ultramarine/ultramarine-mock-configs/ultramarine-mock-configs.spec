Name:           ultramarine-mock-configs
Version:        1.3
Release:        3%{?dist}
Summary:        Mock configs for `ultramarine-linux`

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        ultramarine.tpl
Source1:        ultramarine-rawhide.tpl
Source2:        ultramarine-40-x86_64.cfg
Source3:        ultramarine-40-aarch64.cfg
Source4:        ultramarine-41-x86_64.cfg
Source5:        ultramarine-41-aarch64.cfg
Source6:        ultramarine-42-x86_64.cfg
Source7:        ultramarine-42-aarch64.cfg
Source8:        ultramarine-43-x86_64.cfg
Source9:        ultramarine-43-aarch64.cfg
Source10:       ultramarine-44-x86_64.cfg
Source11:       ultramarine-44-aarch64.cfg
Source12:       ultramarine-rawhide-x86_64.cfg
Source13:       ultramarine-rawhide-aarch64.cfg
Requires:       ultramarine-mock-gpg-keys
BuildArch:      noarch

%description
%{summary}

%prep

%build

%install
mkdir -p %{buildroot}/etc/mock/templates
cp -v %{SOURCE0} %{buildroot}/etc/mock
cp -v %{SOURCE2} %{buildroot}/etc/mock/templates
cp -v %{SOURCE3} %{buildroot}/etc/mock/templates
cp -v %{SOURCE4} %{buildroot}/etc/mock/
cp -v %{SOURCE5} %{buildroot}/etc/mock/
cp -v %{SOURCE6} %{buildroot}/etc/mock/
cp -v %{SOURCE7} %{buildroot}/etc/mock/
cp -v %{SOURCE8} %{buildroot}/etc/mock/
cp -v %{SOURCE9} %{buildroot}/etc/mock/
cp -v %{SOURCE10} %{buildroot}/etc/mock/
cp -v %{SOURCE11} %{buildroot}/etc/mock/
cp -v %{SOURCE12} %{buildroot}/etc/mock/
cp -v %{SOURCE13} %{buildroot}/etc/mock/
cp -v %{SOURCE14} %{buildroot}/etc/mock/
cp -v %{SOURCE15} %{buildroot}/etc/mock/
cp -v %{SOURCE16} %{buildroot}/etc/mock/

%files
/etc/mock/*
/etc/mock/templates/*

%changelog
* Sat Mar 15 2025 madonuko <mado@fyralabs.com>
- Add configs for 42
* Wed Aug 08 2024 madonuko <mado@fyralabs.com>
- Add configs for 41
* Thu Mar 07 2024 Lleyton Gray <lleyton@fyralabs.com>
- Add configs for 40
* Fri Oct 07 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial package release
