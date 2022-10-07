Name:           hyfetch
Version:        1.4.1
Release:        1%{?dist}
Summary:        neofetch with pride flags <3
URL:            https://github.com/hykilpikonna/hyfetch
Source0:        %{url}/archive/refs/tags/1.4.1.tar.gz
License:        MIT

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3-devel
# BuildRequires:  python3-typing_extensions
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
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
%description -n hyfetch-neofetch
%{summary}

Obsoletes:      neofetch >= 7.1.0
Provides:       neofetch
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

%files -n hyfetch-neofetch
%{_bindir}/neofetch
%{_mandir}/man1/neofetch.1.gz


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
%make_install
#%%pyproject_install
#%%pyproject_save_files hyfetch
# bash commands

#%%files -f %{pyproject_files}
#%%{_bindir}/hyfetch


%changelog
* Wed Sep 21 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 1.4.1-1.um36
- Initial version

