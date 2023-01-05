Name:       ultramarine-obsolete-packages
Version:    37
Release:    1
Summary:    A package to obsolete retired Ultramarine packages

License:    LicenseRef-Fedora-Public-Domain
BuildArch:  noarch

Source0:    README

Obsoletes:  budgie-desktop-schemas < 10.6.3-3
Obsoletes:  budgie-desktop-libs < 10.6.3-3

%description
This package exists only to obsolete other packages which need to be removed
from the distribution.

%prep
%autosetup -c -T
cp %SOURCE0 .

%files
%doc README
