Name:           ultramarine-mock-configs
Version:        1.3
Release:        1%{?dist}
Summary:        Mock configs for Ultramarine Linux

License:        MIT
URL:            https://ultramarine-linux.org
Source0:        https://github.com/Ultramarine-Linux/mock-configs/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch

%description
%{summary}

%prep
%autosetup -n mock-configs-%{version}

%build

%install
mkdir -p %{buildroot}/etc/mock/templates
cp -v ./*.tpl -t %{buildroot}/etc/mock/templates
cp -v ./*.cfg -t %{buildroot}/etc/mock/

%files
/etc/mock/*.cfg
/etc/mock/templates/*

%changelog
* Sun Oct 19 2025 Owen Zimmerman <owen@fyralabs.com>
- Add configs for 43
* Sat Mar 15 2025 madonuko <mado@fyralabs.com>
- Add configs for 42
* Wed Aug 08 2024 madonuko <mado@fyralabs.com>
- Add configs for 41
* Thu Mar 07 2024 Lleyton Gray <lleyton@fyralabs.com>
- Add configs for 40
* Fri Oct 07 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial package release
