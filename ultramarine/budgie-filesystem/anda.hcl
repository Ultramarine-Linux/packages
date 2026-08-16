project "pkg" {
    rpm {
        spec = "ultramarine-budgie-filesystem.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
