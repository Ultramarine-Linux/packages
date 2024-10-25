%global	_firmwarepath	/usr/lib/firmware
%global	fn_commit	223ccf3a3ddb11b3ea829749fbbba4d65b380897
%global	fn_shortcommit	%(c=%{commit}; echo ${c:0:7})
%global	bz_commit	d9d4741caba7314d6500f588b1eaa5ab387a4ff5
%global	bz_shortcommit	%(c=%{bz_commit}; echo ${c:0:7})
%global	fn_srcdir	firmware-nonfree-%{fn_commit}
%global	bz_srcdir	bluez-firmware-%{bz_commit}

Name:		linux-firmware-rpi
Version:	20240528
Release:	5%{?dist}
Summary:	Supplemental firmware used by Linux kernel for some Raspberry Pi models
BuildArch:	noarch
ExclusiveArch:	aarch64

# LICENSE file installed by linux-firmware package also covers these suppremental firmware
# /usr/share/licenses/linux-firmware/LICENCE.broadcom_bcm43xx
License:	Redistributable, no modification permitted
URL:		https://github.com/RPi-Distro/firmware-nonfree

Source0:	https://github.com/RPi-Distro/firmware-nonfree/archive/%{fn_commit}/firmware-nonfree-%{fn_commit}.tar.gz
Source1:	https://github.com/RPi-Distro/bluez-firmware/archive/%{bz_commit}/bluez-firmware-%{bz_commit}.tar.gz

Requires:	linux-firmware

%description
This package is part of the Ultramarine Anywhere Initative. Provides suppremental firmware files not included in linux-firmware to enable radios on some Raspberry Pi models.

%prep
%setup -n %{fn_srcdir}
%setup -n %{fn_srcdir} -a 1

%build

%install
install -d %{buildroot}%{_firmwarepath}/brcm
install -c -m 644 debian/config/brcm80211/brcm/brcmfmac43455-sdio.txt %{buildroot}%{_firmwarepath}/brcm/
install -c -m 644 debian/config/brcm80211/brcm/brcmfmac43456-sdio.txt %{buildroot}%{_firmwarepath}/brcm/
install -c -m 644 debian/config/brcm80211/brcm/brcmfmac43456-sdio.bin %{buildroot}%{_firmwarepath}/brcm/
install -c -m 644 debian/config/brcm80211/brcm/brcmfmac43456-sdio.clm_blob %{buildroot}%{_firmwarepath}/brcm/
# Bluetooth for RPi Zero 2W
install -c -m 644 %{bz_srcdir}/debian/firmware/broadcom/BCM43430B0.hcd %{buildroot}%{_firmwarepath}/brcm/
# Bluetooth for RPi 3B+, 4, 5
install -c -m 644 %{bz_srcdir}/debian/firmware/broadcom/BCM43430A1.hcd %{buildroot}%{_firmwarepath}/brcm/
install -c -m 644 %{bz_srcdir}/debian/firmware/broadcom/BCM4345C0.hcd %{buildroot}%{_firmwarepath}/brcm/
# Bluetooth for RPi 400
install -c -m 644 %{bz_srcdir}/debian/firmware/broadcom/BCM4345C5.hcd %{buildroot}%{_firmwarepath}/brcm/
# Other firmware files installed by linux-firmware are compressed, so compress these as well
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/brcmfmac43455-sdio.txt
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/brcmfmac43456-sdio.bin
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/brcmfmac43456-sdio.clm_blob
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/brcmfmac43456-sdio.txt
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/BCM43430A1.hcd
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/BCM43430B0.hcd
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/BCM4345C0.hcd
xz -C crc32 %{buildroot}%{_firmwarepath}/brcm/BCM4345C5.hcd
# Create model-specific symlinks
# Raspberry Pi CM 4
ln -s brcmfmac43455-sdio.bin.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43455-sdio.raspberrypi,4-compute-module.bin.xz
ln -s brcmfmac43455-sdio.clm_blob.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43455-sdio.raspberrypi,4-compute-module.clm_blob.xz
# Raspberry Pi 400
ln -s brcmfmac43456-sdio.bin.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43456-sdio.raspberrypi,400.bin.xz
ln -s brcmfmac43456-sdio.clm_blob.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43456-sdio.raspberrypi,400.clm_blob.xz
ln -s brcmfmac43456-sdio.txt.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43456-sdio.raspberrypi,400.txt.xz
# Raspberry Pi 5
ln -s BCM4345C0.hcd.xz %{buildroot}%{_firmwarepath}/brcm/BCM4345C0.raspberrypi,5-model-b.hcd.xz
ln -s brcmfmac43455-sdio.bin.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43455-sdio.raspberrypi,5-model-b.bin.xz
ln -s brcmfmac43455-sdio.clm_blob.xz %{buildroot}%{_firmwarepath}/brcm/brcmfmac43455-sdio.raspberrypi,5-model-b.clm_blob.xz

%files
%{_firmwarepath}/brcm/*

%changelog
* Thu Oct 24 2024 Jaiden Riordan <jade@fyralabs.com>
- Port to Ultramarine

* Thu Jul 25 2024 Andrew Lukoshko <alukoshko@almalinux.org> - 20240528-5
- Update to not conflict with linux-firmware-20240603-143.1.el9_4

* Wed Jul 10 2024 Koichiro Iwao <meta@almalinux.org> - 20240528-4
- Fix wrong symlink for RPi CM4
- Set ExclusiveArch to aarch64

* Mon Jun 03 2024 Koichiro Iwao <meta@almalinux.org> - 20240528-3
-  Add symlink for RPi CM4

* Tue May 28 2024 Koichiro Iwao <meta@almalinux.org> - 20240528-2
- Fix symlink typo and add missing file

* Tue May 28 2024 Koichiro Iwao <meta@almalinux.org> - 20240528-1
- Update firmware-nonfree to 223ccf3
- Add symlink for RPi 5

* Fri Nov 17 2023 Koichiro Iwao <meta@almalinux.org> - 20231117-1
- Add firmware to support Bluetooth for RPi 3B+, Zero 2 W and 400

* Thu Apr 20 2023 Koichiro Iwao <koichiro.iwao@miraclelinux.com> - 20230420-1
- Initial creation