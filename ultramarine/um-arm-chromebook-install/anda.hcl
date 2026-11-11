project "pkg" {
  arches = ["aarch64"]
    rpm {
        spec = "um-arm-chromebook-install.spec"
    }
}
