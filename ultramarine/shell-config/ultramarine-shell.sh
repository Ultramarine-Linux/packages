# Global and common shell config for Ultramarine Linux

um=$(cat<<EOF
"Try searching for this package with `dnf search` or in your edition's app store."
EOF
)
tryinstall="You can install '%' to hide this message. This probably isn't what you want to do and may have unintended consequences. We aren't responsible for any breakage, thermonuclear war, death of a pet, etc that happens from here. You have been warned."

if ! [ -x "$(command -v apt)" ]; then
    apt() {
        echo "Debian packages are not supported in Ultramarine."
        echo $um
        echo $tryinstall | sed 's/%/apt/g'
        return 1
    }
fi


if ! [ -x "$(command -v dpkg)" ]; then
    dpkg() {
        echo "Debian packages are not supported in Ultramarine."
        echo $um
        echo $tryinstall | sed 's/%/dpkg/g'
        return 1
    }
fi

if ! [ -x "$(command -v pacman)" ]; then
    pacman() {
        echo "Arch packages are not supported on Ultramarine."
        echo $um
        echo $tryinstall | sed 's/%/pacman/g'
        return 1
    }
fi

if ! [ -x "$(command -v snap)" ]; then
    snap() {
        echo "Ultramarine comes with Flathub and Terra, which should include most of the software you're looking for."
        echo $um
        echo "If the software you need is only availible as a Snap, you can install it with `sudo dnf install snapd`"
        return 1
    }
fi

emerge() {
    echo "Gentoo packages are not supported on Ultramarine."
    echo $um
    return 1
}

_aur_helper() {
    echo "AUR packages are not supported on Ultramarine."
    echo $um
    return 1
}

alias yay=_aur_helper
alias pacaur=_aur_helper
alias paru=_aur_helper

if ! [ -x "$(command -v neofetch)" ]; then
    neofetch() {
        echo 'Neofetch is no longer maintained.'
        echo 'Ultramarine comes with fastfetch, give it a try!'
        echo 'You can disable this message by installing hyfetch-neofetch.'
        return 1
    }
fi

# if ~/.config/starship.toml doesn't exist
if ! [ -f ~/.config/starship.toml ]; then
    # export another starship config
    export STARSHIP_CONFIG=/usr/share/ultramarine-shell-config/starship.toml
else
    unset STARSHIP_CONFIG
fi
