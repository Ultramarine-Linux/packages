Name:           umupgrader
Version:        0.1.0
Release:        1%?dist
Summary:        A GUI System Upgrader for Ultramarine Linux 
License:        MIT
URL:            https://github.com/Ultramarine-Linux/umupgrader
Source0:        %url/archive/refs/tags/%version.tar.gz
BuildRequires:  nim git-core pkgconfig(gtk4) pkgconfig(libadwaita-1) anda-srpm-macros

%description
%summary.

%prep
%autosetup

%build
nimble build umupgrader -y -t:'%nim_tflags' -l:'%nim_lflags' --debuginfo:on

%install
mkdir -p %buildroot%_bindir %buildroot%_datadir/{applications,polkit-1/actions}
install -Dm755 %name %buildroot%_bindir/
install -Dm644 com.fyralabs.umupgrader.policy %buildroot%_datadir/polkit-1/actions/
install -Dm644 umupgrader.desktop %buildroot%_datadir/applications/com.fyralabs.umupgrader.desktop

%files
%_bindir/%name
%_datadir/polkit-1/actions/com.fyralabs.umupgrader.policy
%_datadir/applications/com.fyralabs.umupgrader.desktop

%changelog
%autochangelog
