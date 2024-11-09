%define debug_package %nil

Name:       dnf5-default-package-manager
Version:    0
Release:    3%?dist
Summary:    Package that sets dnf5 as the default package manager
License:    MIT
URL:        https://wiki.ultramarine-linux.org/en/usage/um40-dnf5/
Requires:   dnf5
Recommends: dnf5-plugins
BuildArch:  noarch

%description
This package contains post-install hooks that symlinks %_bindir/dnf
to the new dnf5 binary.

%prep
touch .placeholder

%build

%install

%posttrans
if [ $1 -gt 1 ]; then
  rm %_bindir/{dnf,yum}
  ln -s %_bindir/dnf5 /usr/bin/dnf
  ln -s %_bindir/dnf5 /usr/bin/yum
fi

%preun
echo
echo "dnf5-default-package-manager will be uninstalled."
echo "If you want to revert the symlinks, run the following commands:"
echo "rm %_bindir/{dnf,yum}"
echo "ln -s /usr/bin/dnf-3 /usr/bin/dnf"
echo "ln -s %_bindir/dnf-3 /usr/bin/yum"
echo "For more information, visit: %url"
echo

%triggerin -- dnf
rm %_bindir/{dnf,yum}
ln -s %_bindir/dnf5 /usr/bin/dnf
ln -s %_bindir/dnf5 /usr/bin/yum

%triggerin -- yum
rm %_bindir/{dnf,yum}
ln -s %_bindir/dnf5 /usr/bin/dnf
ln -s %_bindir/dnf5 /usr/bin/yum

%files
%doc .placeholder
