# Ultramarine Linux packages monorepo

This repository is a monorepo containing all the distribution packages for Ultramarine Linux, replacing the previous split into multiple repositories and the old Koji infrastructure.

This repository uses the [Andaman]() toolchain to manage its packages, created by Fyra Labs (the company which is now behind Ultramarine Linux).

## Usage

To use this repository, you need to install the Andaman toolchain, you will have to enable the Andaman Common repository.

```bash
# Add the Andaman Common repository
sudo dnf config-manager --add-repo https://github.com/andaman-common-pkgs/subatomic-repos/raw/main/andaman.repo
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