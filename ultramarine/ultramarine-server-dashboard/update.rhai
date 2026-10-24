let image = "ghcr.io/ultramarine-linux/dashboard";
let tag = oci_tag(image);
rpm.version(tag);
rpm.global("dashboard_digest", oci_digest(image, tag));
