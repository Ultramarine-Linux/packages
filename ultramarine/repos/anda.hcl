project "pkg" {
    rpm {
        spec = "repos.spec"
        sources =  "."
    }
    labels {
      updbranch = 1
    }
}
