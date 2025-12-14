# This updates some of the vendored files from the upstream release package repository.
# Right now this doesn't do all of the files, so please check the files manually.
# Additionally, this will overwrite our changes, so check those too. Ideally, we shouldn't change upstream files if possible.

VERSION="43"

download_file() {
    curl -o "$1" "https://src.fedoraproject.org/rpms/fedora-release/raw/f$VERSION/f/$2"
}

download_file 80-workstation.preset 80-workstation.preset
download_file 81-atomic-desktop.preset 81-atomic-desktop.preset
download_file 81-desktop.preset 81-desktop.preset
download_file 85-display-manager.preset 85-display-manager.preset
download_file 90-default-user.preset 90-default-user.preset
download_file 90-default.preset 90-default.preset
download_file 99-default-disable.preset 99-default-disable.preset

download_file longer-default-shutdown-timeout.conf longer-default-shutdown-timeout.conf

download_file org.projectatomic.rpmostree1.rules org.projectatomic.rpmostree1.rules
