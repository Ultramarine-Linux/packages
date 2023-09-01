%global is_rawhide 0

%global release_name Kuma
%global codename kuma
%define dist_version 39

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


Summary:	Ultramarine Linux release files
Name:		ultramarine-release
Version:	39
Release:	%autorelease -p
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

Source19:   distro-template.swidtag
Source20:   distro-edition-template.swidtag


Source28:   longer-default-shutdown-timeout.conf


Source30:   ultramarine.conf

BuildArch: noarch

Provides: generic-release = %{version}-%{release}
Provides: ultramarine-release = %{version}-%{release}


# We need to Provides: and Conflicts: system release here and in each
# of the generic-release-$VARIANT subpackages to ensure that only one
# may be installed on the system at a time.
Conflicts:  system-release
Conflicts:  generic-release
Provides:   system-release = %{version}
Provides:   system-release(%{version})
Conflicts:	ultramarine-release
Conflicts:	ultramarine-release-identity
Requires:   ultramarine-release-common = %{version}-%{release}
Recommends: ultramarine-release-identity-basic

%description
Release files for Ultramarine Linux.


%package common
Summary: Generic release files

Requires:   generic-release-variant = %{version}
Suggests:   generic-release

Obsoletes:  generic-release < 30-0.1

Obsoletes:  convert-to-edition < 30-0.7
Requires:   ultramarine-repos(%{version}) = %{version}
Requires:   ultramarine-release = %{version}-%{release}

Conflicts: fedora-release-common
Conflicts: generic-release-common

%description common
Release files common to all Editions and Spins


%package notes
Summary:	Release Notes
License:	Open Publication
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	ultramarine-release-notes

%description notes
Release files for Ultramarine Linux.

######################################################################
#### Variants
######################################################################

####### Generic (Basic) #######

%if %{with basic}

%package basic
Summary:		Generic release files for Ultramarine Linux
RemovePathPostfixes: .basic
Provides:		ultramarine-release-variant = %{version}-%{release}
Provides:		system-release-variant = %{version}-%{release}
Provides:		base-module(platform:f%{version}) = %{version}-%{release}
Requires:		ultramarine-release-common = %{version}-%{release}
Provides:		generic-release-variant = %{version}-%{release}
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-basic
%description basic
%{summary}

%package identity-basic
Summary:		Package providing the basic Ultramarine identity

RemovePathPostfixes: .basic
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Provides:		generic-release-identity = %{version}-%{release}

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
Provides:		ultramarine-release-variant = %{version}-%{release}
Provides:		base-module(platform:f%{version}) = %{version}-%{release}
Provides:		system-release-product = %{version}-%{release}
Requires:		ultramarine-release-common = %{version}-%{release}
Provides:		generic-release-variant = %{version}-%{release}
Provides:		system-release-variant = %{version}-%{release}
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-flagship
%description flagship
Provides a base package for Ultramarine Flagship configurations.


%package identity-flagship
Summary:		Package providing the Ultramarine Flagship Identity

RemovePathPostfixes: .flagship
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Provides:		generic-release-identity = %{version}-%{release}

%description identity-flagship
Provides the necessary files for a Ultramarine Flagship installation.

%endif

######################################################################
####### Pantheon #######

%if %{with pantheon}
%package pantheon
Summary:		Base package for Ultramarine Pantheon-specific default configurations

RemovePathPostfixes: .pantheon
Provides:		ultramarine-release-variant = %{version}-%{release}
Provides:		system-release-product = %{version}-%{release}
Provides:		base-module(platform:f%{version}) = %{version}-%{release}
Requires:		ultramarine-release-common = %{version}-%{release}
Provides:		generic-release-variant = %{version}-%{release}
Provides:		system-release-variant = %{version}-%{release}
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
Provides:		generic-release-identity = %{version}-%{release}

%description identity-pantheon
Provides the necessary files for a Ultramarine Pantheon installation.

%endif

######################################################################
####### KDE #######

%if %{with kde}
%package kde
Summary:		Base package for Ultramarine KDE-specific default configurations

RemovePathPostfixes: .kde
Provides:		ultramarine-release-variant = %{version}-%{release}
Provides:		system-release-product = %{version}-%{release}
Provides:		base-module(platform:f%{version}) = %{version}-%{release}
Requires:		ultramarine-release-common = %{version}-%{release}
Provides:		generic-release-variant = %{version}-%{release}
Provides:		system-release-variant = %{version}-%{release}
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
Provides:		generic-release-identity = %{version}-%{release}

%description identity-kde

Provides the necessary files for a Ultramarine KDE installation.

%endif
######################################################################
####### GNOME #######

%if %{with gnome}

%package gnome
Summary:		Base package for Ultramarine GNOME-specific default configurations

RemovePathPostfixes: .gnome
Provides:		ultramarine-release-variant = %{version}-%{release}
Provides:		system-release-product = %{version}-%{release}
Provides:		base-module(platform:f%{version}) = %{version}-%{release}
Requires:		ultramarine-release-common = %{version}-%{release}
Provides:		generic-release-variant = %{version}-%{release}
Provides:		system-release-variant = %{version}-%{release}
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-gnome
%description gnome
Provides a base package for Ultramarine GNOME configurations.

%package identity-gnome
Summary:		Package providing the Ultramarine GNOME Identity

RemovePathPostfixes: .gnome
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Provides:		generic-release-identity = %{version}-%{release}

%description identity-gnome
Provides the necessary files for a Ultramarine GNOME installation.

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
echo "VARIANT_ID=Flagship" >> %{buildroot}%{_prefix}/lib/os-release.flagship
sed -i -e "s|(%{release_name}%{?prerelease})|(Flagship Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.flagship
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Flagship/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.flagship
%endif

%if %{with pantheon}
# Pantheon
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.pantheon
echo "VARIANT=\"Pantheon Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.pantheon
echo "VARIANT_ID=Pantheon" >> %{buildroot}%{_prefix}/lib/os-release.pantheon
sed -i -e "s|(%{release_name}%{?prerelease})|(Pantheon Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.pantheon
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Pantheon/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.pantheon
%endif

%if %{with kde}
# KDE
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT=\"KDE Plasma Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT_ID=KDE" >> %{buildroot}%{_prefix}/lib/os-release.kde
sed -i -e "s|(%{release_name}%{?prerelease})|(KDE Plasma Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kde
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/KDE Plasma/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.kde
%endif

%if %{with gnome}
# GNOME
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.gnome
echo "VARIANT=\"GNOME Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.gnome
echo "VARIANT_ID=GNOME" >> %{buildroot}%{_prefix}/lib/os-release.gnome
sed -i -e "s|(%{release_name}%{?prerelease})|(GNOME Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.gnome
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/GNOME/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.gnome
%endif


# Create copr config file so COPR doesnt flip out and assume EPEL
# I created a PR to support this months ago, but completely forgot about it
# to the point that risiOS managed to beat us to it - Cappy
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/dnf/plugins/copr.d/
cat <<EOF >> %{buildroot}%{_sysconfdir}/dnf/plugins/copr.d/copr.vendor.conf
[main]
releasever = %{version}
distribution = fedora

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

#########################



#Budgie config
mkdir -p %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE13} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE14} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-lightdm-gtk-greeter.conf

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




%files common
%{_sysconfdir}/dnf/plugins/copr.d/copr.vendor.conf
%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
%license licenses/LICENSE licenses/README.license
%{_prefix}/lib/ultramarine-release
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

%if %{with pantheon}
%files pantheon
%files identity-pantheon
%{_prefix}/lib/os-release.pantheon
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.pantheon
%endif

%if %{with kde}
%files kde
%files identity-kde
%{_prefix}/lib/os-release.kde
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.kde
%endif

%if %{with gnome}
%files gnome
%files identity-gnome
%{_prefix}/lib/os-release.gnome
%attr(0644,root,root) %{_swidtagdir}/org.ultramarinelinux.Ultramarine-edition.swidtag.gnome
%endif

%files notes
%doc readme/README.Ultramarine-Release-Notes

%changelog
%autochangelog
