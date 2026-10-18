# taidan_proc_macros is a git submodule, which GitHub's release tarballs leave
# out.
%global proc_macros_commit 56d5a78e5a30c87ebc274c840e85509d986c4356

# The OOBE authenticates with Tetra's setup-session API.
# FIX: placeholder. Set to the first tetra release that ships the setup-session API.
%global tetra_min_version 0.3.0

Name:           ultramarine-server-oobe
Version:        0.2.8
Release:        1%{?dist}
Summary:        Local first-run setup for Ultramarine Server
SourceLicense:  GPL-3.0-or-later
License:        %{sourcelicense} AND OFL-1.1 AND LicenseRef-Proprietary AND Apache-2.0 AND MIT AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND (Unlicense OR MIT) AND Unicode-3.0 AND Zlib
URL:            https://github.com/Ultramarine-Linux/taidan

ExclusiveArch:  x86_64 aarch64

BuildRequires:  anda-srpm-macros
BuildRequires:  cargo-rpm-macros
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libxcrypt)
BuildRequires:  pkgconfig(openssl)
# taidan_proc_macros::keymap! reads /usr/share/X11/xkb/rules/evdev.lst at compile time
BuildRequires:  xkeyboard-config
BuildRequires:  nodejs
BuildRequires:  nodejs-license-checker
BuildRequires:  pnpm
BuildRequires:  systemd-rpm-macros

Requires:       tetra >= %{tetra_min_version}
Requires:       nodejs

Packager:       Cypress Reed <cypress@fyralabs.com>

%description
Ultramarine Server OOBE is a local web application that guides users through
the first-run setup of an Ultramarine Server host. It runs unprivileged and
makes every host change through Tetra.

%prep
%git_clone %{url}
%cargo_prep_online

%build
%__pnpm --dir server-oobe install --frozen-lockfile
%__pnpm --dir server-oobe build
# %%cargo_build has no -p, and without it cargo builds the desktop taidan
# package at the workspace root; build only tdnx, as the macro would.
%{__cargo} build -j${RPM_BUILD_NCPUS} -Z avoid-dev-deps --profile rpm \
    -p tdnx --no-default-features --features server-oobe
# %%cargo_license_online covers the whole workspace (the desktop app's GTK
# stack included); list only what is linked into tdnx, same filters as the macro.
set -o pipefail
%{__cargo} tree -Z avoid-dev-deps -p tdnx --no-default-features --features server-oobe \
    --edges no-build,no-dev,no-proc-macro --no-dedupe --target all \
    --prefix none --format "{l}: {p}" \
    | sed -e "s: ($(pwd)[^)]*)::g" -e ':b; s/^\([^:]*\)\//\1 OR /; tb' \
    | sort -u > LICENSE.cargo-dependencies

%install
install -dm755 %{buildroot}%{_datadir}/ultramarine-server-oobe

# the Atkinson Hyperlegible Next font is compiled into build/ from this
# build-time-only dependency; OFL-1.1 requires shipping the license text.
# must be copied before node_modules is rebuilt below without devDependencies
install -m644 server-oobe/node_modules/@fontsource-variable/atkinson-hyperlegible-next/LICENSE LICENSE.font

# adapter-node externalises packages in "dependencies" (ws, @fluent/bundle)
# instead of bundling them, so the production node_modules must ship
# alongside build/. reinstall from scratch: pnpm leaves orphaned dev packages
# behind in node_modules/.pnpm if you only flip an existing install to --prod
rm -rf server-oobe/node_modules
%__pnpm --dir server-oobe install --frozen-lockfile --prod
pushd server-oobe
%npm_license -o ../LICENSE.npm-dependencies
popd

# install(1) cannot recurse, so the build output and node_modules trees
# are copied with cp -a (preserves the pnpm symlink layout)
cp -a server-oobe/build/. %{buildroot}%{_datadir}/ultramarine-server-oobe/
cp -a server-oobe/node_modules %{buildroot}%{_datadir}/ultramarine-server-oobe/
install -m644 server-oobe/package.json %{buildroot}%{_datadir}/ultramarine-server-oobe/package.json

# distinct basename so it doesn't collide with the main LICENSE in %%_licensedir
install -m644 server-oobe/src/lib/icons/LICENSE LICENSE.icons

install -Dpm755 target/rpm/tdnx %{buildroot}%{_libexecdir}/ultramarine-server-oobe/tdnx
install -Dpm644 server-oobe/ultramarine-server-oobe.service %{buildroot}%{_unitdir}/ultramarine-server-oobe.service
install -Dpm644 server-oobe/ultramarine-server-oobe.sysusers.conf %{buildroot}%{_sysusersdir}/ultramarine-server-oobe.conf

%post
%systemd_post ultramarine-server-oobe.service

%preun
%systemd_preun ultramarine-server-oobe.service

%postun
%systemd_postun_with_restart ultramarine-server-oobe.service

%files
%doc server-oobe/README.md
%license LICENSE.md LICENSE.cargo-dependencies LICENSE.npm-dependencies LICENSE.icons LICENSE.font
%{_datadir}/ultramarine-server-oobe
%dir %{_libexecdir}/ultramarine-server-oobe
%{_libexecdir}/ultramarine-server-oobe/tdnx
%{_unitdir}/ultramarine-server-oobe.service
%{_sysusersdir}/ultramarine-server-oobe.conf

%changelog
* Sun Oct 18 2026 Cypress Reed <cypress@fyralabs.com>
- Build from taidan's server-oobe/ and tdnx

* Thu Jul 30 2026 Cypress Reed <cypress@fyralabs.com>
- Initial package release
