#!/usr/bin/env bash

CHECKFILE="/etc/sddm-switched"

[[ -f "$CHECKFILE" ]] && exit 0

# If SDDM is already the default DM, mark done and exit silently
DM_LINK=$(readlink -f /etc/systemd/system/display-manager.service 2>/dev/null || true)
DM=$(basename "$DM_LINK" .service)

if [[ "$DM" == "sddm" ]]; then
    pkexec touch "$CHECKFILE"
    exit 0
fi

(action=$(notify-send --wait \
    --urgency=critical \
    --app-icon=ultramarine \
    --app-name="Ultramarine System" \
    --action="default=Open Wiki" \
    "Upgrade Display Manager" \
    "Ultramarine Budgie is switching to the SDDM display manager, if you don't switch, you won't be able to update to the next release. Click this notification to open the wiki.") \
    && [[ "$action" == "default" ]] \
    && xdg-open "https://wiki.ultramarine-linux.org/en/release/budgie-sddm") &
