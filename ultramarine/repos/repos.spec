%global _dist_version %{?fedora}

Name: ultramarine-repos
Version: %{_dist_version}
Release: 3%{?dist}
License: MIT
Summary: Repositories for Ultramarine Linux
Requires: %{name}-common = %{version}-%{release}
Recommends: %{name}-extras = %{version}-%{release}

Provides: ultramarine-repos(%{_dist_version}) = %{_dist_version}
BuildArch: noarch

%description
Metapackage for Ultramarine Linux repositories.

%package common
Summary: Common repository for Ultramarine Linux
Requires: fedora-repos(%{version})
Requires: ultramarine-gpg-keys
Source100: ultramarine.repo
# UM40 patch
Requires: terra-release
Requires: terra-release-mesa
# todo: if upgrading from 39 require terra-release or something
%description common
Common repository files for Ultramarine Linux

%package extras
Summary: Additional repositories for Ultramarine Linux
Requires: distribution-gpg-keys
Requires: flatpak
Requires: terra-release-extras
Source200: https://flathub.org/repo/flathub.flatpakrepo

# Don't own the rpmfusion repositories, let it be overridden by the real packages

#Source201: rpmfusion-free.repo
#Source202: rpmfusion-free-updates.repo
#Source203: rpmfusion-nonfree.repo
#Source204: rpmfusion-nonfree-updates.repo
%description extras
Additional repository files for Ultramarine Linux that provides access to popular software that are not shipped by default:
    - Flathub's Flatpak repo (enabled by default)
    - RPMFusion Free (all patented codecs filtered out)
    - RPMFusion Nonfree (enabled by default)
    - Repositories for secureboot support for 'akmod' kernel modules (enabled by default)
    - Terra Extras repo (packages that conflict with Fedora)


%package appcenter
Summary: AppCenter repository for Ultramarine Linux
Requires: %{name}-extras = %{version}-%{release}
Source201: https://flatpak.elementary.io/repo.flatpakrepo

%description appcenter
%{summary}.

%dnl %package rpi
%dnl Summary: Additional repo for Raspberry Pi Kernel
%dnl Source300: https://copr.fedorainfracloud.org/coprs/dwrobel/kernel-rpi/repo/fedora-%{version}/dwrobel-kernel-rpi-fedora-%{version}.repo

%dnl %description rpi
%dnl Additional repository for Raspberry Pi Kernel

%prep

%build

%install
# DNF repos
mkdir -p %{buildroot}/%{_sysconfdir}/yum.repos.d/

#common
cp -avx %{SOURCE100} %{buildroot}/%{_sysconfdir}/yum.repos.d/

# Flatpak remotes
mkdir -p %{buildroot}/%{_sysconfdir}/flatpak/remotes.d
cp -avx %{SOURCE200} %{buildroot}/%{_sysconfdir}/flatpak/remotes.d/
cp -avx %{SOURCE201} %{buildroot}/%{_sysconfdir}/flatpak/remotes.d/appcenter.flatpakrepo

%dnl # Raspberry Pi
%dnl cp -avx %{SOURCE300} %{buildroot}/%{_sysconfdir}/yum.repos.d/

%files

%files common
%{_sysconfdir}/yum.repos.d/ultramarine.repo
%files extras
%{_sysconfdir}/flatpak/remotes.d/flathub.flatpakrepo
%files appcenter
%{_sysconfdir}/flatpak/remotes.d/appcenter.flatpakrepo
%dnl %{_sysconfdir}/yum.repos.d/rpmfusion-free.repo
%dnl %{_sysconfdir}/yum.repos.d/rpmfusion-free-updates.repo
%dnl %{_sysconfdir}/yum.repos.d/rpmfusion-nonfree.repo
%dnl %{_sysconfdir}/yum.repos.d/rpmfusion-nonfree-updates.repo
%dnl %files rpi
%dnl %{_sysconfdir}/yum.repos.d/dwrobel-kernel-rpi-fedora-%{version}.repo
