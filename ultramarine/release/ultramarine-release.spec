%global is_rawhide 0

%global release_name Cyberia
%global fedora_codename Forty One
%global codename cyberia
%define dist_version 41
%define _alt_name fedora-release

%define xfce_conf_commit 24fae98d5cf148b5017d6273e442d9b46bf41e91

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif

%bcond_without basic
%bcond_without flagship
%bcond_without plasma
%bcond_without gnome
%bcond_without xfce
%bcond_without atomic_flagship
%bcond_without atomic_plasma
%bcond_without atomic_gnome
%bcond_without atomic_xfce
%bcond_without chromebook
%ifarch x86_64
%bcond_without surface
%else
%bcond_with surface
%endif

%if %{with flagship} || %{with plasma} || %{with gnome} || %{with xfce} || %{with atomic_flagship} || %{with atomic_plasma} || %{with atomic_gnome} || %{with atomic_xfce}
%global with_desktop 1
%endif

%if %{with atomic_flagship} || %{with atomic_plasma} || %{with atomic_gnome} || %{with atomic_xfce}
%global with_atomic_desktop 1
%endif

## ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
## ┃ Ultramarine Linux Release Package ┃
## ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Summary:	Ultramarine Linux release files
Name:		ultramarine-release
Version:	%{dist_version}
Release:	5%{?dist}
License:	MIT
Source0:	LICENSE
URL:        https://ultramarine-linux.org
Recommends: ultramarine-release-identity-basic
BuildArch:  noarch
Obsoletes:  dnf5-default-package-manager

Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}

Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})

Requires:   ultramarine-release-common = %{version}-%{release}

Source1:	README.developers
Source2:	README.Ultramarine-Release-Notes
Source3:	README.license

Source4:	80-workstation.preset
Source5:	81-desktop.preset
Source6:	85-display-manager.preset
Source7:	90-default.preset
Source8:	99-default-disable.preset
Source9:	90-default-user.preset
Source10:	89-ultramarine-default.preset

Source12:   60-ultramarine-presets.conf
Source13:   lightdm-gtk-greeter-flagship.conf
Source14:   lightdm-gtk-greeter-xfce.conf
Source15:   50_ultramarine-gnome.gschema.override

Source19:   distro-template.swidtag
Source20:   distro-edition-template.swidtag

Source28:   longer-default-shutdown-timeout.conf

Source31:   enable-kwin-system76-scheduler-integration.service
Source32:   org.projectatomic.rpmostree1.rules
Source34:   ultramarine.urls

Source40:   https://github.com/Ultramarine-Linux/xfce-config/archive/%{xfce_conf_commit}.tar.gz

Source50:   ultramarine.conf
Source51:   ultramarine-flagship.conf
Source52:   ultramarine-gnome.conf
Source53:   ultramarine-plasma.conf
Source54:   ultramarine-xfce.conf

Source60:   ultramarine-flagship-protected.conf
Source61:   ultramarine-gnome-protected.conf
Source62:   ultramarine-plasma-protected.conf
Source63:   ultramarine-xfce-protected.conf

Source64:   88-ultramarine-chromebook-default.preset

Source65:   91-ultramarine-surface-default.preset

Source70:   polycrystal-ultramarine-flaghsip.json
Source71:   polycrystal-ultramarine-gnome.json
Source72:   polycrystal-ultramarine-plasma.json
Source73:   polycrystal-ultramarine-xfce.json

BuildRequires:    systemd-rpm-macros

%description
Release files for Ultramarine Linux.


## ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
## ┃ Common Files and Release Notes ┃
## ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

%package common
Summary:    Generic release files
Requires:   ultramarine-release-variant = %{version}
Requires:   ultramarine-repos(%{version})
Requires:   ultramarine-release-identity = %{version}-%{release}
Recommends: system76-scheduler
Recommends: ultramarine-phony-bookmarks
Conflicts:  generic-release
Conflicts:  fedora-release
Conflicts:  fedora-release-common
Provides:   %{_alt_name} = %{version}-%{release}
Provides:   generic-release = %{version}-%{release}

%description common
Release files common to all Editions and Spins


%package notes
Summary:	Release Notes
License:	Open Publication
Provides:	system-release-notes = %{version}-%{release}

%description notes
Release files for Ultramarine Linux.

%if %{with basic}

######################################################################
#### Variants
######################################################################

####### Generic (Basic) #######

%package identity-basic
Summary:		Package providing the basic Ultramarine identity
RemovePathPostfixes: .basic
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Conflicts:		fedora-release-identity-basic

%description identity-basic
Provides the necessary files for a Ultramarine installation that is not identifying
itself as a particular Edition.

%endif

######################################################################
####### Flagship #######

%if %{with flagship}

%package flagship
Summary:	Base package for Ultramarine Flagship-specific default configurations
RemovePathPostfixes: .flagship
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-flagship = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-flagship

%description flagship
Provides a base package for Ultramarine Flagship configurations.

%package identity-flagship
Summary:		Package providing the Ultramarine Flagship Identity
RemovePathPostfixes: .flagship
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):	ultramarine-release-flagship = %{version}-%{release}

%description identity-flagship
Provides the necessary files for a Ultramarine Flagship installation.

%endif

######################################################################
####### Atomic Flagship #######

%if %{with atomic_flagship}

%package atomic-flagship
Summary:	Base package for Ultramarine Atomic Flagship-specific default configurations
RemovePathPostfixes: .atomic-flagship
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-atomic-flagship = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   ultramarine-release-atomic-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-atomic-flagship

%description atomic-flagship
Provides a base package for Ultramarine Atomic Flagship configurations.

%package identity-atomic-flagship
Summary:		Package providing the Ultramarine Atomic Flagship Identity
RemovePathPostfixes: .atomic-flagship
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):	ultramarine-release-atomic-flagship = %{version}-%{release}

%description identity-atomic-flagship
Provides the necessary files for a Ultramarine Atomic Flagship installation.

%endif

######################################################################
####### Plasma #######

%if %{with plasma}
%package plasma
Summary:	Base package for Ultramarine Plasma-specific default configurations
RemovePathPostfixes: .plasma
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-plasma = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
Provides: ultramarine-release-kde = %{version}-%{release}
Obsoletes: ultramarine-release-kde < 40-12
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-plasma
Recommends:	kwin-system76-scheduler-integration

%description plasma
Provides a base package for Ultramarine Plasma configurations.

%package identity-plasma
Summary:		Package providing the Ultramarine Plasma Identity
RemovePathPostfixes: .plasma
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Obsoletes:        ultramarine-release-identity-kde < 40-12
Requires(meta):	ultramarine-release-plasma = %{version}-%{release}

%description identity-plasma
Provides the necessary files for a Ultramarine Plasma installation.

%endif

######################################################################
####### Atomic Plasma #######

%if %{with atomic_plasma}
%package atomic-plasma
Summary:	Base package for Ultramarine Atomic Plasma-specific default configurations

RemovePathPostfixes: .atomic-plasma
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-atomic-plasma = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   ultramarine-release-atomic-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-atomic-plasma

%description atomic-plasma
Provides a base package for Ultramarine Atomic Plasma configurations.

%package identity-atomic-plasma
Summary:		Package providing the Ultramarine Atomic Plasma Identity
RemovePathPostfixes: .atomic-plasma
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):	ultramarine-release-atomic-plasma = %{version}-%{release}

%description identity-atomic-plasma
Provides the necessary files for a Ultramarine Atomic Plasma installation.

%endif

######################################################################
####### GNOME #######

%if %{with gnome}

%package gnome
Summary:	Base package for Ultramarine GNOME-specific default configurations
RemovePathPostfixes: .gnome
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-gnome = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
Recommends: gnome-shell-extension-pop-shell
Recommends: gnome-shell-extension-appindicator
Recommends: gnome-shell-extension-windowsNavigator
Recommends: gnome-shell-extension-appmenu-is-back
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-gnome

%description gnome
Provides a base package for Ultramarine GNOME configurations.

%package identity-gnome
Summary:		Package providing the Ultramarine GNOME Identity
RemovePathPostfixes: .gnome
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):	ultramarine-release-gnome = %{version}-%{release}

# Allow migration from the legacy ultramarine-gnome-filesystem package
Provides: ultramarine-gnome-filesystem = %{version}-%{release}
Obsoletes: ultramarine-gnome-filesystem < 0.1.2-2

%description identity-gnome
Provides the necessary files for a Ultramarine GNOME installation.

%endif

######################################################################
####### Atomic GNOME #######

%if %{with atomic_gnome}

%package atomic-gnome
Summary:	Base package for Ultramarine Atomic GNOME-specific default configurations
RemovePathPostfixes: .atomic-gnome
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-atomic-gnome = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   ultramarine-release-atomic-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
Recommends: gnome-shell-extension-pop-shell
Recommends: gnome-shell-extension-appindicator
Recommends: gnome-shell-extension-windowsNavigator
Recommends: gnome-shell-extension-appmenu-is-back
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-atomic-gnome

%description atomic-gnome
Provides a base package for Ultramarine Atomic GNOME configurations.

%package identity-atomic-gnome
Summary:		Package providing the Ultramarine Atomic GNOME Identity
RemovePathPostfixes: .atomic-gnome
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):	ultramarine-release-atomic-gnome = %{version}-%{release}

%description identity-atomic-gnome
Provides the necessary files for a Ultramarine Atomic GNOME installation.

%endif


######################################################################
####### XFCE #######

%if %{with xfce}

## ━━━ pkgexcl ━━━
## A Special package that conflicts with packages provided by various
## Fedora groups. These packages are removed to make it as lightweight
## as possible.

%package xfce-pkgexcl
Summary:	Package that excludes other redundant packages for XFCE
Conflicts:	abrt-desktop
Conflicts:	dnfdragora-updater

%description xfce-pkgexcl
This package excludes some packages included in Fedora groups that are
pulled into Ultramarine as weak/optional dependencies.
This is done by marking them as conflicts in this package.


%package xfce
Summary:	Base package for Ultramarine XFCE-specific default configurations
RemovePathPostfixes: .xfce
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-xfce = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
Recommends:	ultramarine-release-identity-xfce
Recommends: materia-gtk-theme
Recommends: papirus-icon-theme
Recommends: papirus-icon-theme-dark
Recommends: papirus-icon-theme-light
Recommends: mugshot
# The config replaces the default app menu with whisker menu
Recommends: xfce4-whiskermenu-plugin
Recommends: xfce4-docklike-plugin
Recommends: ultramarine-release-xfce-pkgexcl

%description xfce
Provides a base package for Ultramarine XFCE configurations.

%package identity-xfce
Summary:		Package providing the Ultramarine XFCE Identity
RemovePathPostfixes: .xfce
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta): ultramarine-release-xfce = %{version}-%{release}

%description identity-xfce
Provides the necessary files for a Ultramarine XFCE installation.

%endif

######################################################################
####### Atomic XFCE #######

%if %{with atomic_xfce}

%package atomic-xfce
Summary:	Base package for Ultramarine Atomic XFCE-specific default configurations

RemovePathPostfixes: .atomic-xfce
Provides:   ultramarine-release = %{version}-%{release}
Provides:   ultramarine-release-atomic-xfce = %{version}-%{release}
Provides:   ultramarine-release-variant = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}
Requires:   ultramarine-release-desktop = %{version}-%{release}
Requires:   ultramarine-release-atomic-desktop = %{version}-%{release}
Requires:   polycrystal
Provides:   system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:	ultramarine-release-identity-atomic-xfce
Recommends: ultramarine-release-xfce-pkgexcl

%description atomic-xfce
Provides a base package for Ultramarine Atomic XFCE configurations.

%package identity-atomic-xfce
Summary:		Package providing the Ultramarine Atomic XFCE Identity
RemovePathPostfixes: .atomic-xfce
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta): ultramarine-release-atomic-xfce = %{version}-%{release}

%description identity-atomic-xfce
Provides the necessary files for a Ultramarine Atomic XFCE installation.

%endif

######################################################################
#### Accessory packages
######################################################################

####### Chromebook #######

%if %{with chromebook}
%package        chromebook
Summary:        Common configuration package for chromebook variants

%description chromebook
Common configuration package for chromebook variants
%endif

####### Surface #######

%if %{with surface}
%package        surface
Summary:        Common configuration package for surface variants

%description surface
Common configuration package for surface variants
%endif

####### Desktop #######

%if %{with desktop}
%package desktop
Summary:        Common configuration package for desktop variants

%description desktop
Common configuration package for desktop variants
%endif

####### Atomic Desktop (OSTree) #######

%if %{with atomic_desktop}
%package atomic-desktop
Summary:        Common configuration package for atomic desktop variants

%description atomic-desktop
Common configuration package for atomic desktop variants
%endif

%prep

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Ultramarine Linux release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/ultramarine-release
echo "cpe:/o:ultramarine:um:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/ultramarine-release %{buildroot}%{_sysconfdir}/ultramarine-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s ultramarine-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s ultramarine-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ultramarine-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}

# ╭────────────────────────────────────────────────────────────────────────────
# │ Definitions for /etc/os-release and for macros in macros.dist. These macros
# │ are useful for spec files where distribution-specific identifiers are used
# │ to customize packages.
# │
# │ Name of vendor / name of distribution. Typically used to identify where the
# │ binary comes from in --help or --version messages of programs.
# │ Examples: gdb.spec, clang.spec

%global dist_vendor Ultramarine
%global dist_name   Ultramarine Linux

# │ URL of the homepage of the distribution
# │ Example: gstreamer1-plugins-base.spec
%global dist_home_url https://ultramarine-linux.org/

# │ Bugzilla / bug reporting URLs shown to users.
# │ Examples: gcc.spec
%global dist_bug_report_url https://github.com/Ultramarine-Linux/ultramarine/

# │ debuginfod server, as used in elfutils.spec.
%global dist_debuginfod_url https://debuginfod.fedoraproject.org/
# ╰────────────────────────────────────────────────────────────────────────────

install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >> os-release
NAME="Ultramarine Linux"
ID=ultramarine
VERSION="%{dist_version} (%{release_name})"
VERSION_CODENAME=%{codename}
ID_LIKE=fedora
PLATFORM_ID="platform:um%{dist_version}"
VERSION_ID=%{dist_version}
PRETTY_NAME="Ultramarine Linux %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
LOGO=ultramarine
CPE_NAME="cpe:/o:ultramarine:um:%{dist_version}"
DEFAULT_HOSTNAME="ultramarine"
HOME_URL="http://ultramarine-linux.org"
SUPPORT_URL="https://discord.gg/5fdPuxTg5Q"
BUG_REPORT_URL="https://github.com/Ultramarine-Linux/ultramarine"
DOCUMENTATION_URL="https://wiki.ultramarine-linux.org"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{dist_version}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{dist_version}
PRIVACY_POLICY_URL="https://fyralabs.com/privacy"
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -sf ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -sf ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}


# Create os-release files for the different editions

%if %{with basic}
# Basic
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.basic
%endif

%if %{with flagship}
# Flagship
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.flagship
echo "VARIANT=\"Flagship Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.flagship
echo "VARIANT_ID=flagship" >> %{buildroot}%{_prefix}/lib/os-release.flagship
sed -i -e "s|(%{release_name}%{?prerelease})|(Flagship Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.flagship
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Flagship/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.flagship

install -Dm0644 %{SOURCE60} %{buildroot}%{_sysconfdir}/dnf/protected.d/ultramarine-flagship.conf
%endif

%if %{with atomic_flagship}
# Atomic Flagship
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.atomic-flagship
echo "VARIANT=\"Atomic Flagship Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.atomic-flagship
echo "VARIANT_ID=atomic-flagship" >> %{buildroot}%{_prefix}/lib/os-release.atomic-flagship
sed -i -e "s|(%{release_name}%{?prerelease})|(Atomic Flagship Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.atomic-flagship
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Atomic Flagship/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-flagship
%endif

%if %{with plasma}
# Plasma
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.plasma
echo "VARIANT=\"Plasma Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.plasma
echo "VARIANT_ID=plasma" >> %{buildroot}%{_prefix}/lib/os-release.plasma
sed -i -e "s|(%{release_name}%{?prerelease})|(Plasma Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.plasma
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Plasma/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.plasma

install -Dm0644 %{SOURCE62} %{buildroot}%{_sysconfdir}/dnf/protected.d/ultramarine-plasma.conf

install -Dm644 %{SOURCE31} %{buildroot}%{_userunitdir}/enable-kwin-system76-scheduler-integration.service

%endif

%if %{with atomic_plasma}
# Atomic Plasma
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.atomic-plasma
echo "VARIANT=\"Atomic Plasma Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.atomic-plasma
echo "VARIANT_ID=atomic-plasma" >> %{buildroot}%{_prefix}/lib/os-release.atomic-plasma
sed -i -e "s|(%{release_name}%{?prerelease})|(Atomic Plasma Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.atomic-plasma
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Atomic Plasma/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-plasma

install -Dm644 %{SOURCE31} %{buildroot}%{_userunitdir}/enable-kwin-system76-scheduler-integration.service

%endif

%if %{with gnome}
# GNOME
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.gnome
echo "VARIANT=\"GNOME Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.gnome
echo "VARIANT_ID=gnome" >> %{buildroot}%{_prefix}/lib/os-release.gnome
sed -i -e "s|(%{release_name}%{?prerelease})|(GNOME Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.gnome
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/GNOME/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.gnome

install -Dm0644 %{SOURCE61} %{buildroot}%{_sysconfdir}/dnf/protected.d/ultramarine-gnome.conf
%endif

%if %{with atomic_gnome}
# Atomic GNOME
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.atomic-gnome
echo "VARIANT=\"Atomic GNOME Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.atomic-gnome
echo "VARIANT_ID=atomic-gnome" >> %{buildroot}%{_prefix}/lib/os-release.atomic-gnome
sed -i -e "s|(%{release_name}%{?prerelease})|(Atomic GNOME Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.atomic-gnome
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Atomic GNOME/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-gnome
%endif

%if %{with xfce}
# XFCE
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.xfce
echo "VARIANT=\"XFCE Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.xfce
echo "VARIANT_ID=xfce" >> %{buildroot}%{_prefix}/lib/os-release.xfce
sed -i -e "s|(%{release_name}%{?prerelease})|(XFCE Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.xfce
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/XFCE/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.xfce

install -Dm0644 %{SOURCE63} %{buildroot}%{_sysconfdir}/dnf/protected.d/ultramarine-xfce.conf

# install xfce configs

mkdir -p %{buildroot}%{_sysconfdir}/skel

# the file just contains a .config
# remove the first directory from the extract path, so it's just a .config

tar -xvf %{SOURCE40} -C %{buildroot}%{_sysconfdir}/skel --strip-components=1


%endif

%if %{with atomic_xfce}
# Atomic XFCE
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.atomic-xfce
echo "VARIANT=\"Atomic XFCE Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.atomic-xfce
echo "VARIANT_ID=atomic-xfce" >> %{buildroot}%{_prefix}/lib/os-release.atomic-xfce
sed -i -e "s|(%{release_name}%{?prerelease})|(Atomic XFCE Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.atomic-xfce
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Atomic XFCE/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-xfce
%endif


# Create copr config file so COPR doesnt flip out and assume EPEL
# I created a PR to support this months ago, but completely forgot about it
# to the point that risiOS managed to beat us to it - Cappy
install -d %{buildroot}%{_datadir}/dnf/plugins
cat >> %{buildroot}%{_datadir}/dnf/plugins/copr.vendor.conf << EOF
[main]
distribution = fedora
releasever = %{releasever}
EOF

# provide upstream-release files for debian based apps
install -d $RPM_BUILD_ROOT%{_sysconfdir}/upstream-release
cat << EOF >>$RPM_BUILD_ROOT%{_sysconfdir}/upstream-release/lsb-release
ID=Fedora
VERSION_ID=%dist_version
VERSION_CODENAME="%fedora_codename"
PRETTY_NAME="Fedora Linux %dist_version (%fedora_codename)"
EOF

##########################

# Create custom Anaconda config
mkdir -p %{buildroot}%{_sysconfdir}/anaconda/profile.d/
cp -pr %{SOURCE50} %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
cp -pr %{SOURCE51} %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine-flagship.conf
cp -pr %{SOURCE52} %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine-gnome.conf
cp -pr %{SOURCE53} %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine-plasma.conf
cp -pr %{SOURCE54} %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine-xfce.conf

# sysctls
mkdir -p %{buildroot}%{_prefix}/lib/sysctl.d/


#########################

#########################

# Polycrystal entries
mkdir -p %{buildroot}%{_sysconfdir}/polycrystal/entries
install %{SOURCE70} %{buildroot}%{_sysconfdir}/polycrystal/entries/ultramarine-flagship.conf
install %{SOURCE71} %{buildroot}%{_sysconfdir}/polycrystal/entries/ultramarine-gnome.conf
install %{SOURCE72} %{buildroot}%{_sysconfdir}/polycrystal/entries/ultramarine-plasma.conf
install %{SOURCE73} %{buildroot}%{_sysconfdir}/polycrystal/entries/ultramarine-xfce.conf

#########################

# Budgie config
mkdir -p %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE12} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE13} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-flagship-lightdm-gtk-greeter.conf

# XFCE config
install %{SOURCE14} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-xfce-lightdm-gtk-greeter.conf

# GNOME config
install -Dm0644 %{SOURCE15} -t %{buildroot}%{_datadir}/glib-2.0/schemas/

# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE19} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s --relative %{buildroot}%{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/ultramarinelinux.org


# Create os-release and issue files for the different editions here
# There are no separate editions for generic-release

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora			  %{dist_version}
%%dist			      %%{?distprefix}.um%{dist_version}%%{?with_bootstrap:~bootstrap}
%%ultramarine		  %{dist_version}
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
%%dist_debuginfod_url %{dist_debuginfod_url}
EOF

# Install readme
mkdir -p readme
install -pm 0644 %{SOURCE3} readme/README.Ultramarine-Release-Notes

# Install licenses
mkdir -p licenses
install -pm 0644 %{SOURCE0} licenses/LICENSE
install -pm 0644 %{SOURCE2} licenses/README.license

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

# Default system wide
install -Dm0644 %{SOURCE6} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE7} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE8} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE10} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE9} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/user.conf.d/

%if %{with desktop}

# Install systemd presets for desktop
install -Dm0644 %{SOURCE5} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

%endif

%if %{with chromebook}

# Install systemd presets for chromebook
install -Dm0644 %{SOURCE64} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

%endif

%if %{with surface}

# Install systemd presets for surface
install -Dm0644 %{SOURCE65} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

%endif

%if %{with gnome} || %{with atomic_gnome}

# Install systemd presets for gnome
install -Dm0644 %{SOURCE4} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

%endif

# Add debuginfod urls
install -D -p -m 0644 -t %{buildroot}%{_sysconfdir}/debuginfod %{SOURCE34}

%if %{with atomic_desktop}

# Install rpm-ostree polkit rules
install -Dm0644 %{SOURCE32} -t %{buildroot}%{_datadir}/polkit-1/rules.d/

%endif

# the funny Plasma system76 scheduler integration
%if %{with plasma}

%post identity-plasma
%systemd_user_post enable-kwin-system76-scheduler-integration.service

%preun identity-plasma
%systemd_user_preun enable-kwin-system76-scheduler-integration.service

%endif

%if %{with atomic_plasma}

%post identity-atomic-plasma
%systemd_user_post enable-kwin-system76-scheduler-integration.service

%preun identity-atomic-plasma
%systemd_user_preun enable-kwin-system76-scheduler-integration.service

%endif


%files common
%{_datadir}/dnf/plugins/copr.vendor.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine-flagship.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine-gnome.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine-plasma.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine-xfce.conf
%license licenses/LICENSE licenses/README.license
%{_prefix}/lib/ultramarine-release
%{_prefix}/lib/systemd/user.conf.d/*
%{_prefix}/lib/systemd/system.conf.d/*
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/upstream-release/
%{_sysconfdir}/ultramarine-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/89-ultramarine-default.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/org.ultramarinelinux.Ultramarine-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d
%config(noreplace) %{_sysconfdir}/debuginfod/ultramarine.urls

%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif

%if %{with flagship}
%files flagship
%files identity-flagship
%{_prefix}/lib/os-release.flagship
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.flagship
%{_sysconfdir}/dnf/protected.d/ultramarine-flagship.conf
%config %{_sysconfdir}/polycrystal/entries/ultramarine-flagship.json
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-flagship-lightdm-gtk-greeter.conf
%endif

%if %{with atomic_flagship}
%files atomic-flagship
%files identity-atomic-flagship
%{_prefix}/lib/os-release.atomic-flagship
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-flagship
%config %{_sysconfdir}/polycrystal/entries/ultramarine-flagship.json
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-flagship-lightdm-gtk-greeter.conf
%endif

%if %{with plasma}
%files plasma
%files identity-plasma
%{_prefix}/lib/os-release.plasma
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.plasma
%config %{_sysconfdir}/polycrystal/entries/ultramarine-plasma.json
%{_sysconfdir}/dnf/protected.d/ultramarine-plasma.conf
%config %_userunitdir/enable-kwin-system76-scheduler-integration.service
%endif

%if %{with atomic_plasma}
%files atomic-plasma
%files identity-atomic-plasma
%{_prefix}/lib/os-release.atomic-plasma
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-plasma
%config %{_sysconfdir}/polycrystal/entries/ultramarine-plasma.json
%config %_userunitdir/enable-kwin-system76-scheduler-integration.service
%endif

%if %{with gnome}
%files gnome
%files identity-gnome
%{_prefix}/lib/os-release.gnome
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.gnome
%{_sysconfdir}/dnf/protected.d/ultramarine-gnome.conf
%config %{_sysconfdir}/polycrystal/entries/ultramarine-gnome.json
%{_datadir}/glib-2.0/schemas/50_ultramarine-gnome.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%endif

%if %{with atomic_gnome}
%files atomic-gnome
%files identity-atomic-gnome
%{_prefix}/lib/os-release.atomic-gnome
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-gnome
%config %{_sysconfdir}/polycrystal/entries/ultramarine-gnome.json
%{_datadir}/glib-2.0/schemas/50_ultramarine-gnome.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%endif

%if %{with xfce}
%files xfce
%files identity-xfce
%{_prefix}/lib/os-release.xfce
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.xfce
%{_sysconfdir}/dnf/protected.d/ultramarine-xfce.conf
%config %{_sysconfdir}/polycrystal/entries/ultramarine-xfce.json
%{_sysconfdir}/skel/.config/xfce4/
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-xfce-lightdm-gtk-greeter.conf
%endif

%if %{with atomic_xfce}
%files atomic-xfce
%files identity-atomic-xfce
%{_prefix}/lib/os-release.atomic-xfce
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-xfce
%config %{_sysconfdir}/polycrystal/entries/ultramarine-xfce.json
%{_sysconfdir}/skel/.config/xfce4/
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-xfce-lightdm-gtk-greeter.conf
%endif

%if %{with desktop}
%files desktop
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%endif

%if %{with chromebook}
%files chromebook
%{_prefix}/lib/systemd/system-preset/88-ultramarine-chromebook-default.preset
%endif

%if %{with surface}
%files surface
%{_prefix}/lib/systemd/system-preset/91-ultramarine-surface-default.preset
%endif

%if %{with atomic_desktop}
%files atomic-desktop
%attr(0644,root,root) %{_prefix}/share/polkit-1/rules.d/org.projectatomic.rpmostree1.rules
%endif

%files notes
%doc readme/README.Ultramarine-Release-Notes

%changelog
%autochangelog
