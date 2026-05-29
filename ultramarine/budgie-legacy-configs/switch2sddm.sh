#!/usr/bin/env bash

set -euo pipefail

CHECKFILE="/etc/sddm-switched"

if [[ -f "$CHECKFILE" ]]; then
    echo "You're already on SDDM, if you're still getting the notification get help on Discord."
    exit 0
fi

DM_LINK=$(readlink -f /etc/systemd/system/display-manager.service 2>/dev/null || true)
DM=$(basename "$DM_LINK" .service)

if [[ "$DM" == "sddm" ]]; then
    echo "SDDM is already the default display manager."
    pkexec touch "$CHECKFILE"
    exit 0
fi

if [[ "$DM" != "lightdm" ]]; then
    echo "You're not on lightdm, seeing '${DM:-unknown}'. If you know what you're doing stop here, otherwise get help on Discord." >&2
    echo "Aborting" >&2
    exit 1
fi

echo "Disable LightDM"
systemctl disable lightdm.service

echo "Enable SDDM"
systemctl enable sddm.service

echo "Disable Notification"
pkexec touch "$CHECKFILE"

echo ""
echo "All Done!"
echo "You need to reboot, save your work now, then reboot when you're ready"
read -p "Press enter to reboot"
