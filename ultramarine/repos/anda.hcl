project "pkg" {
    arches = ["aarch64"]
    rpm {
        spec = "repos.spec"
        sources =  "."
    }
}
