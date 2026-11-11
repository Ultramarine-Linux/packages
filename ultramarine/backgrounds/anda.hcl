project "pkg" {
    arches = ["aarch64"]
    rpm {
        spec = "ultramarine-backgrounds.spec"
        sources =  "."
    }
}
