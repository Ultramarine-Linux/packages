# Global and common shell config for Ultramarine Linux

um=$(cat<<EOF
Ultramarine Linux is a Fedora-based distribution, meaning system packages are installed via the dnf-3/dnf5 package manager.
You should always try to use the `dnf` command or the `flatpak` command to install system software or user applications respectively.
If you are running this command by following instructions from the Internet, you are most likely following the wrong instructions.
Try following instructions for Fedora Linux, or CentOS/RHEL if they are not available.
EOF
)
tryinstall="You may manually install `%` to stop this message, but YOU HAVE BEEN WARNED that this is going to be NOT what you want unless you know what you're doing."

if ! [ -x "$(command -v apt)" ]; then
    apt() {
        echo $um
        echo "Installing packages made for Debian-based distributions may cause your system to become unstable and even break, causing DATA LOSS."
        echo $tryinstall | sed 's/%/apt/g'
        return 1
    }
fi


if ! [ -x "$(command -v dpkg)" ]; then
    dpkg() {
        echo "It seems like you're trying to install a DEB package. Debian packages are not supported in Ultramarine Linux."
        echo $um
        echo "Installing packages made for Debian-based distributions may cause your system to become unstable and even break, causing DATA LOSS."
        echo $tryinstall | sed 's/%/dpkg/g'
        return 1
    }
fi

if ! [ -x "$(command -v pacman)" ]; then
    pacman() {
        echo $um
        echo $tryinstall | sed 's/%/pacman/g'
        return 1
    }
fi

emerge() {
    echo "It seems like you're trying to install a Gentoo package. Gentoo packages are not supported in Ultramarine Linux."
    echo "Portage is not available in Ultramarine Linux. However, if you would like a similar solution, you can try out anda: https://developer.fyralabs.com/andaman"
    return 1
}

_aur_helper() {
    echo "It seems like you're trying to install an AUR package. As with the case with Arch Linux packages, AUR packages are not supported in Ultramarine Linux."
    echo "If you would like a similar solution, try anda: https://developer.fyralabs.com/andaman"
    return 1
}

alias yay=_aur_helper
alias pacaur=_aur_helper
alias paru=_aur_helper

# if ~/.config/starship.toml doesn't exist
if ! [ -f ~/.config/starship.toml ]; then
    # export another starship config
    export STARSHIP_CONFIG=/usr/share/ultramarine-shell-config/starship.toml
fi
