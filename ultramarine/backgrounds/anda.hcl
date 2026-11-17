project "pkg" {
    rpm {
        spec = "ultramarine-backgrounds.spec"
        sources =  "."
    }
    labels {
        oglyad_ignore = "drift, stale"
    }
}
