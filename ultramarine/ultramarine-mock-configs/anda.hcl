project "pkg" {
    arches = ["x86_64"]
    rpm {
        spec = "ultramarine-mock-configs.spec"
        sources = "."
    }
}
