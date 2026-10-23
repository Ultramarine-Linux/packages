let tag = gh("Ultramarine-Linux/taidan");
rpm.version(tag);
// taidan_proc_macros is a submodule; GitHub release tarballs omit it, so the
// spec fetches it separately at the commit this tag records.
rpm.global("proc_macros_commit", get(`https://api.github.com/repos/Ultramarine-Linux/taidan/contents/taidan_proc_macros?ref=${tag}`).json().sha);
