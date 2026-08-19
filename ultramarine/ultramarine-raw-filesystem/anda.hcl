project "pkg" {
    rpm {
        spec = "ultramarine-raw-filesystem.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
