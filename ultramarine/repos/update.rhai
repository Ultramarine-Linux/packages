import "andax/bump_extras.rhai" as bump;

rpm.global("_dist_version", bump::as_bodhi_ver(labels.branch));

if rpm.changed() {
  rpm.release();
}
