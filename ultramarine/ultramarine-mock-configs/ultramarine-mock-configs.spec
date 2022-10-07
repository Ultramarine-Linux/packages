Name:           ultramarine-mock-configs
Version:        1.0
Release:        1%{?dist}
Summary:        Ultramarine Linux mock configs

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        ultramarine-35-x86_64.cfg
Source2:        ultramarine.tpl
Source3:        ultramarine-testing.tpl
Source4:        ultramarine-36-x86_64.cfg
Source5:        ultramarine-37-x86_64.cfg
BuildArch:      noarch

%description


%prep


%build


%install
mkdir -p %{buildroot}/etc/mock/templates
cp -v %{SOURCE0} %{buildroot}/etc/mock
cp -v %{SOURCE2} %{buildroot}/etc/mock/templates
cp -v %{SOURCE3} %{buildroot}/etc/mock/templates
cp -v %{SOURCE4} %{buildroot}/etc/mock/
cp -v %{SOURCE5} %{buildroot}/etc/mock/


%files
/etc/mock/*
/etc/mock/templates/*



%changelog
* Fri Oct 07 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- 
