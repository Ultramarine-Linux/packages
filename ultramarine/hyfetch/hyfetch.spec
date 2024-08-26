Name:           hyfetch
Version:        1.4.11
Release:        1%{?dist}
Summary:        neofetch with pride flags <3
URL:            https://github.com/hykilpikonna/hyfetch
Source0:        %{url}/archive/refs/tags/%version.tar.gz
License:        MIT

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3-devel
# BuildRequires:  python3-typing_extensions
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python-unversioned-command
Requires:       bash >= 3.2
Requires:       bind-utils
Requires:       catimg
Requires:       coreutils
Requires:       gawk
Requires:       grep
Requires:       pciutils
Recommends:     caca-utils
Recommends:     ImageMagick
Recommends:     jp2a
Recommends:     w3m-img
Recommends:     xdpyinfo
Recommends:     xprop
Recommends:     xrandr
Recommends:     xrdb
Recommends:     xwininfo

%package -n     hyfetch-neofetch
Summary:        Replacement for neofetch

Obsoletes:      neofetch <= 7.3
Conflicts:      hyfetch
Provides:       neofetch = 7.3.1-%{release}
Requires:       bash >= 3.2
Requires:       bind-utils
Requires:       catimg
Requires:       coreutils
Requires:       gawk
Requires:       grep
Requires:       pciutils
Recommends:     caca-utils
Recommends:     ImageMagick
Recommends:     jp2a
Recommends:     w3m-img
Recommends:     xdpyinfo
Recommends:     xprop
Recommends:     xrandr
Recommends:     xrdb
Recommends:     xwininfo

%description -n hyfetch-neofetch
%{summary}.
%files -n hyfetch-neofetch
%{_bindir}/neowofetch
%{_bindir}/neofetch
%{_mandir}/man1/neofetch.1.gz
%{_mandir}/man1/neowofetch.1.gz
/usr/lib/python*/site-packages/HyFetch-%version-py*.egg/


%description
%{summary}

%prep
%autosetup -n hyfetch-%{version}
#%%generate_buildrequires
#%%pyproject_buildrequires


%build
%make_build
#%%pyproject_wheel

%install
make install PREFIX=%buildroot%_prefix
make install-doc DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
mv %buildroot%_bindir/{hyfetch,neofetch}
mv %buildroot%_mandir/man1/{hyfetch,neofetch}.1
sed -i 's@#!/usr/bin/python@#!/usr/bin/python3@' %buildroot%_bindir/neofetch
rm %buildroot/usr/lib/python*/site-packages/typing_extensions-*.egg
#%%pyproject_install
#%%pyproject_save_files hyfetch
# bash commands

#%%files -f %{pyproject_files}
#%%{_bindir}/hyfetch


%changelog
* Wed Sep 21 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 1.4.1-1.um36
- Initial version

