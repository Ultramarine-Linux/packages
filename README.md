# Ultramarine Linux packages monorepo

This repository is a monorepo containing all the distribution packages for Ultramarine Linux.

This repository uses the [Andaman](https://github.com/FyraLabs/anda) toolchain to manage its packages, created by Fyra Labs (the company behind Ultramarine Linux).

## Usage

To use this repository, you need to install the Andaman toolchain, you will have to enable the Terra repository.

```bash
# Install Terra
sudo dnf install --repofrompath 'terra,https://repos.fyralabs.com/terra$releasever' --setopt='terra.gpgkey=https://repos.fyralabs.com/terra$releasever/key.asc' terra-release
# Install the Andaman toolchain
sudo dnf install anda
```

You can also install Andaman as a crates on crates.io, but you will have to install the dependencies manually.

```bash
# install runtime dependencies
sudo dnf install mock rpmdevtools rpm-build createrepo_c
# Add yourself to the mock group
sudo usermod -a -G mock $USER
# Install andaman using cargo
cargo install anda
```

Once Andaman is installed, you can clone this repository and build the packages.

To list all current packages in this repository, you can use the `list` command.

```bash
anda list
```

# Notes

- From Ultramarine 40+, on each major release, an admin should upload the `terra-release` package from Terra into the Ultramarine Linux repo. This is required since `ultramarine-repos` no longer provides the terra.repo file, but rather requires on `terra-release`. If it's missing, this may break installs where the user doesn't have the Terra repo installed (out of band), additionally, there was a time in 40's cycle where the `ultramarine-repos` only recommended the `terra-release` package, which might have caused it to not be installed on some systems during the 39 to 40 upgrade.
    - There's no need to update the `terra-release` package once it's uploaded to the UM repo. Once the Terra repo is discovered, the user will get updates for the package from Terra.
- When preparing a new major release, make sure to update files pulled from upstream, such as systemd preset config in the release package or cetain kde-settings files.
