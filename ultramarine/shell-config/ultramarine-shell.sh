# Global and common shell config for Ultramarine Linux

# if apt is not installed
if ! [ -x "$(command -v apt)" ]; then
    apt() {
        # print arguments
        echo "Ultramarine Linux uses the DNF package manager. If you're running this command by following instructions from the internet, you are probably following the wrong instructions."
        echo "Try following the instructions for Fedora Linux, or CentOS/RHEL if they're not available."
        echo "If you want stop this message from showing, manually install apt by running \"sudo dnf install apt\"."
        return 1
    }
fi


if ! [ -x "$(command -v dpkg)" ]; then
    dpkg() {
        # print arguments
        echo "It seems like you're trying to install a DEB package. Debian packages are not supported in Ultramarine Linux."
        echo "While it may be possible to actually install a DEB package in Ultramarine Linux, you should always try to install RPMs (or Flatpaks) whenever possible."
        echo "Installing DEB packages on Ultramarine Linux may cause your system to become unstable, and may even break your system, causing DATA LOSS."
        echo "If you want stop this message from showing and you know what you're doing, manually install dpkg by running \"sudo dnf install dpkg\"."
        return 1
    }
fi

# pacman
if ! [ -x "$(command -v pacman)" ]; then
    pacman() {
        # print arguments
        echo "Ultramarine Linux is a Fedora-based distribution, which means Ultramarine uses the DNF package manager. Ultramarine Linux is *not* an Arch-based distribution."
        echo "Please use dnf instead of pacman."
        echo "If you still would like to use pacman, install pacman manually."
        echo "WARNING: pacman is *not* supported by Ultramarine Linux, and using pacman may result in unexpected behavior. YOU HAVE BEEN WARNED."
        return 1
    }
fi

# emerge
emerge(){
    # print arguments
    echo "It seems like you're trying to install a Gentoo package. Gentoo packages are not supported in Ultramarine Linux."
    echo "Portage is not available in Ultramarine Linux. However, if you would like a similar solution, you can try out umpkg https://github.com/Ultramarine-Linux/umpkg"
    return 1
}

# AUR helpers
_aur_helper() {
    # print arguments
    echo "It seems like you're trying to install an AUR package. As with the case with Arch Linux packages, AUR packages are not supported in Ultramarine Linux."
    echo "If you would like a similar solution, try umpkg https://github.com/Ultramarine-Linux/umpkg"
    return 1
}

alias yay=_aur_helper
alias pacaur=_aur_helper
alias paru=_aur_helper

alias ls=exa

export PAGER=most

# if ~/.config/starship.toml doesn't exist
if ! [ -f ~/.config/starship.toml ]; then
    # export another starship config
    export STARSHIP_CONFIG=/usr/share/ultramarine-shell-config/starship.toml
fi