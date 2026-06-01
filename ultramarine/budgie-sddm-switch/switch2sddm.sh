#!/usr/bin/env bash

set -euo pipefail

CHECKFILE="/etc/sddm-switched"

if [[ -f "$CHECKFILE" ]]; then
    echo "You're already on SDDM, if you're still getting the notification, get support or file an issue."
    read -p "Press Enter to open Community page on the Wiki, or Ctrl+C to exit" && xdg-open "https://wiki.ultramarine-linux.org/en/community/community"
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
    read -p "Press Enter to open Community page on the Wiki, or Ctrl+C to exit" && xdg-open "https://wiki.ultramarine-linux.org/en/community/community"
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
echo "Your device needs to restart"
notify-send --wait \
    --urgency=critical \
    --app-icon=ultramarine \
    --app-name="Ultramarine System" \
    "Switch Complete" \
    "Save your work and return to the terminal to restart your device"
read -p "Save your work and press enter when you're ready to reboot" && pkexec systemctl soft-reboot
# we're gonna test this with a soft reboot
