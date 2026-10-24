project "pkg" {
        arches = ["x86_64"]
    rpm {
        spec = "ultramarine-system-configs.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
