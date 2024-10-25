%global commit_firmware_long cb9500d6021e083a182ba168fe4424e3db2494cf
%global commit_linux_long 4fc5a03ad1d2fb811d8652be67260312fa3125fc

ExclusiveArch: aarch64 armv7hl

%undefine _debugsource_packages

%ifarch aarch64
%define Arch arm64
%define build_image Image
%define armtarget 8
%define with_rpi4 1
%else
%define Arch arm
%define build_image zImage
%define armtarget 7
%bcond_with rpi4
%endif

%if %{with rpi4}
%ifarch aarch64
%define local_version v8
%else
%define local_version v7l
%endif
%define bcmmodel 2711
%define ksuffix 4
%else
%define local_version v7
%define bcmmodel 2709
%endif
%define extra_version 1

%define kversion 6.1
%define patchlevel 31

Name:           rpi
Version:        %{kversion}.%{patchlevel}
Release:        %{local_version}.%{extra_version}%{?dist}
Summary:        Kernel and bootcode for Raspberry Pi, ported from AlmaLinux

License:        GPLv2
URL:            https://github.com/raspberrypi/linux
Source0:        https://www.kernel.org/pub/linux/kernel/v6.x/linux-%{kversion}.tar.xz
Source1:        https://github.com/raspberrypi/firmware/archive/%{commit_firmware_long}.tar.gz
%if %{patchlevel} > 0
Source2:        https://cdn.kernel.org/pub/linux/kernel/v6.x/patch-%{version}.xz
%endif
Source3:        rpi-6.1.x.patch

BuildRequires: kmod, patch, bash, coreutils, tar
BuildRequires: bzip2, xz, findutils, gzip, m4, perl, perl-Carp, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, git
BuildRequires: net-tools, hostname, bc
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python3-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel
BuildRequires: pciutils-devel gettext ncurses-devel
BuildRequires: openssl-devel
%if 0%{?rhel} == 7
BuildRequires:  devtoolset-8-build
BuildRequires:  devtoolset-8-binutils
BuildRequires:  devtoolset-8-gcc
BuildRequires:  devtoolset-8-make
%endif

# Compile with SELinux but disable per default
#Patch100:       bcm2709_selinux_config.patch
#Patch101:       bcm2711_selinux_config.patch
# disabled this, we'll see if it works --jr

%description
This package is part of the Ultramarine Anywhere Initative. Provides the Raspberry Pi Foundation's kernel and AlmaLinux's boot proccess.

%package kernel%{?ksuffix}
Group:          System Environment/Kernel
Summary:        The Linux kernel
Provides:       kernel = %{version}-%{release}
Requires:	coreutils
#Requires:	dracut

%description kernel%{?ksuffix}
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package kernel%{?ksuffix}-devel
Group:          System Environment/Kernel
Summary:        Development package for building kernel modules to match the kernel
Provides:       kernel-devel = %{version}-%{release}
Provides:       kernel-devel-uname-r = %{version}-%{release}
Autoreq:        no
Requires(pre):  findutils
Requires:       findutils
Requires:       perl-interpreter

%description kernel%{?ksuffix}-devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.


%package firmware
Summary:        GPU firmware for the Raspberry Pi computer
License:        Redistributable, with restrictions; see LICENSE.broadcom
Obsoletes:      grub, grubby, efibootmgr
%if 0%{?rhel} >= 8
Provides:        grubby=8.40-10
%endif

%description firmware
This package contains the GPU firmware for the Raspberry Pi BCM2835 SOC
including the kernel bootloader.


%prep
%if 0%{?rhel} == 7
source scl_source enable devtoolset-8 || :
%endif
%setup -q -n linux-%{kversion}
git init
git config user.email "kernel-team@fedoraproject.org"
git config user.name "Fedora Kernel Team"
git config gc.auto 0
git add .
git commit -a -q -m "baseline"
%if %{patchlevel} > 0
xzcat %{SOURCE2} | patch -p1 -F1 -s
git commit -a -q -m "%{version}"
%endif
git am %{SOURCE3}

git am %{PATCH100}
git am %{PATCH101}

perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}/" Makefile
perl -p -i -e "s/^CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION=/" arch/%{Arch}/configs/bcm%{bcmmodel}_defconfig

%if 0%{?rhel} >= 8
# Mangle /usr/bin/python shebangs to /usr/bin/python3
# Mangle all Python shebangs to be Python 3 explicitly
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" scripts/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" scripts/diffconfig scripts/bloat-o-meter scripts/show_delta scripts/jobserver-exec
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tools/ tools/perf/scripts/python/*.py tools/kvm/kvm_stat/kvm_stat scripts/clang-tools/*.py
%endif

# This Prevents scripts/setlocalversion from mucking with our version numbers.
touch .scmversion
git commit -a -q -m "modifs"

%build
%if 0%{?rhel} == 7
source scl_source enable devtoolset-8 || :
%endif
export KERNEL=kernel%{armtarget}
make bcm%{bcmmodel}_defconfig
make %{?_smp_mflags} HOSTCFLAGS="%{?build_cflags}" HOSTLDFLAGS="%{?build_ldflags}" %{build_image} modules dtbs

%install
%if 0%{?rhel} == 7
source scl_source enable devtoolset-8 || :
%endif
# kernel
mkdir -p %{buildroot}/boot/overlays/
mkdir -p %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
cp -p -v COPYING %{buildroot}/boot/COPYING.linux-%{kversion}
%ifarch aarch64
cp -p -v arch/%{Arch}/boot/dts/broadcom/*.dtb %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot
%else
cp -p -v arch/%{Arch}/boot/dts/*.dtb %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot
%endif
cp -p -v arch/%{Arch}/boot/dts/overlays/*.dtb* %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
cp -p -v arch/%{Arch}/boot/dts/overlays/README %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
#scripts/mkknlimg arch/%{Arch}/boot/zImage %{buildroot}/boot/kernel-%{version}-%{release}.img
cp -p -v arch/%{Arch}/boot/%{build_image} %{buildroot}/boot/kernel-%{version}-%{release}.img
make INSTALL_MOD_PATH=%{buildroot} modules_install
cat > %{buildroot}/boot/config-kernel-%{version}-%{release}.inc <<__EOF__
%ifarch aarch64
arm_64bit=1
%endif
kernel kernel-%{version}-%{release}.img
initramfs initramfs-%{version}-%{release}.img followkernel
__EOF__
cp .config %{buildroot}/boot/config-%{version}-%{release}

# kernel-devel
DevelDir=/usr/src/kernels/%{version}-%{release}
mkdir -p %{buildroot}$DevelDir
# first copy everything
cp -p -v Module.symvers System.map %{buildroot}$DevelDir
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` %{buildroot}$DevelDir
# then drop all but the needed Makefiles/Kconfig files
rm -rf %{buildroot}$DevelDir/Documentation
rm -rf %{buildroot}$DevelDir/scripts
rm -rf %{buildroot}$DevelDir/include
cp .config %{buildroot}$DevelDir
cp -a scripts %{buildroot}$DevelDir
cp -a include %{buildroot}$DevelDir

if [ -d arch/%{Arch}/scripts ]; then
  cp -a arch/%{Arch}/scripts %{buildroot}$DevelDir/arch/%{_arch} || :
fi
if [ -f arch/%{Arch}/*lds ]; then
  cp -a arch/%{Arch}/*lds %{buildroot}$DevelDir/arch/%{_arch}/ || :
fi
if [ -f arch/%{Arch}/kernel/module.lds ]; then
  cp -a --parents arch/%{Arch}/kernel/module.lds %{buildroot}$DevelDir/
fi
rm -f %{buildroot}$DevelDir/scripts/*.o
rm -f %{buildroot}$DevelDir/scripts/*/*.o
cp -a --parents arch/%{Arch}/include %{buildroot}$DevelDir
# include the machine specific headers for ARM variants, if available.
if [ -d arch/%{Arch}/mach-bcm%{bcmmodel}/include ]; then
  cp -a --parents arch/%{Arch}/mach-bcm%{bcmmodel}/include %{buildroot}$DevelDir
fi
cp include/generated/uapi/linux/version.h %{buildroot}$DevelDir/include/linux
touch -r %{buildroot}$DevelDir/Makefile %{buildroot}$DevelDir/include/linux/version.h
ln -T -s $DevelDir %{buildroot}/lib/modules/%{version}-%{release}/build --force
ln -T -s build %{buildroot}/lib/modules/%{version}-%{release}/source --force

# kernel-firmware
#rm .config
#make INSTALL_FW_PATH=%{buildroot}/lib/firmware firmware_install

# firmware
#   precompiled GPU firmware and bootloader
pushd %{buildroot}
tar -xf %{_sourcedir}/%{commit_firmware_long}.tar.gz \
    firmware-%{commit_firmware_long}/boot/start* \
    firmware-%{commit_firmware_long}/boot/fixup* \
    firmware-%{commit_firmware_long}/boot/LICENCE.broadcom \
    firmware-%{commit_firmware_long}/boot/bootcode.bin \
    --strip-components=1
popd

%files kernel%{?ksuffix}
%defattr(-,root,root,-)
/lib/modules/%{version}-%{release}
/usr/share/%{name}-kernel/%{version}-%{release}
/usr/share/%{name}-kernel/%{version}-%{release}/boot
/usr/share/%{name}-kernel/%{version}-%{release}/boot/*.dtb
/boot/config-%{version}-%{release}
/boot/overlays/
/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/*
%attr(0755,root,root) /boot/kernel-%{version}-%{release}.img
%ghost /boot/initramfs-%{version}-%{release}.img
/boot/config-kernel-%{version}-%{release}.inc
%doc /boot/COPYING.linux-%{kversion}


%posttrans kernel%{?ksuffix}
if [ -f /boot/kernel%{armtarget}.img ] || [ ! -f /boot/config-kernel.inc ];then
    # if nothing exists, fall back to generating the file, but don't create it
    # if we have moved to initramfs
    cp /boot/kernel-%{version}-%{release}.img /boot/kernel%{armtarget}.img
fi
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/*.dtb /boot/
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/*.dtb* /boot/overlays/
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/README /boot/overlays/
/usr/bin/dracut /boot/initramfs-%{version}-%{release}.img %{version}-%{release}
cp /boot/config-kernel-%{version}-%{release}.inc /boot/config-kernel.inc

%postun kernel%{?ksuffix}
if [ -f /boot/kernel%{armtarget}.img ];then
    #only restore kernel%{armtarget}.img if it exists, we may have moved to initramfs
    cp $(ls -1 /boot/kernel-*-*|sort -V|tail -1) /boot/kernel%{armtarget}.img
fi
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/*.dtb /boot/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/overlays/*.dtb* /boot/overlays/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/overlays/README /boot/overlays/
cp $(ls -1 /boot/config-kernel-*-*|sort -V|tail -1) /boot/config-kernel.inc


%files kernel%{?ksuffix}-devel
%defattr(-,root,root)
/usr/src/kernels/%{version}-%{release}


#%files kernel-firmware
#%defattr(-,root,root)
#/lib/firmware/*


%files firmware
%defattr(-,root,root,-)
/boot/bootcode.bin
/boot/fixup*
/boot/start*
%doc /boot/LICENCE.broadcom

%changelog
* Thu Oct 24 2024 Jaiden Riordan <jade@fyralabs.com>
- Port to Ultramarine

* Sun Jun 04 2023 Pablo Greco <pgreco@centosproject.org> - 6.1.31
- Update to version v6.1.31

* Sun Apr 09 2023 Pablo Greco <pgreco@centosproject.org> - 6.1.23
- Update to version v6.1.23

* Sun Jan 29 2023 Pablo Greco <pgreco@centosproject.org> - 6.1.8
- Update to version v6.1.8

* Sat Dec 17 2022 Pablo Greco <pgreco@centosproject.org> - 6.1.0
- Update to version v6.1.0

* Sun Nov 27 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.80
- Update to version v5.15.80

* Sat Oct 15 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.74
- Update to version v5.5.74

* Sun Aug  7 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.59
- Update to version v5.15.59

* Sat Jul 16 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.55
- Update to version v5.15.55

* Sun Jun 19 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.48
- Update to version v5.15.48

* Sat May 21 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.41
- Update to version v5.15.41

* Sun Apr 17 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.34
- Update to version v5.15.34

* Thu Mar 17 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.29
- Update to version v5.15.29

* Sat Feb 26 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.25
- Update to version v5.15.25

* Sat Feb 12 2022 Pablo Greco <pgreco@centosproject.org> - 5.15.21
- Update to version v5.15.21

* Sat Nov  6 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.78
- Update to version v5.10.78

* Sat Oct 23 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.74
- Update to version v5.10.74

* Sat Aug 21 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.60
- Update to version v5.10.60
- Support booting from initramfs (markvnl)

* Fri Jul 23 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.52
- Update to version v5.10.52

* Wed Jun 30 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.47
- Update to version v5.10.47

* Tue Jun 15 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.43
- Update to version v5.10.43

* Sun May 23 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.39
- Update to version v5.10.39

* Sat May 22 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.38
- Update to version v5.10.38

* Sat May  1 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.33
- Update to version v5.10.33

* Sun Apr 11 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.29
- Update to version v5.10.29

* Sat Mar 13 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.23
- Update to version v5.10.23

* Sun Feb  7 2021 Pablo Greco <pgreco@centosproject.org> - 5.10.14
- Update to version v5.10.14

* Fri Dec 25 2020 Pablo Greco <pgreco@centosproject.org> - 5.10.2
- Update to version v5.10.2

* Sun Dec 20 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.84
- Update to version v5.4.84

* Sun Oct 18 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.72
- Update to version v5.4.72

* Sat Sep 12 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.65
- Update to version v5.4.65
- Build using devtoolset-8

* Sun Aug 23 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.60
- Update to version v5.4.60

* Fri Aug  7 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.56
- Update to version v5.4.56
- Redesign format to make it look more like the kernel package

* Sun Jul 26 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.53
- Update to version v5.4.53
- Add Wireguard support

* Sat Jun 27 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.49
- Update to version v5.4.49

* Thu May 21 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.42
- Update to version v5.4.42

* Sun May  3 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.38
- Update to version v5.4.38

* Sun Mar 29 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.28
- Update to version v5.4.28

* Mon Mar 16 2020 Pablo Greco <pgreco@centosproject.org> - 5.4.24
- Update to version v5.4.24

* Mon Mar 16 2020 Pablo Greco <pgreco@centosproject.org> - 4.19.110-v7.1.el7
- Update to version v4.19.110

* Sat Mar 14 2020 Pablo Greco <pgreco@centosproject.org> - 4.19.109-v7.1.el7
- Update to version v4.19.109
- Add team network driver

* Sat Feb 15 2020 Pablo Greco <pgreco@centosproject.org> - 4.19.104-v7.1.el7
- Update to version v4.19.104
- Support building in CentOS8

* Thu Jan  9 2020 Pablo Greco <pgreco@centosproject.org> - 4.19.94-v7.1.el7
- Update to version v4.19.94

* Sat Nov 16 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.84-v7.1.el7
- Update to version v4.19.84
- Build for aarch64

* Tue Sep 10 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.72-v7.1.el7
- Update to version v4.19.72

* Sun Sep 01 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.69-v7.1.el7
- Update to version v4.19.69

* Sat Jul 27 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.61-v7.1.el7
- Conditional to build kernel for rpi4
- Update to version v4.19.61

* Tue Jun 25 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.56-v7.1.el7
- Update to version v4.19.56

* Mon Jun 17 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.52-v7.1.el7
- Update to version v4.19.52

* Sat Jun 15 2019 Pablo Greco <pgreco@centosproject.org> - 4.19.51-v7.1.el7
- Update to version v4.19.51

* Thu May 16 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.43-v7.1.el7
- Update to version v4.19.43

* Mon May  6 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.40-v7.1.el7
- Update to version v4.19.40

* Sat May  4 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.39-v7.1.el7
- Update to version 4.19.39

* Fri May  3 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.38-v7.1.el7
- Update to version 4.19.38

* Sat Apr 13 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.34-v7.1.el7
- Update to version 4.19.34
- Avoid devel subpkg from pulling unnecessary deps

* Fri Mar 29 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.32-v7.1.el7
- Update to version 4.19.32

* Sat Mar 16 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.29-v7.1.el7
- Update to version 4.19.29

* Wed Mar 13 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.28-v7.1.el7
- readded kernel-devel-uname-r, fixed back in 4.14.58
- Update to version 4.19.28

* Sat Mar 09 2019 Jacco Ligthart <jacco@redsleeve.org> - 4.19.27-v7.1.el7
- update to version 4.19.27
- added 'sort -V' to the scripts
- changed download location from 'tarball' to 'archive'
- moves from 'post' script to 'posttrans'
- moved 'COPYING.linux' to 'COPYING.linux-4.19'
- added 'README' to the overlays dir

* Thu Dec 20 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.14.89-v7.1.el7
- update to version 4.14.89

* Wed Oct 10 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.14.74-v7.1.el7
- update to version 4.14.74

* Fri Aug 10 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.14.61-v7.1.el7
- update to version 4.14.61

* Fri Jun 15 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.14.49-v7.1.el7
- update to version 4.14.49

* Thu May 24 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.14.42-v7.1.el7
- update to version 4.14.42
- stop makeing the kernel-firmware subpackage

* Fri Mar 16 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.9.80-v7.2.el7
- update to latest git for raspberry pi 3 B+ support

* Wed Feb 28 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.9.80-v7.1.el7
- update to version 4.9.80, probably the last in the 4.9 series

* Sat Jan 27 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.9.78-v7.1.el7
- update to version 4.9.78

* Sun Dec 17 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.69-v7.1.el7
- update to version 4.9.69

* Mon Nov 27 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.65-v7.1.el7
- update to version 4.9.65

* Sun Oct 29 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.59-v7.1.el7
- update to version 4.9.59

* Mon Oct 02 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.52-v7.1.el7
- update to version 4.9.52

* Thu Aug 17 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.43-v7.1.el7
- update to version 4.9.43

* Sat Jul 22 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.39-v7.1.el7
- update to version 4.9.39

* Sat Jul 01 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.35-v7.1.el7
- update to version 4.9.35

* Mon Jun 19 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.33-v7.1.el7
- update to version 4.9.33

* Mon Jun 05 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.30-v7.1.el7
- update to version 4.9.30

* Fri May 12 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.27-v7.1.el7
- update to version 4.9.27

* Wed Apr 19 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.23-v7.1.el7
- update to version 4.9.23

* Thu Mar 30 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.19-v7.1.el7
- update to version 4.9.19

* Wed Mar 15 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.14-v7.1.el7
- update tp version 4.9.14

* Mon Feb 27 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.13-v7.1.el7
- update to version 4.9.13

* Sat Dec 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.39-v7.1.el7
- update to version 4.4.39

* Wed Nov 16 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.32-v7.1.el7
- update to version 4.4.32

* Fri Oct 21 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.26-v7.1.el7
- update to version 4.4.26 which includes a fix for CVE-2016-5195

* Tue Sep 27 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-v7.3.el7
- changed versioning scheme, added EXTRAVERSION to makefile
- lost dificult linking in /lib/modules
- added all dirs under /usr/share/%{name}-kernel/ to the %files

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-2
- removed dracut I don't see why we need a initramfs
- fixed the preun scripts. they blocked uninstall
- removed -b0 from %setup, the source was extracted twice

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-1
- updated to 4.4.21
- moved the Requires: to the kernel subpackage
- added /boot/overlays to the %files

* Mon Jul 11 2016 Fabian Arrotin <arrfab@centos.org> - 4.4.14-2
- Fixed the dracut call for %{release}

* Thu Jul 7 2016 Fabian Arrotin <arrfab@centos.org>
- upgrade to kernel 4.4.14
- Moved some *dtb* files to /usr/share/raspberrypi2-kernel/boot/
- Using %post to put those in /boot/*
- generating initramfs in %post

* Fri Jun 17 2016 Johnny Hughes <johnny@centos.org>
- upgrade to kernel 4.4.13
- modified to copy *.dtb* to /boot/overlays/

* Sun Mar 13 2016 Fabian Arrotin <arrfab@centos.org>
- Added kmod/libselinux as BuildRequires (for the depmod part)
- Added audit support in the bcm2709_selinux_config.patch

* Fri Mar 11 2016 Henrik Andersson <henrik.4e@gmail.com>
- updated to 4.1.19
- build kernel from source instead of using binaries from firmware
- use only GPU firmware and bootloader from firmware

* Mon Jan 25 2016 Fabian Arrotin <arrfab@centos.org>
- updated to 4.1.16
- contains the patch fro CVE-2016-0728

* Thu Jan 21 2016 Fabian Arrotin <arrfab@centos.org>
- updated to 4.1.15

* Thu Nov 26 2015 Fabian Arrotin <arrfab@centos.org>
- Added %{?dist} rpm macro in the name

* Sat Oct 24 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 4.1.11

* Fri Sep 04 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 4.1.6

* Fri Jun 26 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 4.0.6

* Sun May 10 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 3.18.13

* Sun Mar 29 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 3.18.10
- fixed a bcm2708 vs. bcm2709 issue with include dirs

* Sat Mar 14 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 3.18.9

* Fri Feb 20 2015 Jacco Ligthart <jacco@redsleeve.org>
- converted for raspberrypi model2 (kernel7 / version *-v7+ )

* Fri Feb 20 2015 Jacco Ligthart <jacco@redsleeve.org>
- update to version 3.18 (coming from 3.12)
- require coreutils