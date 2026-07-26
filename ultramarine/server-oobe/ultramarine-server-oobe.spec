Name:           ultramarine-server-oobe
Version:        0.1.0
Release:        1%{?dist}
Summary:        Local first-run setup for Ultramarine Server
License:        GPL-3.0-or-later
URL:            https://github.com/Ultramarine-Linux/server-oobe

BuildRequires:  anda-srpm-macros
BuildRequires:  nodejs
BuildRequires:  pnpm
BuildRequires:  systemd-rpm-macros

Requires:       tetra
Requires:       nodejs

%description
Ultramarine Server OOBE is a standalone local web application that guides
users through the first-run setup of an Ultramarine Server host.

%prep
%git_clone %url v%version

%build
pnpm install --frozen-lockfile
pnpm build

%install
mkdir -p %{buildroot}%{_datadir}/ultramarine-server-oobe
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/ultramarine-server-oobe

cp -r build/* %{buildroot}%{_datadir}/ultramarine-server-oobe/

cat > %{buildroot}%{_unitdir}/ultramarine-server-oobe.service << 'EOF'
[Unit]
Description=Ultramarine Server OOBE
After=network.target

[Service]
Type=simple
WorkingDirectory=%{_datadir}/ultramarine-server-oobe
ExecStart=/usr/bin/node %{_datadir}/ultramarine-server-oobe/index.js
Environment=OOBE_STATE_PATH=%{_sharedstatedir}/ultramarine-server-oobe/state.json
Environment=PORT=3972
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

%post
%systemd_post ultramarine-server-oobe.service

%preun
%systemd_preun ultramarine-server-oobe.service

%postun
%systemd_postun_with_restart ultramarine-server-oobe.service

%files
%doc README.md
%{_datadir}/ultramarine-server-oobe
%{_unitdir}/ultramarine-server-oobe.service
%dir %attr(0750, root, root) %{_sharedstatedir}/ultramarine-server-oobe
