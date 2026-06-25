project "pkg" {
        arches = ["x86_64"]
    rpm {
        spec = "kde-settings.spec"
        sources =  "."
    }
}
