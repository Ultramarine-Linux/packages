# This package is taken from AlmaLinux, please sync from this git repo's testing branch every UM release https://git.almalinux.org/metalefty/raspberrypi
# Thank you to Koichiro Iwao (metalefty) from AlmaLinux for their work on this package
#
%global firmware_tag	1.20250915
%global version_tag	21da81b5507ac3353013dc093208e6bed53d10e2

ExclusiveArch: aarch64

%undefine _debugsource_packages

%define Arch arm64
%define build_image Image.gz
%define armtarget 8

%define local_version v8
%define bcmmodel 2711
%define extra_version 1

%define kversion 6.18
%define patchlevel 20

%if 0%{?rhel} >= 10 || 0%{?fedora} >= 40
%define pathfix %{__python3} %{_rpmconfigdir}/redhat/pathfix.py
%else
%define pathfix pathfix.py
%endif

# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# tools
%define with_tools     %{?_without_tools:     0} %{?!_without_tools:     1}
# firmware
%define with_firmware  %{?_without_firmware:  0} %{?!_without_firmware:  1}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}

Name:           kernel-rpi
Version:        %{kversion}.%{patchlevel}
Release:        20260329.%{local_version}.%{extra_version}%{?dist}
Summary:        Specific kernel and bootcode for Raspberry Pi

License:        GPL-2.0-only WITH Linux-syscall-note
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/%{version_tag}.tar.gz
Source1:        https://github.com/raspberrypi/firmware/archive/refs/tags/%{firmware_tag}.tar.gz
Patch1000: config-bcm2711.patch
Patch1001: config-bcm2712.patch
# Sources for kernel-tools
Source2000:    cpupower.service
Source2001:    cpupower.config
Source2002:    kvm_stat.logrotate

BuildRequires: kmod, patch, bash, coreutils, tar
BuildRequires: bzip2, xz, findutils, gzip, m4, perl, perl-Carp, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python3-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel
BuildRequires: pciutils-devel gettext ncurses-devel
BuildRequires: openssl-devel
%if %{with_tools}
# kernel-tools
BuildRequires: asciidoc
%endif
%if %{with_headers}
BuildRequires: rsync
%endif

%description
Specific kernel and bootcode for Raspberry Pi

%package kernel
Group:          System Environment/Kernel
Summary:        The Linux kernel
Provides:       kernel = %{version}-%{release}
Provides:       kernel-core = %{version}-%{release}
Provides:       installonlypkg(kernel)
Requires:       coreutils
Requires:       dracut
%description kernel
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

%package kernel-devel
Group:          System Environment/Kernel
Summary:        Development package for building kernel modules to match the kernel
Provides:       kernel-devel = %{version}-%{release}
Provides:       kernel-devel-uname-r = %{version}-%{release}
Provides:       installonlypkg(kernel)
Autoreq:        no
Requires(pre):  findutils
Requires:       findutils
Requires:       perl-interpreter
%description kernel-devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.

%if 0%{?rhel} >= 10
%package kernel-modules
Summary:        Pseudo package for kernel modules
Group:          System Environment/Kernel
Provides:       installonlypkg(kernel-module)
Provides:       kernel-modules = %{version}-%{release}
Provides:       kernel-modules-uname-r = %{version}-%{release}
Obsoletes:      kernel-modules < %{version}-%{release}
Requires:       %{name}-kernel = %{version}-%{release}
AutoReq:        no
AutoProv:       yes
%description kernel-modules
This package provides pseudo dependency for the packages that depends on regular
kernel-modules packages.

%package kernel-modules-core
Summary:        Pseudo package for core kernel modules
Group:          System Environment/Kernel
Provides:       installonlypkg(kernel-module)
Provides:       kernel-modules-core = %{version}-%{release}
Provides:       kernel-modules-core-uname-r = %{version}-%{release}
Obsoletes:      kernel-modules-core < %{version}-%{release}
Requires:       %{name}-kernel = %{version}-%{release}
AutoReq:        no
AutoProv:       yes
%description kernel-modules-core
This package provides pseudo dependency for the packages that depends on regular
kernel-modules-core packages.

%package kernel-modules-extra
Summary:        Pseudo package for extra kernel modules
Group:          System Environment/Kernel
Provides:       kernel-modules-extra = %{version}-%{release}
Provides:       kernel-modules-extra-uname-r = %{version}-%{release}
Provides:       installonlypkg(kernel-module)
Obsoletes:      kernel-modules-extra < %{version}-%{release}
Requires:       %{name}-kernel = %{version}-%{release}
AutoReq:        no
AutoProv:       yes
%description kernel-modules-extra
This package provides pseudo dependency for the packages that depends on regular
kernel-modules-extra packages.

%package kernel-modules-extra-matched
Summary:        Pseudo package for extra kernel modules
Group:          System Environment/Kernel
Provides:       kernel-modules-extra-matched = %{version}-%{release}
Provides:       kernel-modules-extra-matched-uname-r = %{version}-%{release}
Provides:       installonlypkg(kernel-module)
Obsoletes:      kernel-modules-extra-matched < %{version}-%{release}
Requires:       %{name}-kernel = %{version}-%{release}
AutoReq:        no
AutoProv:       yes
%description kernel-modules-extra-matched
This package provides pseudo dependency for the packages that depends on regular
kernel-modules-extra-matched packages.
%endif

%if %{with_tools}
%package kernel-tools
Summary: Assortment of tools for the Linux kernel
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: %{name}-kernel-tools-libs = %{version}-%{release}
Obsoletes: kernel-tools < %{version}
Provides: kernel-tools = %{version}-%{release}
%define __requires_exclude ^%{_bindir}/python
%description kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package kernel-tools-libs
Summary: Libraries for the kernels-tools
Obsoletes: kernel-tools-libs < %{version}
Provides: kernel-tools-libs = %{version}-%{release}
%description kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
Requires: %{name}-kernel-tools = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: %{name}-kernel-tools-libs = %{version}-%{release}
Obsoletes: kernel-tools-libs-devel < %{version}
Provides: kernel-tools-libs-devel = %{version}-%{release}
%description kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.
%endif

%if %{with_firmware}
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
%endif

%if %{with_headers}
%package kernel-headers
Obsoletes: kernel-headers < %{version}
Provides: kernel-headers = %{version}-%{release}
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
Summary: Header files for the Linux kernel for use by glibc

%description kernel-headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.
%endif

%prep
%setup -q -n linux-%{version_tag}
%patch -P 1000 -p1
%patch -P 1001 -p1
perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}/" Makefile
perl -p -i -e "s/^CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION=/" arch/%{Arch}/configs/bcm2711_defconfig
perl -p -i -e "s/^CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION=/" arch/%{Arch}/configs/bcm2712_defconfig

%if 0%{?rhel} >= 8 || 0%{?fedora} >= 28
# Mangle /usr/bin/python shebangs to /usr/bin/python3
# Mangle all Python shebangs to be Python 3 explicitly
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
%{pathfix} -pni "%{__python3} %{py3_shbang_opts}" scripts/
%{pathfix} -pni "%{__python3} %{py3_shbang_opts}" scripts/diffconfig scripts/bloat-o-meter scripts/show_delta \
                                                  scripts/jobserver-exec scripts/dtc/dt-extract-compatibles
%{pathfix} -pni "%{__python3} %{py3_shbang_opts}" tools/ tools/kvm/kvm_stat/kvm_stat
%endif

%build
# 16K page-size kernel optimized (bcmmodel=2712) for RPi 5 is not built at the moment
# to support both RPi 4 and 5.
export KERNEL=kernel%{armtarget}
make bcm%{bcmmodel}_defconfig
%if %{with_up}
make %{?_smp_mflags} HOSTCFLAGS="%{?build_cflags}" HOSTLDFLAGS="%{?build_ldflags}" %{build_image} modules dtbs
%endif

# kernel-tools
%if %{with_tools}
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false DEBUG=false
pushd tools/thermal/tmon/
make %{?_smp_mflags} HOSTCFLAGS="%{?build_cflags}" HOSTLDFLAGS="%{?build_ldflags}"
popd
pushd tools/iio/
make %{?_smp_mflags} HOSTCFLAGS="%{?build_cflags}" HOSTLDFLAGS="%{?build_ldflags}"
popd
pushd tools/gpio/
make %{?_smp_mflags} HOSTCFLAGS="%{?build_cflags}" HOSTLDFLAGS="%{?build_ldflags}"
popd
pushd tools/mm/
make %{?_smp_mflags} HOSTCFLAGS="%{?build_cflags}" HOSTLDFLAGS="%{?build_ldflags}" slabinfo page_owner_sort
popd
%endif

%install
%if %{with_up}
# kernel
mkdir -p %{buildroot}/boot/overlays/
mkdir -p %{buildroot}/usr/share/%{name}/%{version}-%{release}/boot/overlays
cp -p -v COPYING %{buildroot}/boot/COPYING.linux-%{kversion}
cp -p -v arch/%{Arch}/boot/dts/overlays/README %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
%ifarch aarch64
cp -p -v arch/%{Arch}/boot/dts/broadcom/*.dtb %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot
%else
cp -p -v arch/%{Arch}/boot/dts/*.dtb %{buildroot}/usr/share/%{name}-kernel%/%{version}-%{release}/boot
%endif
cp -p -v arch/%{Arch}/boot/dts/overlays/*.dtb* %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
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

%endif

%if %{with_firmware}
# firmware
#   precompiled GPU firmware and bootloader
pushd %{buildroot}
tar -xf %{_sourcedir}/%{firmware_tag}.tar.gz \
    firmware-%{firmware_tag}/boot/start* \
    firmware-%{firmware_tag}/boot/fixup* \
    firmware-%{firmware_tag}/boot/LICENCE.broadcom \
    firmware-%{firmware_tag}/boot/bootcode.bin \
    --strip-components=1
%{__chmod} -x %{buildroot}/boot/start*.elf
popd
%endif

%if %{with_tools}
# kernel-tools
make  -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower

install -D -m644 %{SOURCE2000} %{buildroot}%{_unitdir}/cpupower.service
install -D -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
pushd tools/thermal/tmon
make INSTALL_ROOT=%{buildroot} install
popd
pushd tools/iio
make DESTDIR=%{buildroot} install
popd
pushd tools/gpio
make DESTDIR=%{buildroot} install
popd
install -m644 -D %{SOURCE2002} %{buildroot}%{_sysconfdir}/logrotate.d/kvm_stat
pushd tools/kvm/kvm_stat
%{__make} INSTALL_ROOT=%{buildroot} install-tools
%{__make} INSTALL_ROOT=%{buildroot} install-man
install -m644 -D kvm_stat.service %{buildroot}%{_unitdir}/kvm_stat.service
popd
pushd tools/mm/
install -m755 slabinfo %{buildroot}%{_bindir}/slabinfo
install -m755 page_owner_sort %{buildroot}%{_bindir}/page_owner_sort
popd
%endif

%if %{with_headers}
%{__make} ARCH=%{Arch} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

find %{buildroot}/usr/include \
    \( -name .install -o -name .check -o \
       -name ..install.cmd -o -name ..check.cmd \) -delete
%endif

%if %{with_tools}
%post kernel-tools
%systemd_post cpupower.service

%preun kernel-tools
%systemd_preun cpupower.service

%postun kernel-tools
%systemd_postun cpupower.service

%post kernel-tools-libs
/sbin/ldconfig

%postun kernel-tools-libs
/sbin/ldconfig
%endif

%if %{with_up}
%files kernel
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


%posttrans kernel
if [ -d /usr/lib/ostree-boot ]; then
  mkdir -p /usr/lib/modules/%{version}-%{release}
  pushd /usr/lib/ostree-boot
  [ -e config-%{version}-%{release} ] && \
    mv config-%{version}-%{release} /usr/lib/modules/%{version}-%{release}/
  [ -e config-kernel-%{version}-%{release}.inc ] && \
    mv config-kernel-%{version}-%{release}.inc /usr/lib/modules/%{version}-%{release}/
  [ -e initramfs-%{version}-%{release}.img ] && \
    mv initramfs-%{version}-%{release}.img /usr/lib/modules/%{version}-%{release}/initramfs
  [ -e kernel-%{version}-%{release}.img ] && \
    mv kernel-%{version}-%{release}.img /usr/lib/modules/%{version}-%{release}/vmlinuz
  popd
fi
if [ -d /boot ]; then
  if [ -f /boot/kernel%{armtarget}.img ] || [ ! -f /boot/config-kernel.inc ];then
      # if nothing exists, fall back to generating the file, but don't create it
      # if we have moved to initramfs
      cp /boot/kernel-%{version}-%{release}.img /boot/kernel%{armtarget}.img
  fi
  cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/*.dtb /boot/
  cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/*.dtb* /boot/overlays/
  cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/README /boot/overlays/
  cp /boot/config-kernel-%{version}-%{release}.inc /boot/config-kernel.inc

  /usr/bin/dracut --no-hostonly /boot/initramfs-%{version}-%{release}.img %{version}-%{release}
  cp /boot/initramfs-%{version}-%{release}.img /boot/initramfs%{armtarget}
fi

%postun kernel
if [ -f /boot/kernel%{armtarget}.img ]; then
    #only restore kernel%{armtarget}.img if it exists, we may have moved to initramfs
    cp $(ls -1 /boot/kernel-*-*|sort -V|tail -1) /boot/kernel%{armtarget}.img
fi
if [ -f /boot/initramfs%{armtarget} ]; then
    cp $(ls -1 /boot/initramfs-*-*|sort -V| tail -1) /boot/initramfs%{armtarget}
fi
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/*.dtb /boot/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/overlays/*.dtb* /boot/overlays/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/overlays/README /boot/overlays/
cp $(ls -1 /boot/config-kernel-*-*|sort -V|tail -1) /boot/config-kernel.inc


%files kernel-devel
%defattr(-,root,root)
/usr/src/kernels/%{version}-%{release}

%if 0%{?rhel} >= 10
%files kernel-modules
# empty package
%defattr(-,root,root)

%files kernel-modules-core
# empty package
%defattr(-,root,root)

%files kernel-modules-extra
# empty package
%defattr(-,root,root)

%files kernel-modules-extra-matched
# empty package
%defattr(-,root,root)
%endif
%endif

%if %{with_tools}
%files kernel-tools -f cpupower.lang
%{_bindir}/cpupower
%{_datadir}/bash-completion/completions/cpupower
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%{_libexecdir}/cpupower
%config(noreplace) %{_sysconfdir}/cpupower-service.conf
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%{_bindir}/tmon
%{_bindir}/iio_event_monitor
%{_bindir}/iio_generic_buffer
%{_bindir}/lsiio
%{_bindir}/lsgpio
%{_bindir}/gpio-hammer
%{_bindir}/gpio-event-mon
%{_bindir}/gpio-watch
%{_mandir}/man1/kvm_stat*
%{_bindir}/kvm_stat
%{_unitdir}/kvm_stat.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kvm_stat
%{_bindir}/page_owner_sort
%{_bindir}/slabinfo

%files kernel-tools-libs
%{_libdir}/libcpupower.so.1
%{_libdir}/libcpupower.so.1.0.1

%files kernel-tools-libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_includedir}/powercap.h
%endif

%if %{with_firmware}
%files firmware
%defattr(-,root,root,-)
/boot/bootcode.bin
/boot/fixup*
/boot/start*
%doc /boot/LICENCE.broadcom
%endif

%if %{with_headers}
%files kernel-headers
/usr/include/*
%exclude %{_includedir}/cpufreq.h
%exclude %{_includedir}/internal/
%exclude %{_includedir}/perf/
%endif

%changelog
* Wed Apr 29 2026 Jaiden Riordan <jade@fyralabs.com
- Port to Ultramarine

* Wed Apr 01 2026 Koichiro Iwao <meta@almalinux.org> - 6.18.20-20260329.v8.1
- Update kernel to v6.18.20 21da81b5

* Mon Mar 02 2026 Koichiro Iwao <meta@almalinux.org> - 6.12.47-20250916.v8.2
- Add a pseudo subpackage -modules-extra-matched to resolve dependency issue

* Fri Oct 03 2025 Koichiro Iwao <meta@almalinux.org> - 6.12.47-20250916.v8.1
- Update kernel to v6.12.47 stable_20250916
- Make it buildable on Fedora

* Wed Sep 24 2025 Ryosuke Nakayama <ryosuke_666@icloud.com> - 6.12.34-20250702.v8.2
- Update firmware to 1.20250915

* Wed Jul 09 2025 Koichiro Iwao <meta@almalinux.org> - 6.12.34-20250702.v8.1
- Update kernel to v6.12.34 stable_20240702

* Mon Jun 23 2025 Koichiro Iwao <meta@almalinux.org> - 6.12.25-20250428.v8.2
- Reintroduce initramfs for XFS / LUKS
  https://github.com/AlmaLinux/raspberry-pi/issues/65
  https://github.com/AlmaLinux/raspberry-pi/issues/86

* Mon May 26 2025 Koichiro Iwao <meta@almalinux.org> - 6.12.25-20250428.v8.1
- Update kernel to v6.12.25 stable_20250428
- Update firmware to 1.20250430
- Regenerate patches
- Use the consistent directory under /usr/share with the package name
- Enable EROFS bootc container (contributed by Kevin Fox)
- Fixes to enable bootc (contributed by Kevin Fox)

* Mon Jan 27 2025 Koichiro Iwao <meta@almalinux.org> - 6.12.1-20241206.v8.2
- Add pseudo subpackages for kernel modules to resolve dependency issue
- The main kernel package now provides kernel-core
- Convert license to SPDX expression
- Remove dracut as initramfs is not needed (mentioned in 4.4.21-2)

* Wed Dec 25 2024 Koichiro Iwao <meta@almalinux.org> - 6.12.1-20241206.v8.1
- Update kernel to v6.12.1 rpi-6.12.y_20241206_2
- Update firmware to 1.20241126

* Tue Nov 12 2024 Koichiro Iwao <meta@almalinux.org> - 6.12.0-20241111.v8.1
- Update kernel to v6.12.0-rc7 20241110 bf70ebd2

* Tue Nov 12 2024 Koichiro Iwao <meta@almalinux.org> - 6.11.7-20241110.v8.1
- Update kernel to v6.11.7 20241110 efda653d

* Fri Nov 08 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.51-20241008.v8.2
- Fix build for AL10 Kitten

* Mon Oct 21 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.51-20241008.v8.1
- Update kernel to version v6.6.51 stable_20241008
- Update firmware to 1.20241008

* Thu Sep 05 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.31-20240529.v8.4
- Add kernel-headers subpackage

* Fri Aug 30 2024 Andrew Lukoshko <alukoshko@almalinux.org> - 6.6.31-20240529.v8.3
- Fix kernel-tools dependencies

* Thu Jun 20 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.31-20240529.v8.2
- Add kernel-tools to optimize CPU clock (cpupower.service)

* Mon Jun 10 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.31-20240529.v8.1
- Update to v6.6.31 stable_20240529

* Tue Jun 04 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.28-20240423.v8.2
- Add installonlypkg(kernel) to kernel and -devel subpackages
  Resolves: https://github.com/AlmaLinux/raspberry-pi/issues/39
  See also: https://src.fedoraproject.org/rpms/kernel/c/aba3940

* Thu May 30 2024 Koichiro Iwao <meta@almalinux.org> - 6.6.28-20240423.v8.1
- Update to version v6.6.28
- Support both Raspberry Pi 4 and 5
- Refine package based on Linux for Raspberry Pi (raspberrypi/linux)
- Generate gzip compressed kernel image
- Drop armv7hl support
- Drop EL7 support

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
