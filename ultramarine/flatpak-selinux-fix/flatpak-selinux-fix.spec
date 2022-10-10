%global selinux_variants mls targeted
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)
%global modulename flatpak-timeout-fix

Name:           flatpak-selinux-fix
Version:        1
Release:        1%{?dist}
Summary:        A .pp file to fix Flatpak on SELinux
License:        GPL v3
URL:            https://github.com/risiOS/risiOS-meta

BuildRequires:  checkpolicy, selinux-policy-devel, hardlink
%if "%{selinux_policyver}" != ""
Requires:       selinux-policy >= %{selinux_policyver}
%endif
Requires(post):   /usr/sbin/semodule, /sbin/fixfiles, flatpak
Requires(postun): /usr/sbin/semodule

%description
Fixes an issue where SELinux will not allow Flatpak to install a package.

%prep
mkdir SELinux

%build
cd SELinux
cat > flatpak-timeout-fix.te <<EOF
module flatpak-timeout-fix 1.0;
require {
	type accountsd_t;
	type flatpak_helper_t;
	class dbus send_msg;
}
#============= accountsd_t ==============
allow accountsd_t flatpak_helper_t:dbus send_msg;
EOF

for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv flatpak-timeout-fix.pp flatpak-timeout-fix.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -

%install
cd SELinux
for selinuxvariant in %{selinux_variants}
do
  mkdir -p %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 %{modulename}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
done
cd -

/usr/bin/hardlink -cv %{buildroot}%{_datadir}/selinux

%clean
rm -rf %{buildroot}

%post
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp &> /dev/null || :
done

%postun
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{modulename} &> /dev/null || :
  done
fi

%files
%defattr(-,root,root,0755)
%{_datadir}/selinux/*/%{modulename}.pp

%changelog
* Mon Jul 31 2006 John Doe <doe@example.com> 0.01-1
- Initial version