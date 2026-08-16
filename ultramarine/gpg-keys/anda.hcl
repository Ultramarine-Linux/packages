project "pkg" {
    arches = ["x86_64"]
    rpm {
        spec = "ultramarine-gpg-keys.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
