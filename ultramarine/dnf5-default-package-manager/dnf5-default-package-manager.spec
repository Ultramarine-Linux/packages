%define debug_package %nil

Name:       dnf5-default-package-manager
Version:    0
Release:    1%?dist
Summary:    Package that sets dnf5 as the default package manager
License:    MIT
URL:        https://wiki.ultramarine-linux.org/en/usage/um40-dnf5/
Requires:   dnf5

%description
This package contains post-install hooks that symlinks %_bindir/dnf
to the new dnf5 binary.

%prep
cat<<EOF > README
The `%name` package replaces `%_bindir/dnf` and `%_bindir/yum` to
point to `%_bindir/dnf5`. For more information, please visit:
%url
EOF

%build

%install

%posttrans
if [ $1 -gt 1 ]; then
  rm %_bindir/{dnf,yum}
  ln -s %_bindir/dnf5 /usr/bin/dnf
  ln -s %_bindir/dnf5 /usr/bin/yum
fi

%preun
rm %_bindir/{dnf,yum}
ln -s /usr/bin/dnf-3 /usr/bin/dnf
ln -s %_bindir/dnf-3 /usr/bin/yum

%triggerin -- dnf
rm %_bindir/{dnf,yum}
ln -s %_bindir/dnf5 /usr/bin/dnf
ln -s %_bindir/dnf5 /usr/bin/yum

%triggerin -- yum
rm %_bindir/{dnf,yum}
ln -s %_bindir/dnf5 /usr/bin/dnf
ln -s %_bindir/dnf5 /usr/bin/yum

%files
%doc README

%changelog
%autochangelog