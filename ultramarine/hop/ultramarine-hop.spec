Name:           ultramarine-hop
Version:        0.1.5
Release:        1%?dist
Summary:        Hop between desktop environments and editions easily!
License:        GPL-3.0
URL:            https://github.com/Ultramarine-Linux/hop
Source0:        %url/archive/v%version.tar.gz
Requires:       dnf5
Requires:       ultramarine-release
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  anda-srpm-macros
BuildRequires:  nim mold
Provides:       hop
Provides:       umswitch

%description
Ultramarine Hop is a graphical application that enables users of Ultramarine to
switch between editions or install multiple desktop environments on their
system.

%prep
%autosetup -n hop-%version
%nim_prep

%build
%nim_c --define:releasever=%fedora src/umswitch

%install
install -Dm755 src/umswitch %buildroot%_bindir/umswitch
install -Dm644 com.fyralabs.umswitch.policy %buildroot%_datadir/polkit-1/actions/com.fyralabs.umswitch.policy
install -Dm644 umswitch.desktop %buildroot%_datadir/applications/umswitch.desktop

%files
%doc README.md
%license LICENSE
%_bindir/umswitch
%_datadir/polkit-1/actions/com.fyralabs.umswitch.policy
%_datadir/applications/umswitch.desktop
