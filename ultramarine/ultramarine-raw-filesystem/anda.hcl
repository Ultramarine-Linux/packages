project "pkg" {
    arches = ["aarch64"]
    rpm {
        spec = "ultramarine-raw-filesystem.spec"
        sources =  "."
    }
}
