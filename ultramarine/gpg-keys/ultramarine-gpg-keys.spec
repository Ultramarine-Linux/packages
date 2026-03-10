%undefine dist

Name:           ultramarine-gpg-keys
Version:        %{?fedora}
Release:        2%?dist
Summary:        GPG keys for Ultramarine Linux
Requires:       filesystem >= 3.18-6

License:        MIT
URL:            https://ultramarine-linux.org
# We aren't pulling keys from the origin URLs, since they shouldn't change and this is easier to audit.
Source0:        RPM-GPG-KEY-um37
Source1:        RPM-GPG-KEY-um38
Source2:        RPM-GPG-KEY-um39
Source3:        RPM-GPG-KEY-um40
Source4:        RPM-GPG-KEY-um40-source
Source5:        RPM-GPG-KEY-um41
Source6:        RPM-GPG-KEY-um41-source
Source7:        RPM-GPG-KEY-um42
Source8:        RPM-GPG-KEY-um42-source
Source9:        RPM-GPG-KEY-um43
Source10:       RPM-GPG-KEY-um43-source
Source11:       RPM-GPG-KEY-um44
Source12:       RPM-GPG-KEY-um44-source
Source13:       RPM-GPG-KEY-umrawhide
Source14:       RPM-GPG-KEY-umrawhide-source
BuildArch:      noarch

%description
GPG keys for Ultramarine Linux, used for verifying RPM package signatures.

%package -n     ultramarine-mock-gpg-keys
Summary:        Ultramarine GPG keys for Mock

%description -n ultramarine-mock-gpg-keys
Ultramarine GPG key copies for use in Mock.

%prep

%build

%install
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/mock
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/mock/

%files
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*

%files -n ultramarine-mock-gpg-keys
%dir /etc/pki/mock
/etc/pki/mock/RPM-GPG-KEY-*
