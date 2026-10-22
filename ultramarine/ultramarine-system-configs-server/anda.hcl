project "pkg" {
    rpm {
        spec = "ultramarine-system-configs-server.spec"
    }
    labels {
      updbranch = 1
      arches = ["x86_64"]
    }
}
