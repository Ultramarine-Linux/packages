project "pkg" {
    rpm {
        spec = "flatpak-selinux-fix.spec"
        sources =  "."
    }
}