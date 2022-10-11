%define _disable_source_fetch 0

Name:          ultramarine-logos
%define        _alt_name fedora-logos
Summary:       Icons and pictures related to Ultramarine Linux
Version:       37
%define        _release 2%{?dist}
Release:       2%{?dist}
URL:           https://github.com/Ultramarine-Linux/logos-src
Source0:       https://github.com/Ultramarine-Linux/logos-src/archive/refs/heads/lapis.zip
Source1:       distributor-logo-ultramarine-flat.svg
License:       Licensed only for approved usage, see COPYING for details.
Provides:      redhat-logos = %{version}-%{_release}
Provides:      gnome-logos = %{version}-%{_release}
Provides:      system-logos = %{version}-%{_release}
Provides:      %{_alt_name} = %{version}-%{_release}
BuildArch:     noarch
BuildRequires: hardlink
Requires:      ultramarine-release = %{version}

%if ! 0%{?eln}
# For _kde4_* macros:
BuildRequires:	kde-filesystem
%endif
 
%description
See the included COPYING file for full information on copying and
redistribution of this package and its contents.

%package httpd
Summary: Assets used by httpd that are related to Ultramarine Linux
Provides:	system-logos-httpd = %{version}-%{_release}
Provides: %{_alt_name}-httpd = %{version}-%{_release}
BuildArch:	noarch
Recommends:	julietaula-montserrat-base-web-fonts
Provides:	system-logos(httpd-logo-ng)
 
%description httpd
Assets used by httpd that are related to Ultramarine Linux
 
%package classic
Summary:	Compatibility package for %{_alt_name}
Provides: %{_alt_name}-classic = %{version}-%{_release}
BuildArch:	noarch
 
%description classic
Compatibility package for %{_alt_name}

%package -n whitesur-icon-theme-ultramarine
Summary: Ultramarine Linux assets to complement the whitesur-icon-theme package
License: GPLv3
Requires: whitesur-icon-theme
BuildArch: noarch

%description -n whitesur-icon-theme-ultramarine
Ultramarine Linux assets to complement the whitesur-icon-theme package

%prep
%setup -qn logos-src-lapis
 
%build
 
%install
# Bootloader related files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
# To regenerate this file, see the bootloader/fedora.icns entry in the Makefile
install -p -m 644 bootloader/fedora.icns $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
 
# Classic variant
install -p -m 644 bootloader/fedora_classic.icns $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
 
# To regenerate these files, run:
# pngtopnm foo.png | ppmtoapplevol > foo.vol
install -p -m 644 bootloader/fedora.vol bootloader/fedora-media.vol $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
 
# General purpose Fedora logos
for i in pixmaps/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/pixmaps
done
 
# Anaconda release notes (that contain Fedora logos)
# Pretty sure these are legacy/unused now (2021).
for i in rnotes/* ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/anaconda/pixmaps/$i
  install -p -m 644 $i/* $RPM_BUILD_ROOT%{_datadir}/anaconda/pixmaps/$i
done
 
# OLD LOGO ONLY
# The Plymouth charge theme (uses the Fedora logo)
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
for i in plymouth/charge/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
done
 
# The Plymoth spinner theme Fedora logo bits
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/spinner
install -p -m 644 pixmaps/fedora-gdm-logo.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/spinner/watermark.png
 
# Fedora logo icons
for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  pushd $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png icon-panel-menu.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon_classic.png icon-panel-menu_classic.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png gnome-main-menu.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon_classic.png gnome-main-menu_classic.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png kmenu.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon_classic.png kmenu_classic.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png start-here.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon_classic.png start-here_classic.png
  popd
  for i in icons/hicolor/$size/apps/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  done
done
 
for i in 16 22 24 32 36 48 96 256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places/start-here.png
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon_classic.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places/start-here_classic.png
%if ! 0%{?eln}
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/${i}x${i}/places/start-here-kde-fedora.png
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon_classic.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/${i}x${i}/places/start-here-kde-fedora_classic.png
%endif
done
 
%if ! 0%{?eln}
mkdir -p $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/
install -p -m 644 icons/hicolor/scalable/apps/org.fedoraproject.AnacondaInstaller.svg $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/
install -p -m 644 icons/hicolor/scalable/apps/org.fedoraproject.AnacondaInstaller_classic.svg $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/
%endif
 
# Fedora favicon
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
pushd $RPM_BUILD_ROOT%{_sysconfdir}
  ln -s %{_datadir}/icons/hicolor/16x16/apps/fedora-logo-icon.png favicon.png
  ln -s %{_datadir}/icons/hicolor/16x16/apps/fedora-logo-icon_classic.png favicon_classic.png
popd
 
# Fedora hicolor icons
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/xfce4_xicon1.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/xfce4_xicon1_classic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/fedora-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg
install -p -m 644 icons/hicolor/scalable/apps/fedora-logo-icon_classic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here_classic.svg
install -p -m 644 icons/hicolor/scalable/apps/org.fedoraproject.AnacondaInstaller.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/org.fedoraproject.AnacondaInstaller.svg
install -p -m 644 icons/hicolor/scalable/apps/org.fedoraproject.AnacondaInstaller_classic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/org.fedoraproject.AnacondaInstaller_classic.svg
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
pushd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
  ln -s ../apps/start-here.svg .
  ln -s ../apps/start-here_classic.svg .
popd
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps
install -p -m 644 icons/hicolor/symbolic/apps/org.fedoraproject.AnacondaInstaller-symbolic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps/
install -p -m 644 icons/hicolor/symbolic/apps/org.fedoraproject.AnacondaInstaller-symbolic_classic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps/
 
# Fedora logos for the clearlooks theme (icewm)
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/icewm_taskbar_logos_fedora.tar.gz $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora_logo.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/icewm_taskbar_logos_fedora_classic.tar.gz $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_classic.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora_classic.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora_logo_classic.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks/taskbar/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/icewm_taskbar_logos_fedora.tar.gz $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora_logo.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/icewm_taskbar_logos_fedora_classic.tar.gz $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_classic.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora_classic.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
install -p -m 644 icons/clearlooks/taskbar/linux_fedora_logo_classic.xpm $RPM_BUILD_ROOT%{_datadir}/icewm/themes/clearlooks-2px/taskbar/
 
# Fedora art in anaconda
# To regenerate the lss file, see anaconda/Makefile
mkdir -p %{buildroot}%{_datadir}/anaconda/boot
install -p -m 644 anaconda/splash.lss %{buildroot}%{_datadir}/anaconda/boot/
install -p -m 644 anaconda/syslinux-splash.png %{buildroot}%{_datadir}/anaconda/boot/
# note the filename change
install -p -m 644 anaconda/syslinux-vesa-splash.png %{buildroot}%{_datadir}/anaconda/boot/splash.png
mkdir -p %{buildroot}%{_datadir}/anaconda/pixmaps
install -p -m 644 anaconda/anaconda_header.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/anaconda_header_classic.png %{buildroot}%{_datadir}/anaconda/pixmaps/
# This had not been regenerated since Fedora 17. Clearly not used anymore.
# install -p -m 644 anaconda/progress_first.png %%{buildroot}%%{_datadir}/anaconda/pixmaps/
# install -p -m 644 anaconda/splash.png %%{buildroot}%%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/sidebar-logo.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/sidebar-logo_classic.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/sidebar-bg.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/topbar-bg.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/fedora.css %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/ultramarine.css %{buildroot}%{_datadir}/anaconda/pixmaps/

 
%if ! 0%{?eln}
# KDE Theme logos
# DO NOT REMOVE THIS ICON!!! We still support the Leonidas and Solar themes!
mkdir -p $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/
install -p -m 644 kde-splash/Leonidas-fedora.png $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png
install -p -m 644 kde-splash/Leonidas-fedora_classic.png $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo_classic.png
%endif
 
# SVG Fedora logos
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a fedora/*.svg $RPM_BUILD_ROOT%{_datadir}/%{name}
 
# HTTP files
cp -a css3 $RPM_BUILD_ROOT%{_datadir}/%{name}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fedora-testpage/
cp -a testpage/index.html $RPM_BUILD_ROOT%{_datadir}/fedora-testpage/
 
# The proper path should be unbranded, but because of history it's easier for
# this package to symlink the old path to the proper one. This avoids having
# to perform scriptlet trickery to handle upgrades from the directory to a
# symlink.
ln -s fedora-testpage $RPM_BUILD_ROOT%{_datadir}/testpage
 
# save some dup'd icons
# Except in /boot. Because some people think it is fun to use VFAT for /boot.
# hardlink is /usr/sbin/hardlink on Fedora <= 30 and /usr/bin/hardlink on F31+
hardlink -vv %{buildroot}/usr

# # # # # # # # # # # # # # # # #
# whitesur-icon-theme-ultramarine
mkdir -p %{buildroot}/%{_datadir}/icons/WhiteSur/apps/scalable/
cp -v %{SOURCE1} %{buildroot}/%{_datadir}/icons/WhiteSur/apps/scalable/distributor-logo-ultramarine.svg
mkdir -p %{buildroot}/%{_datadir}/icons/WhiteSur-dark/apps/scalable/
cp -v %{SOURCE1} %{buildroot}/%{_datadir}/icons/WhiteSur-dark/apps/scalable/distributor-logo-ultramarine.svg
# # # # # # # # # # # # # # # # #

%post -n whitesur-icon-theme-ultramarine
pushd %{_datadir}/icons/WhiteSur
ln -nvfs apps/scalable/distributor-logo-ultramarine.svg launcher-icon.svg
sha512sum launcher-icon.svg > whitesur-icon-theme-ultramarine.SHA512_CHECKSUM
popd

pushd %{_datadir}/icons/WhiteSur-dark
ln -nvfs apps/scalable/distributor-logo-ultramarine.svg launcher-icon.svg
sha512sum launcher-icon.svg > whitesur-icon-theme-ultramarine.SHA512_CHECKSUM
popd

%postun -n whitesur-icon-theme-ultramarine
pushd %{_datadir}/icons/WhiteSur
sha512sum -c whitesur-icon-theme-ultramarine.SHA512_CHECKSUM
if [ ${?} == 0 ]; then
  rm -v launcher-icon.svg
fi
popd

pushd %{_datadir}/icons/WhiteSur-dark
sha512sum -c whitesur-icon-theme-ultramarine.SHA512_CHECKSUM
if [ ${?} == 0 ]; then
  rm -v launcher-icon.svg
fi
popd

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/plymouth/themes/spinner/
%if ! 0%{?eln}
# No one else before us owns this, so we shall.
%dir %{_kde4_sharedir}/kde4/
%exclude %{_kde4_iconsdir}/oxygen/*/places/start-here-kde-fedora_classic.png
%exclude %{_kde4_iconsdir}/oxygen/scalable/apps/org.fedoraproject.AnacondaInstaller_classic.svg
%{_kde4_iconsdir}/oxygen/
# DO NOT REMOVE THIS ICON!!! We still support the Leonidas and Solar themes!
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png
%endif
# in -classic
%exclude %{_datadir}/pixmaps/bootloader/fedora_classic.icns
%exclude %{_datadir}/pixmaps/fedora-gdm-logo_classic.png
%exclude %{_datadir}/pixmaps/fedora-logo_classic.png
%exclude %{_datadir}/pixmaps/fedora-logo-small_classic.png
%exclude %{_datadir}/pixmaps/fedora-logo-sprite_classic.png
%exclude %{_datadir}/pixmaps/fedora-logo-sprite_classic.svg
%exclude %{_datadir}/pixmaps/fedora_whitelogo_classic.svg
%exclude %{_datadir}/pixmaps/poweredby_classic.png
%exclude %{_datadir}/pixmaps/system-logo-white_classic.png
%{_datadir}/pixmaps/*
# This lives in the http subpackage
%exclude %{_datadir}/pixmaps/poweredby.png
%exclude %{_datadir}/anaconda/pixmaps/*_classic*
%exclude %{_datadir}/anaconda/pixmaps/*/*_classic*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/anaconda/boot/splash.lss
%{_datadir}/anaconda/boot/syslinux-splash.png
%{_datadir}/anaconda/boot/splash.png
%exclude %{_datadir}/icewm/themes/clearlooks/taskbar/*_classic*
%exclude %{_datadir}/icewm/themes/clearlooks-2px/taskbar/*_classic*
%{_datadir}/icewm/themes/clearlooks/taskbar/*
%{_datadir}/icewm/themes/clearlooks-2px/taskbar/*
%exclude %{_datadir}/icons/hicolor/*/apps/*_classic*
%exclude %{_datadir}/icons/hicolor/*/places/*_classic*
%exclude %{_datadir}/icons/Bluecurve/*/apps/*_classic*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/places/*
%{_datadir}/icons/Bluecurve/*/apps/*
%exclude %{_datadir}/%{name}/*_classic*
# old logo
%exclude %{_datadir}/%{name}/css3
%{_datadir}/%{name}/
# we multi-own these directories, so as not to require the packages that
# provide them, thereby dragging in excess dependencies.
%dir %{_datadir}/icons/Bluecurve/
%dir %{_datadir}/icons/Bluecurve/16x16/
%dir %{_datadir}/icons/Bluecurve/16x16/apps/
%dir %{_datadir}/icons/Bluecurve/22x22/
%dir %{_datadir}/icons/Bluecurve/22x22/apps/
%dir %{_datadir}/icons/Bluecurve/24x24/
%dir %{_datadir}/icons/Bluecurve/24x24/apps/
%dir %{_datadir}/icons/Bluecurve/32x32/
%dir %{_datadir}/icons/Bluecurve/32x32/apps/
%dir %{_datadir}/icons/Bluecurve/36x36/
%dir %{_datadir}/icons/Bluecurve/36x36/apps/
%dir %{_datadir}/icons/Bluecurve/48x48/
%dir %{_datadir}/icons/Bluecurve/48x48/apps/
%dir %{_datadir}/icons/Bluecurve/96x96/
%dir %{_datadir}/icons/Bluecurve/96x96/apps/
%dir %{_datadir}/icons/Bluecurve/256x256/
%dir %{_datadir}/icons/Bluecurve/256x256/apps/
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/16x16/
%dir %{_datadir}/icons/hicolor/16x16/apps/
%dir %{_datadir}/icons/hicolor/16x16/places/
%dir %{_datadir}/icons/hicolor/22x22/
%dir %{_datadir}/icons/hicolor/22x22/apps/
%dir %{_datadir}/icons/hicolor/22x22/places/
%dir %{_datadir}/icons/hicolor/24x24/
%dir %{_datadir}/icons/hicolor/24x24/apps/
%dir %{_datadir}/icons/hicolor/24x24/places/
%dir %{_datadir}/icons/hicolor/32x32/
%dir %{_datadir}/icons/hicolor/32x32/apps/
%dir %{_datadir}/icons/hicolor/32x32/places/
%dir %{_datadir}/icons/hicolor/36x36/
%dir %{_datadir}/icons/hicolor/36x36/apps/
%dir %{_datadir}/icons/hicolor/36x36/places/
%dir %{_datadir}/icons/hicolor/48x48/
%dir %{_datadir}/icons/hicolor/48x48/apps/
%dir %{_datadir}/icons/hicolor/48x48/places/
%dir %{_datadir}/icons/hicolor/96x96/
%dir %{_datadir}/icons/hicolor/96x96/apps/
%dir %{_datadir}/icons/hicolor/96x96/places/
%dir %{_datadir}/icons/hicolor/256x256/
%dir %{_datadir}/icons/hicolor/256x256/apps/
%dir %{_datadir}/icons/hicolor/256x256/places/
%dir %{_datadir}/icons/hicolor/scalable/
%dir %{_datadir}/icons/hicolor/scalable/apps/
%dir %{_datadir}/icons/hicolor/scalable/places/
%dir %{_datadir}/anaconda
%dir %{_datadir}/anaconda/boot/
%dir %{_datadir}/anaconda/pixmaps/
%dir %{_datadir}/plymouth/
%dir %{_datadir}/plymouth/themes/
%if ! 0%{?eln}
# DO NOT REMOVE THESE DIRS!!! We still support the Leonidas and Solar themes!
%dir %{_kde4_appsdir}
%dir %{_kde4_appsdir}/ksplash
%dir %{_kde4_appsdir}/ksplash/Themes/
%dir %{_kde4_appsdir}/ksplash/Themes/Leonidas/
%dir %{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536
%endif
 
%files httpd
%license COPYING
%dir %{_datadir}/fedora-testpage
%{_datadir}/testpage
%{_datadir}/fedora-testpage/index.html
%{_datadir}/pixmaps/poweredby.png
 
# EVERYTHING IN CLASSIC USES OLD LOGO
%files classic
%license COPYING
%if ! 0%{?eln}
%{_kde4_iconsdir}/oxygen/*/places/start-here-kde-fedora_classic.png
%{_kde4_iconsdir}/oxygen/scalable/apps/org.fedoraproject.AnacondaInstaller_classic.svg
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo_classic.png
%endif
%{_sysconfdir}/favicon_classic.png
%{_datadir}/anaconda/pixmaps/*_classic*
%{_datadir}/icewm/themes/clearlooks/taskbar/*_classic*
%{_datadir}/icewm/themes/clearlooks-2px/taskbar/*_classic*
%{_datadir}/icons/hicolor/*/apps/*_classic*
%{_datadir}/icons/hicolor/*/places/*_classic*
%{_datadir}/icons/Bluecurve/*/apps/*_classic*
%{_datadir}/%{name}/*_classic*
%{_datadir}/%{name}/css3/
%{_datadir}/pixmaps/bootloader/fedora_classic.icns
%{_datadir}/pixmaps/fedora-gdm-logo_classic.png
%{_datadir}/pixmaps/fedora-logo_classic.png
%{_datadir}/pixmaps/fedora-logo-small_classic.png
%{_datadir}/pixmaps/fedora-logo-sprite_classic.png
%{_datadir}/pixmaps/fedora-logo-sprite_classic.svg
%{_datadir}/pixmaps/fedora_whitelogo_classic.svg
%{_datadir}/pixmaps/poweredby_classic.png
%{_datadir}/pixmaps/system-logo-white_classic.png
%{_datadir}/plymouth/themes/charge/

%files -n whitesur-icon-theme-ultramarine
%{_datadir}/icons/WhiteSur/apps/scalable/distributor-logo-ultramarine.svg
%{_datadir}/icons/WhiteSur-dark/apps/scalable/distributor-logo-ultramarine.svg