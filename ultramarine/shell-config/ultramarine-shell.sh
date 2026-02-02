# Global and common shell config for Ultramarine Linux

um=$(cat<<EOF
Try searching for this package with dnf search or in your edition's app store.
EOF
)
tryinstall="Don't install other package managers unless you really know what you're doing."

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

if ! [ -x "$(command -v snap)" ]; then
    snap() {
        echo "Ultramarine comes with Flathub and Terra, which should include most of the software you're looking for."
        echo $um
        echo "If the software you need is only availible as a Snap, you can install it with `sudo dnf install snapd`"
        return 1
    }
fi

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
