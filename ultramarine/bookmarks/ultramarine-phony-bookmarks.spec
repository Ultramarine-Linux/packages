Name:       ultramarine-phony-bookmarks
Version:    0
Release:    3%?dist
Summary:    A substitute for fedora-bookmarks
License:    CC0
URL:        https://ultramarine-linux.org
Provides:   system-bookmarks
Conflicts:  system-bookmarks
Conflicts:  fedora-bookmarks
Obsoletes:  fedora-bookmarks < 28-31
Enhances:   ultramarine-release
BuildArch:  noarch

%description
This package substitutes / replaces fedora-bookmarks, which might be annoying
especially for Firefox users.

%prep
cat<<EOF > README
The `%name` package substitutes fedora-bookmarks.
This prevents Firefox users from getting Fedora bookmarks.
EOF

%build

%install

%files
%doc README

%changelog
