Name:           ultramarine-server-oobe
Version:        0.1.0
Release:        1%{?dist}
Summary:        Local first-run setup for Ultramarine Server
License:        AGPL-3.0-only AND Apache-2.0 AND OFL-1.1 AND LicenseRef-Proprietary
URL:            https://github.com/Ultramarine-Linux/server-oobe
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  anda-srpm-macros
BuildRequires:  nodejs
BuildRequires:  nodejs-license-checker
BuildRequires:  pnpm
BuildRequires:  systemd-rpm-macros

Requires:       tetra
Requires:       nodejs

Packager:       Cypress Reed <cypress@fyralabs.com>

%description
Ultramarine Server OOBE is a standalone local web application that guides
users through the first-run setup of an Ultramarine Server host.

%prep
%autosetup -n server-oobe-%{version}

%build
%__pnpm install --frozen-lockfile
%__pnpm build

%install
mkdir -p %{buildroot}%{_datadir}/ultramarine-server-oobe
mkdir -p %{buildroot}%{_sharedstatedir}/ultramarine-server-oobe

# the Atkinson Hyperlegible Next font is compiled into build/ from this
# build-time-only dependency; OFL-1.1 requires shipping the license text.
# must be copied before node_modules is rebuilt below without devDependencies
cp node_modules/@fontsource-variable/atkinson-hyperlegible-next/LICENSE LICENSE.font

# adapter-node externalises packages in "dependencies" instead of bundling
# them, so the production node_modules must ship alongside build/.
# reinstall from scratch: pnpm leaves orphaned dev packages behind in
# node_modules/.pnpm if you only flip an existing install to --prod
rm -rf node_modules
%__pnpm install --frozen-lockfile --prod
%npm_license -o LICENSE.dependencies

cp -r build/* %{buildroot}%{_datadir}/ultramarine-server-oobe/
cp -a node_modules %{buildroot}%{_datadir}/ultramarine-server-oobe/
cp package.json %{buildroot}%{_datadir}/ultramarine-server-oobe/

# distinct basename so it doesn't collide with the main LICENSE in %%_licensedir
cp src/lib/icons/LICENSE LICENSE.icons

install -Dpm644 ultramarine-server-oobe.service %{buildroot}%{_unitdir}/ultramarine-server-oobe.service

%post
%systemd_post ultramarine-server-oobe.service

%preun
%systemd_preun ultramarine-server-oobe.service

%postun
%systemd_postun_with_restart ultramarine-server-oobe.service

%files
%doc README.md
%license LICENSE LICENSE.dependencies LICENSE.icons LICENSE.font
%{_datadir}/ultramarine-server-oobe
%{_unitdir}/ultramarine-server-oobe.service
%dir %attr(0750, root, root) %{_sharedstatedir}/ultramarine-server-oobe

%changelog
%autochangelog
