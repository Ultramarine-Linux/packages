%global is_rawhide 0
%global release_name thirtyseven

%define dist_version 37

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif


Summary:	Ultramarine Linux release files
Name:		ultramarine-release
Version:	37
Release:	%autorelease
License:	MIT
Source0:	LICENSE
Source1:	README.developers
Source2:	README.Ultramarine-Release-Notes
Source3:	README.license

Source6:	85-display-manager.preset
Source7:	90-default.preset
Source8:	99-default-disable.preset
Source9:	90-default-user.preset
Source10:   10_ultramarine-default-theme.gschema.override
Source12:   cyber-cutefish-theme.conf
Source13:   60-ultramarine-presets.conf
Source14:   lightdm-gtk-greeter.conf

Source19:   distro-template.swidtag

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

%package basic
Summary:		Base package for a standard Ultrmarine system

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
%description identity-basic
%{summary}

RemovePathPostfixes: .basic
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Provides:		generic-release-identity = %{version}-%{release}

%description identity-basic
Provides the necessary files for a Ultramarine installation that is not identifying
itself as a particular Edition or Spin.


# Budgie Desktop

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

RemovePathPostfixes: .basic
Provides:		ultramarine-release-identity = %{version}-%{release}
Conflicts:		ultramarine-release-identity
Provides:		generic-release-identity = %{version}-%{release}

%description identity-flagship
Provides the necessary files for a Ultramarine Flagship installation.

# Cutefish Desktop

%package cutefish
Summary:		Base package for Fedora Cutefish-specific default configurations

RemovePathPostfixes: .cutefish
Provides:		ultramarine-release-variant = %{version}-%{release}
Provides:		base-module(platform:f%{version}) = %{version}-%{release}
Requires:		ultramarine-release-common = %{version}-%{release}
Provides:		generic-release-variant = %{version}-%{release}
Provides:		system-release-variant = %{version}-%{release}
# ultramarine-release-common Requires: ultramarine-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# ultramarine-release-identity-cinnamon if nothing else is already doing so.
Recommends:		ultramarine-release-identity-basic

%description cutefish
Provides a base package for Ultramarine Cutefish configurations.

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
ln -s ultramarine-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME="Ultramarine Linux"
ID=ultramarine
VERSION=%{version}
VERSION_CODENAME=thirtyseven
ID_LIKE=fedora
PLATFORM_ID="platform:um%{dist_version}"
VERSION_ID=%{dist_version}
PRETTY_NAME="Ultramarine Linux %{dist_version}"
ANSI_COLOR="0;34"
LOGO=ultramarine
CPE_NAME="cpe:/o:ultramarine:um:%{dist_version}"
HOME_URL="http://ultramarine-linux.org"
SUPPORT_URL="https://discord.com/invite/bUuQasHdrF"
BUG_REPORT_URL="https://youtu.be/HxkmXnRQblE"
DOCUMENTATION_URL="https://wiki.ultramarine-linux.org"
REDHAT_BUGZILLA_PRODUCT="Fedora Linux"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{dist_version}
REDHAT_SUPPORT_PRODUCT="Fedora Linux"
REDHAT_SUPPORT_PRODUCT_VERSION=%{dist_version}
PRIVACY_POLICY_URL="https://youtu.be/dQw4w9WgXcQ"
EOF

# provide upstream-release files for debian based apps
install -d $RPM_BUILD_ROOT/etc/upstream-release
cat << EOF >>$RPM_BUILD_ROOT/etc/upstream-release/lsb-release
ID=Fedora
VERSION_ID=36
VERSION_CODENAME="Thirty Six"
PRETTY_NAME="Fedora Linux 36 (Thirty Six)"
EOF

# Create custom Anaconda config
mkdir -p %{buildroot}%{_sysconfdir}/anaconda/profile.d/
touch %{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
cat << EOF >>%{buildroot}%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
# Anaconda configuration file for Ultramarine Linux
[Anaconda]
addons_enabled = True
# List of enabled kickstart modules.
kickstart_modules =
    org.fedoraproject.Anaconda.Modules.Timezone
    org.fedoraproject.Anaconda.Modules.Network
    org.fedoraproject.Anaconda.Modules.Localization
    org.fedoraproject.Anaconda.Modules.Users
    org.fedoraproject.Anaconda.Modules.Payloads
    org.fedoraproject.Anaconda.Modules.Storage
    org.fedoraproject.Anaconda.Modules.Services


[Profile]
# Define the profile.
profile_id = ultramarine

[Profile Detection]
# Match os-release values.
os_id = ultramarine

[Network]
default_on_boot = FIRST_WIRED_WITH_LINK

[Bootloader]
efi_dir = fedora

[Storage]
default_scheme = BTRFS
btrfs_compression = zstd:1

[User Interface]
default_help_pages =
    FedoraPlaceholder.txt
    FedoraPlaceholder.html
    FedoraPlaceholderWithLinks.html

custom_stylesheet = /usr/share/anaconda/pixmaps/ultramarine.css
hidden_spokes =
    PasswordSpoke


[Payload]
default_source = CLOSEST_MIRROR

default_rpm_gpg_keys =
    /etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-\$releasever-\$basearch

updates_repositories =
    updates
    updates-modular
    ultramarine-updates


EOF

#basic placeholder
mkdir -p %{buildroot}%{_prefix}/lib/
cp -pv %{buildroot}%{_prefix}/lib/os-release %{buildroot}%{_prefix}/lib/os-release.basic

# Set up gschemas
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install %{SOURCE10} %{buildroot}%{_datadir}/glib-2.0/schemas/

#Budgie config
mkdir -p %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE13} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/
install %{SOURCE14} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-lightdm-gtk-greeter.conf

#set up Cutefish config
mkdir -p %{buildroot}%{_sysconfdir}/skel/.config/cutefishos/
install %{SOURCE12} %{buildroot}%{_sysconfdir}/skel/.config/cutefishos/theme.conf

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

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


# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE19} > %{buildroot}%{_swidtagdir}/org.ultramarine.Ultramarine-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s %{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/ultramarine-linux.org


%files common
%{_sysconfdir}/anaconda/profile.d/ultramarine.conf
%license licenses/LICENSE licenses/README.license
%{_prefix}/lib/ultramarine-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/upstream-release/
%{_sysconfdir}/ultramarine-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/org.ultramarine.Ultramarine-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d

%files
%{_prefix}/lib/os-release


%files notes
%doc readme/README.Ultramarine-Release-Notes

%files basic
%{_prefix}/lib/os-release.basic

%files identity-basic
%{_datadir}/glib-2.0/schemas/10_ultramarine-default-theme.gschema.override

%files flagship
%{_sysconfdir}/lightdm/lightdm.conf.d/60-ultramarine-presets.conf
%{_sysconfdir}/lightdm/lightdm.conf.d/50-ultramarine-lightdm-gtk-greeter.conf

%files cutefish
%{_sysconfdir}/skel/.config/cutefishos/theme.conf

%changelog
* Tue Feb 22 2022 Ultramarine Release Tracking Service
- Mass rebuild for release um36

%autochangelog