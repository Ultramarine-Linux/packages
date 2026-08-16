project "pkg" {
    rpm {
        spec = "ultramarine-logos.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
