project "pkg" {
    arches = ["aarch64"]
    rpm {
        spec = "ultramarine-logos.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
