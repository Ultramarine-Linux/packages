Summary:        Operating System AppStream Metadata for Ultramarine Linux
Name:           ultramarine-appstream-metadata
# Use the time of the last metadata update as version
Version:        20251125
Release:        2%?dist
License:        MIT
URL:            https://ultramarine-linux.org/
Source0:        https://github.com/Ultramarine-Linux/ultramarine-appstream-metadata/archive/refs/tags/%version.tar.gz
BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup

%build

%install
install -Dpm 0644 org.ultramarine-linux.ultramarine.metainfo.xml %{buildroot}%{_metainfodir}/org.ultramarine-linux.ultramarine.metainfo.xml

%files
%{_metainfodir}/org.ultramarine-linux.ultramarine.metainfo.xml

%changelog
%autochangelog
