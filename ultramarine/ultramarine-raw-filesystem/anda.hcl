project "pkg" {
    arches = ["aarch64"]
    rpm {
        spec = "ultramarine-raw-filesystem.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
