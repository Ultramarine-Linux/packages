#!/bin/bash

# The OOBE setup script for Ultramarine WSL. This file is mainly based on:
# https://src.fedoraproject.org/rpms/wsl-setup/blob/rawhide/f/wsl-oobe.sh
# but, in the future, I think we could do some cooler stuff.
# Ideas/TODO:
# - Using gum for interactive prompts
# - Preset selection via um cli
# - Hit Plausible

set -ueo pipefail

DEFAULT_USER_ID=1000

echo 'Please create a default user account. The username does not need to match your Windows username.'
echo 'For more information visit: https://aka.ms/wslusers'

if getent passwd $DEFAULT_USER_ID > /dev/null ; then
  echo 'User account already exists, skipping creation'
  exit 0
fi

# Prompt from the username
read -r -p 'Enter new UNIX username: ' username

# Create the user
/usr/sbin/useradd -m -G wheel --uid $DEFAULT_USER_ID "$username"

cat > /etc/sudoers.d/wsluser << EOF
# Ensure the WSL initial user can use sudo without a password.
#
# Since the user is in the wheel group, this file can be removed
# if you wish to require a password for sudo. Be sure to set a
# user password before doing so with 'sudo passwd $username'!
$username ALL=(ALL) NOPASSWD: ALL
EOF

# Set the default user; necessary when this script is manually run in versions
# of WSL prior to 2.4.
cat >> /etc/wsl.conf << EOF

[user]
default = "$username"
EOF

echo 'Your user has been created, is included in the wheel group, and can use sudo without a password.'
echo "To set a password for your user, run 'sudo passwd $username'"
