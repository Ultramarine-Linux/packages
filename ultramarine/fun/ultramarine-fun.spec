%define debug_package %nil

Name:			ultramarine-fun
Version:		40
Release:		1%?dist
Summary:		Additional secret/hidden files for ultramarine Linux
License:		MIT
URL:			https://ultramarine-linux.org
Source0:		secrets.tar.gz
BuildArch:      noarch
BuildRequires:	git-core

%description
%summary.

%prep
%autosetup -n secrets

%build

%install
mkdir -p %buildroot%_datadir/"Ultramarine Linux"/ultramarine/.cache
cp iloveyou.txt %buildroot%_datadir/"Ultramarine Linux"/
cp LICENSE AUTHORS CREDITS %buildroot%_datadir/"Ultramarine Linux"/ultramarine/
cp 18_8_15_4_5.txt cake %buildroot%_datadir/"Ultramarine Linux"/ultramarine/.cache/

%files
%_datadir/Ultramarine\ Linux/

%changelog
%autochangelog
