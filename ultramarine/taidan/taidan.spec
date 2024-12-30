Name:           taidan
Version:        0.1.2
Release:        1%?dist
Summary:        Out-Of-Box-Experience (OOBE) and Welcome App
SourceLicense:  GPL-3.0-or-later
License:        (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND MIT AND (MIT OR Apache-2.0) AND (MIT OR Zlib OR Apache-2.0) AND Unicode-3.0 AND (Unlicense OR MIT) AND Zlib
URL:            https://github.com/Ultramarine-Linux/taidan
Source0:        %url/archive/refs/tags/v%version.tar.gz
Requires:       (glib2 or (/usr/bin/plasma-apply-colorscheme and kf6-kconfig))
Requires:       shadow-utils
Requires:       systemd-udev
Requires:       bash
Requires:       (dnf5 and dnf5-command(copr))
Requires:       flatpak
BuildRequires:  anda-srpm-macros mold cargo rust-packaging perl
BuildRequires:  pkgconfig(libhelium-1)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  clang-libs
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(gnome-desktop-4)

%description
Taidan is a GUI Out-Of-Box-Experience (OOBE) and Welcome App for Ultramarine
Linux, written in Rust and the Helium toolkit.

%prep
%autosetup
%cargo_prep_online

%build
%cargo_license_summary_online
%{cargo_license_online} > LICENSE.dependencies

%install
%cargo_install
for category in catalogue/*; do
    install -Dpm644 $category -t %buildroot%_sysconfdir/com.FyraLabs.Taidan/catalogue/
done
install -Dpm644 data/sysusers.d/taidan.conf -t %buildroot%_sysusersdir
install -Dpm644 data/polkit-1/rules.d/100-taidan.rules -t %buildroot%_datadir/polkit-1/rules.d/

%files
%doc README.md
%license LICENSE.md LICENSE.dependencies
%_bindir/taidan
%_datadir/polkit-1/rules.d/100-taidan.rules
%_sysconfdir/com.FyraLabs.Taidan/
%_sysusersdir/taidan.conf
