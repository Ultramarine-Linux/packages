Name:			pipewire-systemd-mask
Version:		0
Release:		1%?dist
Summary:		Mask pipewire.service and pipewire.socket
License:		MIT
Requires:		systemd
Requires:		pipewire

%description
%summary so that Pipewire will not run in sudo.

There is a bug where Pipewire runs when sudo is executed, causing
the audio to reset to 41 every single time. This fixes the issue.

%install
mkdir -p %buildroot%_sysconfdir/systemd/system %buildroot/root/.config/systemd/user
ln -s /dev/null %buildroot%_sysconfdir/systemd/system/pipewire.socket
ln -s /dev/null %buildroot%_sysconfdir/systemd/system/pipewire.service
ln -s /dev/null %buildroot/root/.config/systemd/user/pipewire.socket
ln -s /dev/null %buildroot/root/.config/systemd/user/pipewire.service

%files
%_sysconfdir/systemd/system/pipewire.socket
%_sysconfdir/systemd/system/pipewire.service
/root/.config/systemd/user/pipewire.socket
/root/.config/systemd/user/pipewire.service
