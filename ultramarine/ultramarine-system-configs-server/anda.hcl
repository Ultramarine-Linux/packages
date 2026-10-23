project "pkg" {
   	  arches = ["x86_64"]
    rpm {
        spec = "ultramarine-system-configs-server.spec"
    }
    labels {
      updbranch = 1
    }
}
