Summary:        Operating System AppStream Metadata for Ultramarine Linux
Name:           ultramarine-appstream-metadata
# Use the time of the last metadata update as version
Version:        20241127
Release:        %autorelease
License:        MIT
URL:            https://ultramarine-linux.org/
Source0:        https://github.com/Ultramarine-Linux/ultramarine-appstream-metadata/archive/refs/tags/%version.tar.gz
BuildArch:      noarch

%description
Operating System AppStream Metadata for Ultramarine Linux

%prep
%autosetup
# only appstream 1.0 knows about "snapshot" releases
%if 0%{?fedora} < 40
sed -i '/<release / s/type="snapshot"/type="development"/' org.ultramarine-linux.ultramarine.metainfo.xml
%endif

%build

%install
install -Dpm 0644 org.ultramarine-linux.ultramarine.metainfo.xml %{buildroot}%{_datadir}/metainfo/org.ultramarine-linux.ultramarine.metainfo.xml

%files
%{_datadir}/metainfo/org.ultramarine-linux.ultramarine.metainfo.xml

%changelog
%autochangelog
