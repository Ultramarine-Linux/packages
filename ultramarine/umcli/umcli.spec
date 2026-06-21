%define debug_package %nil
# https://github.com/Ultramarine-Linux/um
%global goipath         github.com/Ultramarine-Linux/um

%global godocs          README.md

Name:           umcli
Version:        0.4.5
Release:        2%dist
Summary:        A CLI tool for managing an Ultramarine Linux system

License:        GPL-3.0-or-later
URL:            %{gourl}
Source:         https://github.com/Ultramarine-Linux/um/archive/v%version.tar.gz
Provides:       golang-github-ultramarine-linux-um
BuildRequires:  git-core
BuildRequires:  pkgconfig(rpm)
BuildRequires:  pkgconfig(flatpak)
Requires:	ansible-core
Requires:	ansible-collection-ansible-posix
Requires:	ansible-collection-community-general

Obsoletes: golang-github-ultramarine-linux-um <= 0.4.5

%description
%summary.

%gopkg

%prep
%autosetup -n um-%version
go mod download

%build
mkdir -p build/bin
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -s -w" -buildmode=pie -o %{gobuilddir}/bin/um %{goipath}

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/um
cp -av data/. %{buildroot}%{_datadir}/um/.

%check
%gocheck

%files
%doc README.md
%{_bindir}/um
%{_datadir}/um/

%changelog
* Sun January 18 2026 Jaiden Riordan <jade@fyralabs.com> - 0.4.5-2
- Rename and cleanup spec
