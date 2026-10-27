rpm.version(gh("Ultramarine-Linux/server-oobe"));
if rpm.changed() {
    rpm.global("taidan_commit", gh_commit("Ultramarine-Linux/taidan"));
    // rpm.global("taidan_tag", gh_tag("Ultramarine-Linux/taidan"));
    // switch to tag once server-oobe feature is in tdnx there
}
