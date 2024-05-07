Name:           ultramarine-mock-configs
Version:        1.2
Release:        1%{?dist}
Summary:        Mock configs for`ultramarine-linux`

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        ultramarine-35-x86_64.cfg
Source2:        ultramarine.tpl
Source3:        ultramarine-testing.tpl
Source4:        ultramarine-36-x86_64.cfg
Source5:        ultramarine-37-x86_64.cfg
Source6:        ultramarine-37-aarch64.cfg
Source7:        ultramarine-38-x86_64.cfg
Source8:        ultramarine-38-aarch64.cfg
Source9:        ultramarine-39-x86_64.cfg
Source10:       ultramarine-39-aarch64.cfg
Source11:       ultramarine-40-x86_64.cfg
Source12:       ultramarine-40-aarch64.cfg
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

%files
/etc/mock/*
/etc/mock/templates/*

%changelog
* Thu Mar 07 2024 Lleyton Gray <lleyton@fyralabs.com>
- Add configs for 40
* Fri Oct 07 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial package release
