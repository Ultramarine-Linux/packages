%global _disable_source_fetch 0
%global _dist_version 37

Name: ultramarine-repos
Version: %{_dist_version}
Release: 5%{?dist}
License: MIT
Summary: Repositories for Ultramarine Linux
Requires: %{name}-common = %{version}-%{release}
Recommends: %{name}-extras = %{version}-%{release}
Suggests: %{name}-extras-jam = %{version}-%{release}
Provides: ultramarine-repos(%{_dist_version}) = %{_dist_version}

%description
Metapackage for Ultramarine Linux repositories

%package common
Summary: Common repository for Ultramarine Linux
Requires: fedora-repos(%{version})
Source100: ultramarine.repo
Source101: terra.repo
%description common
Common repository file for Ultramarine Linux

%package extras
Summary: Additional repositories for Ultramarine Linux
Requires: distribution-gpg-keys
Requires: flatpak
Source200: https://flathub.org/repo/flathub.flatpakrepo

# Don't own the rpmfusion repositories, let it be overridden by the real packages

#Source201: rpmfusion-free.repo
#Source202: rpmfusion-free-updates.repo
#Source203: rpmfusion-nonfree.repo
#Source204: rpmfusion-nonfree-updates.repo
Source206: vscodium.repo
Source209: akmods-secureboot.repo
%description extras
Additional repository files for Ultramarine Linux that provides access to popular software that are not shipped by default:
    - Flathub's Flatpak repo (enabled by default)
    - RPMFusion Free (all patented codecs filtered out)
    - RPMFusion Nonfree (disabled by default)
    - Repositories for secureboot support for 'akmod' kernel modules (enabled by default)
    - Docker CE (disabled by default)
    - VSCodium (enabled by default)

%prep

%build

%install
# DNF repos
mkdir -p %{buildroot}/%{_sysconfdir}/yum.repos.d/

#common
cp -avx %{SOURCE100} %{buildroot}/%{_sysconfdir}/yum.repos.d/
cp -avx %{SOURCE101} %{buildroot}/%{_sysconfdir}/yum.repos.d/

#extras
cp -avx %{SOURCE206} %{buildroot}/%{_sysconfdir}/yum.repos.d/
cp -avx %{SOURCE209} %{buildroot}/%{_sysconfdir}/yum.repos.d/


# Flatpak remotes
mkdir -p %{buildroot}/%{_sysconfdir}/flatpak/remotes.d
cp -avx %{SOURCE200} %{buildroot}/%{_sysconfdir}/flatpak/remotes.d/

%files

%files common
%{_sysconfdir}/yum.repos.d/ultramarine.repo
%{_sysconfdir}/yum.repos.d/terra.repo
%files extras
%{_sysconfdir}/flatpak/remotes.d/flathub.flatpakrepo
%{_sysconfdir}/yum.repos.d/akmods-secureboot.repo
%{_sysconfdir}/yum.repos.d/vscodium.repo
#%%{_sysconfdir}/yum.repos.d/rpmfusion-free.repo
#%%{_sysconfdir}/yum.repos.d/rpmfusion-free-updates.repo
#%%{_sysconfdir}/yum.repos.d/rpmfusion-nonfree.repo
#%%{_sysconfdir}/yum.repos.d/rpmfusion-nonfree-updates.repo

