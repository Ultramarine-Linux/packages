project pkg {
    arches = ["aarch64"]
    rpm {
        spec = "ultramarine-server-dashboard.spec"
        sources = "."
    }
}
