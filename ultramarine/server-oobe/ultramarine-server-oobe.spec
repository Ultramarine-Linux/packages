# tdnx (the libtaidan validation bridge) lives in the taidan workspace; only
# that binary is built from it. bumped by update.rhai
%global taidan_commit d52f1587eacbf724cf4bdb27424efe6b8bddc6c5
%global taidan_url https://github.com/Ultramarine-Linux/taidan
%global taidan_dir %{rpmbuilddir}/taidan
# tdnx sources live outside buildsubdir, so find-debuginfo finds none
%undefine _debugsource_packages

Name:           ultramarine-server-oobe
Version:        0.1.1
Release:        1%{?dist}
Summary:        Local first-run setup for Ultramarine Server
SourceLicense:  AGPL-3.0-only AND GPL-3.0-or-later
# tdnx crate licenses: cargo tree -p tdnx --no-default-features --features server-oobe
License:        AGPL-3.0-only AND Apache-2.0 AND OFL-1.1 AND LicenseRef-Proprietary AND GPL-3.0-or-later AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND MIT AND (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND Unicode-3.0 AND (Unlicense OR MIT) AND Zlib
URL:            https://github.com/Ultramarine-Linux/server-oobe
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  anda-srpm-macros
BuildRequires:  cargo-rpm-macros
BuildRequires:  git-core
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libxcrypt)
BuildRequires:  pkgconfig(openssl)
# taidan_proc_macros::keymap! reads rules/evdev.lst at compile time
BuildRequires:  xkeyboard-config
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
# %%git_clone cds into the checkout and sets buildsubdir, so clone taidan and
# prep cargo there first; %%autosetup then resets buildsubdir to the app
%git_clone %{taidan_url} %{taidan_commit}
%cargo_prep_online
%autosetup -n server-oobe-%{version}

%build
%__pnpm install --frozen-lockfile
%__pnpm build

pushd %{taidan_dir}
%{__cargo} build --profile rpm --locked -p tdnx --no-default-features --features server-oobe
# %%cargo_license_online is hardcoded to --workspace, which would pull in the
# desktop app's deps; only tdnx ships here
%{shrink:
%{__cargo} tree -Z avoid-dev-deps -p tdnx --no-default-features --features server-oobe
  --edges no-build,no-dev,no-proc-macro --no-dedupe --target all
  --prefix none --format "{l}: {p}"
} | sed -e "s: ($(pwd)[^)]*)::g" -e ":b; s/^\([^:]*\)*\//\1 OR /; tb;" | sort -u > $OLDPWD/LICENSE.tdnx.dependencies
popd

%install
install -dm755 %{buildroot}%{_datadir}/ultramarine-server-oobe
install -dm750 %{buildroot}%{_sharedstatedir}/ultramarine-server-oobe

# the Atkinson Hyperlegible Next font is compiled into build/ from this
# build-time-only dependency; OFL-1.1 requires shipping the license text.
# must be copied before node_modules is rebuilt below without devDependencies
install -m644 node_modules/@fontsource-variable/atkinson-hyperlegible-next/LICENSE LICENSE.font

# adapter-node externalises packages in "dependencies" instead of bundling
# them, so the production node_modules must ship alongside build/.
# reinstall from scratch: pnpm leaves orphaned dev packages behind in
# node_modules/.pnpm if you only flip an existing install to --prod
rm -rf node_modules
%__pnpm install --frozen-lockfile --prod
%npm_license -o LICENSE.dependencies

# install(1) cannot recurse, so the build output and node_modules trees
# are copied with cp -a (preserves the pnpm symlink layout)
cp -a build/. %{buildroot}%{_datadir}/ultramarine-server-oobe/
cp -a node_modules %{buildroot}%{_datadir}/ultramarine-server-oobe/
install -m644 package.json %{buildroot}%{_datadir}/ultramarine-server-oobe/package.json

# distinct basename so it doesn't collide with the main LICENSE in %%_licensedir
install -m644 src/lib/icons/LICENSE LICENSE.icons

install -Dpm644 ultramarine-server-oobe.service %{buildroot}%{_unitdir}/ultramarine-server-oobe.service
install -Dpm644 ultramarine-server-oobe.sysusers.conf %{buildroot}%{_sysusersdir}/ultramarine-server-oobe.conf
install -Dpm755 %{taidan_dir}/target/rpm/tdnx %{buildroot}%{_libexecdir}/ultramarine-server-oobe/tdnx

%post
%systemd_post ultramarine-server-oobe.service

%preun
%systemd_preun ultramarine-server-oobe.service

%postun
%systemd_postun_with_restart ultramarine-server-oobe.service

%files
%doc README.md
%license LICENSE LICENSE.dependencies LICENSE.icons LICENSE.font LICENSE.tdnx.dependencies
%{_datadir}/ultramarine-server-oobe
%{_libexecdir}/ultramarine-server-oobe/
%{_unitdir}/ultramarine-server-oobe.service
%{_sysusersdir}/ultramarine-server-oobe.conf
%dir %attr(0750, ultramarine-oobe, ultramarine-oobe) %{_sharedstatedir}/ultramarine-server-oobe

%changelog
* Thu Jul 30 2026 Cypress Reed <cypress@fyralabs.com>
- Initial package release
