project "pkg" {
    arches = ["x86_64"]
    rpm {
        spec = "ultramarine-wsl-filesystem.spec"
    }
    labels {
      updbranch = 1
    }
}
