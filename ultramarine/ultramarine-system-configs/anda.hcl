project "pkg" {
    rpm {
        spec = "ultramarine-system-configs.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
