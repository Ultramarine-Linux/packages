%global is_rawhide 0

%global release_name Kuma
%global codename kuma
%define dist_version 39
%define _alt_name fedora-release

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
%bcond_without pantheon
%bcond_without kde
%bcond_without gnome
%bcond_without atomic_flagship
%bcond_without atomic_pantheon
%bcond_without atomic_kde
%bcond_without atomic_gnome

%if %{with atomic_flagship} || %{with atomic_pantheon} || %{with atomic_kde} || %{with atomic_gnome}
%global with_atomic_desktop 1
%endif

Summary:	Ultramarine Linux release files
Name:		ultramarine-release
Version:	39
Release:	0.16%{?dist}
License:	MIT
Source0:	LICENSE
URL:        https://ultramarine-linux.org
Source1:	README.developers
Source2:	README.Ultramarine-Release-Notes
Source3:	README.license

Source6:	85-display-manager.preset
Source7:	90-default.preset
Source8:	99-default-disable.preset
Source9:	90-default-user.preset
Source13:   60-ultramarine-presets.conf
Source14:   lightdm-gtk-greeter.conf
Source15:   50_ultramarine-gnome.gschema.override

Source19:   distro-template.swidtag
Source20:   distro-edition-template.swidtag

Source28:   longer-default-shutdown-timeout.conf

Source30:   ultramarine.conf

Source31:  enable-kwin-system76-scheduler-integration.service

Source32:  org.projectatomic.rpmostree1.rules

Source33:   50-ultramarine-networking.conf

Source34:   ultramarine.urls

BuildArch: noarch

Provides: ultramarine-release = %{version}-%{release}
Provides: ultramarine-release-variant = %{version}-%{release}

Provides:   system-release
Provides:   system-release(%{version})
Provides:   base-module(platform:f%{version})
Requires:   ultramarine-release-common = %{version}-%{release}

Recommends: ultramarine-release-identity-basic

%description
Release files for Ultramarine Linux.


%package common
Summary: Generic release files

Conflicts:  fedora-release-common

Requires:   ultramarine-release-variant = %{version}
#Suggests:   ultramarine-release

Requires:   ultramarine-repos(%{version})
Requires:   ultramarine-release-identity = %{version}-%{release}

Conflicts:  generic-release
Conflicts:  fedora-release
Provides: %{_alt_name} = %{version}-%{release}
Provides: generic-release = %{version}-%{release}


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
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-basic = %{version}-%{release}
Obsoletes:        ultramarine-release-basic
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Conflicts:        fedora-release-identity-basic
Requires(meta):   ultramarine-release-basic = %{version}-%{release}
Obsoletes:        ultramarine-release-basic < 38

%description identity-basic
Provides the necessary files for a Ultramarine installation that is not identifying
itself as a particular Edition or Spin.

%endif

######################################################################
####### Flagship #######

%if %{with flagship}

%package flagship
Summary:		Base package for Ultramarine Flagship-specific default configurations

RemovePathPostfixes: .flagship
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-flagship = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Provides:         system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-flagship
# GNOME Software plugin for system upgrades since we introduced this mid-cycle.
# Updating the comps won't push it to existing systems until they major upgrade.
# Therefore for 39, we we'll add a conditional requires to the release package
# This should be removed post 39
Requires:		(gs-plugin-ultramarine-pkgdb-collections if gnome-software)
%description flagship
Provides a base package for Ultramarine Flagship configurations.


%package identity-flagship
Summary:		Package providing the Ultramarine Flagship Identity

RemovePathPostfixes: .flagship
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-flagship = %{version}-%{release}

%description identity-flagship
Provides the necessary files for a Ultramarine Flagship installation.

%endif

######################################################################
####### Atomic Flagship #######

%if %{with atomic_flagship}

%package atomic-flagship
Summary:		Base package for Ultramarine Atomic Flagship-specific default configurations

RemovePathPostfixes: .atomic-flagship
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-atomic-flagship = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Requires:         ultramarine-release-atomic-desktop = %{version}-%{release}
Provides:         system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-atomic-flagship
# GNOME Software plugin for system upgrades since we introduced this mid-cycle.
# Updating the comps won't push it to existing systems until they major upgrade.
# Therefore for 39, we we'll add a conditional requires to the release package
# This should be removed post 39
Requires:		(gs-plugin-ultramarine-pkgdb-collections if gnome-software)
%description atomic-flagship
Provides a base package for Ultramarine Atomic Flagship configurations.


%package identity-atomic-flagship
Summary:		Package providing the Ultramarine Atomic Flagship Identity

RemovePathPostfixes: .atomic-flagship
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-atomic-flagship = %{version}-%{release}

%description identity-atomic-flagship
Provides the necessary files for a Ultramarine Atomic Flagship installation.

%endif


######################################################################
####### Pantheon #######

%if %{with pantheon}
%package pantheon
Summary:		Base package for Ultramarine Pantheon-specific default configurations

RemovePathPostfixes: .pantheon
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-pantheon = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Provides:         system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-pantheon
%description pantheon
Provides a base package for Ultramarine Pantheon configurations.

%package identity-pantheon
Summary:		Package providing the Ultramarine Pantheon Identity

RemovePathPostfixes: .pantheon
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-pantheon = %{version}-%{release}

%description identity-pantheon
Provides the necessary files for a Ultramarine Pantheon installation.

%endif

######################################################################
####### Atomic Pantheon #######

%if %{with atomic_pantheon}
%package atomic-pantheon
Summary:		Base package for Ultramarine Atomic Pantheon-specific default configurations

RemovePathPostfixes: .atomic-pantheon
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-atomic-pantheon = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Requires:         ultramarine-release-atomic-desktop = %{version}-%{release}
Provides:         system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-atomic-pantheon
%description atomic-pantheon
Provides a base package for Ultramarine Atomic Pantheon configurations.

%package identity-atomic-pantheon
Summary:		Package providing the Ultramarine Atomic Pantheon Identity

RemovePathPostfixes: .atomic-pantheon
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-atomic-pantheon = %{version}-%{release}

%description identity-atomic-pantheon
Provides the necessary files for a Ultramarine Atomic Pantheon installation.

%endif


######################################################################
####### KDE #######

%if %{with kde}
%package kde
Summary:		Base package for Ultramarine KDE-specific default configurations

RemovePathPostfixes: .kde
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-kde = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Provides:         system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-kde
%description kde
Provides a base package for Ultramarine KDE configurations.

%package identity-kde

Summary:		Package providing the Ultramarine KDE Identity

RemovePathPostfixes: .kde
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-kde = %{version}-%{release}

%description identity-kde

Provides the necessary files for a Ultramarine KDE installation.

%endif

######################################################################
####### Atomic KDE #######

%if %{with atomic_kde}
%package atomic-kde
Summary:		Base package for Ultramarine Atomic KDE-specific default configurations

RemovePathPostfixes: .atomic-kde
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-atomic-kde = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Requires:         ultramarine-release-atomic-desktop = %{version}-%{release}
Provides:         system-release-product
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-atomic-kde
%description atomic-kde
Provides a base package for Ultramarine Atomic KDE configurations.

%package identity-atomic-kde

Summary:		Package providing the Ultramarine Atomic KDE Identity

RemovePathPostfixes: .atomic-kde
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-atomic-kde = %{version}-%{release}

%description identity-atomic-kde

Provides the necessary files for a Ultramarine Atomic KDE installation.

%endif

######################################################################
####### GNOME #######

%if %{with gnome}

%package gnome
Summary:		Base package for Ultramarine GNOME-specific default configurations

RemovePathPostfixes: .gnome
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-gnome = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Provides:         system-release-product
Recommends:       gnome-shell-extension-pop-shell
Recommends:       gnome-shell-extension-appindicator
Recommends:       gnome-shell-extension-windowsNavigator
Recommends:       gnome-shell-extension-appmenu-is-back
Requires:         kwin-system76-scheduler-integration
BuildRequires:    systemd-rpm-macros

# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-gnome
# GNOME Software plugin for system upgrades since we introduced this mid-cycle.
# Updating the comps won't push it to existing systems until they major upgrade.
# Therefore for 39, we we'll add a conditional requires to the release package
# This should be removed post 39
Requires:		(gs-plugin-ultramarine-pkgdb-collections if gnome-software)
%description gnome
Provides a base package for Ultramarine GNOME configurations.

%package identity-gnome
Summary:		Package providing the Ultramarine GNOME Identity

RemovePathPostfixes: .gnome
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-gnome = %{version}-%{release}

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
Summary:		Base package for Ultramarine Atomic GNOME-specific default configurations

RemovePathPostfixes: .atomic-gnome
Provides:         ultramarine-release = %{version}-%{release}
Provides:         ultramarine-release-atomic-gnome = %{version}-%{release}
Provides:         ultramarine-release-variant = %{version}-%{release}
Provides:         system-release
Provides:         system-release(%{version})
Provides:         base-module(platform:f%{version})
Requires:         ultramarine-release-common = %{version}-%{release}
Requires:         ultramarine-release-atomic-desktop = %{version}-%{release}
Provides:         system-release-product
Recommends:       gnome-shell-extension-pop-shell
Recommends:       gnome-shell-extension-appindicator
Recommends:       gnome-shell-extension-windowsNavigator
Recommends:       gnome-shell-extension-appmenu-is-back
Requires:         kwin-system76-scheduler-integration
BuildRequires:    systemd-rpm-macros

# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-atomic-gnome
# GNOME Software plugin for system upgrades since we introduced this mid-cycle.
# Updating the comps won't push it to existing systems until they major upgrade.
# Therefore for 39, we we'll add a conditional requires to the release package
# This should be removed post 39
Requires:		(gs-plugin-ultramarine-pkgdb-collections if gnome-software)
%description atomic-gnome
Provides a base package for Ultramarine Atomic GNOME configurations.

%package identity-atomic-gnome
Summary:		Package providing the Ultramarine Atomic GNOME Identity

RemovePathPostfixes: .atomic-gnome
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Requires(meta):   ultramarine-release-atomic-gnome = %{version}-%{release}

%description identity-atomic-gnome
Provides the necessary files for a Ultramarine Atomic GNOME installation.

%endif

######################################################################
#### Accessory packages
######################################################################

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
# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec

%global dist_vendor Ultramarine
%global dist_name   Ultramarine Linux

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://ultramarine-linux.org/

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://github.com/Ultramarine-Linux/ultramarine/

# debuginfod server, as used in elfutils.spec.
%global dist_debuginfod_url https://debuginfod.fedoraproject.org/
# -------------------------------------------------------------------------

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
SUPPORT_URL="https://discord.com/invite/bUuQasHdrF"
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

%if %{with pantheon}
# Pantheon
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.pantheon
echo "VARIANT=\"Pantheon Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.pantheon
echo "VARIANT_ID=pantheon" >> %{buildroot}%{_prefix}/lib/os-release.pantheon
sed -i -e "s|(%{release_name}%{?prerelease})|(Pantheon Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.pantheon
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Pantheon/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.pantheon
%endif

%if %{with atomic_pantheon}
# Atomic Pantheon
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.atomic-pantheon
echo "VARIANT=\"Atomic Pantheon Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.atomic-pantheon
echo "VARIANT_ID=atomic-pantheon" >> %{buildroot}%{_prefix}/lib/os-release.atomic-pantheon
sed -i -e "s|(%{release_name}%{?prerelease})|(Atomic Pantheon Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.atomic-pantheon
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Atomic Pantheon/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-pantheon
%endif

%if %{with kde}
# KDE
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT=\"KDE Plasma Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT_ID=kde" >> %{buildroot}%{_prefix}/lib/os-release.kde
sed -i -e "s|(%{release_name}%{?prerelease})|(KDE Plasma Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kde
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/KDE Plasma/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.kde

install -Dm644 %{SOURCE31} %{buildroot}%{_userunitdir}/enable-kwin-system76-scheduler-integration.service

%endif

%if %{with atomic_kde}
# Atomic KDE
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.atomic-kde
echo "VARIANT=\"Atomic KDE Plasma Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.atomic-kde
echo "VARIANT_ID=atomic-kde" >> %{buildroot}%{_prefix}/lib/os-release.atomic-kde
sed -i -e "s|(%{release_name}%{?prerelease})|(Atomic KDE Plasma Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.atomic-kde
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Atomic KDE Plasma/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-kde

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


# Create copr config file so COPR doesnt flip out and assume EPEL
# I created a PR to support this months ago, but completely forgot about it
# to the point that risiOS managed to beat us to it - Cappy
install -d %{buildroot}%{_datadir}/dnf/plugins
cat >> %{buildroot}%{_datadir}/dnf/plugins/copr.vendor.conf << EOF
[main]
distribution = Fedora
releasever = %{releasever}
EOF

# provide upstream-release files for debian based apps
install -d $RPM_BUILD_ROOT%{_sysconfdir}/upstream-release
cat << EOF >>$RPM_BUILD_ROOT%{_sysconfdir}/upstream-release/lsb-release
ID=Fedora
VERSION_ID=39
VERSION_CODENAME="Thirty Nine"
PRETTY_NAME="Fedora Linux 39 (Thirty Nine)"
EOF

##########################

# Create custom Anaconda config
mkdir -p %{buildroot}%{_sysconfdir}/anaconda/profile.d/
cp -pr %{SOURCE30} %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine.conf

# sysctls
mkdir -p %{buildroot}%{_prefix}/lib/sysctl.d/
cp -pr %{SOURCE33} %{buildroot}%{_prefix}/lib/sysctl.d/50-ultramarine-networking.conf

#########################



# Budgie config
mkdir -p %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE13} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE14} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-lightdm-gtk-greeter.conf

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

%%fedora			%{dist_version}
%%dist			    %%{?distprefix}.um%{dist_version}%%{?with_bootstrap:~bootstrap}
%%ultramarine		%{dist_version}
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
install -Dm0644 %{SOURCE9} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/user.conf.d/

# Add debuginfod urls
install -D -p -m 0644 -t %{buildroot}%{_sysconfdir}/debuginfod %{SOURCE34}

%if %{with atomic_desktop}

# Install rpm-ostree polkit rules
install -Dm0644 %{SOURCE32} -t %{buildroot}%{_datadir}/polkit-1/rules.d/

%endif

# the funny KDE system76 scheduler integration
%if %{with kde}

%post identity-kde
%systemd_user_post enable-kwin-system76-scheduler-integration.service

%preun identity-kde
%systemd_user_preun enable-kwin-system76-scheduler-integration.service

%endif

%if %{with atomic_kde}

%post identity-atomic-kde
%systemd_user_post enable-kwin-system76-scheduler-integration.service

%preun identity-atomic-kde
%systemd_user_preun enable-kwin-system76-scheduler-integration.service

%endif

%files common
%{_datadir}/dnf/plugins/copr.vendor.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
%{_prefix}/lib/sysctl.d/50-ultramarine-networking.conf
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
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-lightdm-gtk-greeter.conf
%files identity-flagship
%{_prefix}/lib/os-release.flagship
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.flagship
%endif

%if %{with atomic_flagship}
%files atomic-flagship
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-lightdm-gtk-greeter.conf
%files identity-atomic-flagship
%{_prefix}/lib/os-release.atomic-flagship
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-flagship
%endif

%if %{with pantheon}
%files pantheon
%files identity-pantheon
%{_prefix}/lib/os-release.pantheon
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.pantheon
%endif

%if %{with atomic_pantheon}
%files atomic-pantheon
%files identity-atomic-pantheon
%{_prefix}/lib/os-release.atomic-pantheon
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-pantheon
%endif

%if %{with kde}
%files kde
%files identity-kde
%{_prefix}/lib/os-release.kde
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.kde
%config %_userunitdir/enable-kwin-system76-scheduler-integration.service
%endif

%if %{with atomic_kde}
%files atomic-kde
%files identity-atomic-kde
%{_prefix}/lib/os-release.atomic-kde
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-kde
%config %_userunitdir/enable-kwin-system76-scheduler-integration.service
%endif

%if %{with gnome}
%files gnome
%files identity-gnome
%{_prefix}/lib/os-release.gnome
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.gnome
%{_datadir}/glib-2.0/schemas/50_ultramarine-gnome.gschema.override
%endif

%if %{with atomic_gnome}
%files atomic-gnome
%files identity-atomic-gnome
%{_prefix}/lib/os-release.atomic-gnome
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.atomic-gnome
%{_datadir}/glib-2.0/schemas/50_ultramarine-gnome.gschema.override
%endif

%if %{with atomic_desktop}
%files atomic-desktop
%attr(0644,root,root) %{_prefix}/share/polkit-1/rules.d/org.projectatomic.rpmostree1.rules
%endif

%files notes
%doc readme/README.Ultramarine-Release-Notes

%changelog
%autochangelog
