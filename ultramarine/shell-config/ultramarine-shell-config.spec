Name:           ultramarine-shell-config
Version:        45
Release:        3%{?dist}
Summary:        Shell configuration for Ultramarine Linux
License:        MIT

Source0:        ultramarine-shell.bash
Source1:        ultramarine-shell.zsh
Source2:        ultramarine-shell.sh
Source3:        starship.toml
Source4:        50-ultramarine-pwfeedback

Requires:       zsh-autosuggestions
Requires:       zsh-syntax-highlighting
Requires:       starship
Requires:       fzf

BuildArch:      noarch

%description
This package contains shell configurations made for Ultramarine Linux.

%prep

%build

%install
install -Dpm 644 %{SOURCE0} -t %{buildroot}/%{_datadir}/%{name}
install -Dpm 644 %{SOURCE1} %{buildroot}/%{_datadir}/%{name}
install -Dpm 644 %{SOURCE3} %{buildroot}/%{_datadir}/%{name}
install -Dpm 644 %{SOURCE2} -t %{buildroot}/%{_sysconfdir}/profile.d/
install -Dpm 440 %{SOURCE4} -t %{buildroot}/%{_sysconfdir}/sudoers.d/

%post

if [ -f %{_sysconfdir}/bashrc ]; then
    cat %{_datadir}/%{name}/ultramarine-shell.bash >> %{_sysconfdir}/skel/.bashrc
fi

if [ -f %{_sysconfdir}/zshrc ]; then
    cat %{_datadir}/%{name}/ultramarine-shell.zsh >> %{_sysconfdir}/skel/.zshrc
fi

if [ -f %{_sysconfdir}/default/useradd ]; then
    sed -i 's/SHELL=\/bin\/bash/SHELL=\/usr\/bin\/zsh/g' %{_sysconfdir}/default/useradd
fi

%files
%{_datadir}/%{name}/
%{_sysconfdir}/profile.d/ultramarine-shell.sh
%{_sysconfdir}/sudoers.d/50-ultramarine-pwfeedback

%changelog
* Tue Nov 03 2026 Its-J <jonah@fyralabs.com> - 45-2
- Extend Home/End support
- Search history using current input prefix
- Undo/redo
- Case-insensitive completion
- Colored completion lists
- Bash-style text splitting

* Wed Mar 25 2026 madonuko <mado@fyralabs.com> - 44-2

* Sun Oct 19 2025 Jaiden Riordan <jade@fyralabs.com> - 43-1
- Copy rewrite

* Mon Oct 10 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 1.2.2
- Move all configs to skel

* Mon Jun 13 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 1.2
- ZSH History fix

* Wed Jun 08 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 1.0
- Initial Release
