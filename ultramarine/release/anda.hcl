project "pkg" {
        arches = ["x86_64"]
    rpm {
        spec = "ultramarine-release.spec"
        sources = "."
    }
    labels {
      updbranch = 1
    }
}
