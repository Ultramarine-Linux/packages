project "pkg" {
    arches = ["x86_64"]
    rpm {
        spec = "ultramarine-shell-config.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
