import "andax/bump_extras.rhai" as bump;

// ultramarine-plasma-discover.spec is generated from Fedora's spec. don't edit by hand.
//
// 1. Bodhi: upstream plasma-discover build
// 2. Koji: the dist-git commit that build came from
// 3. dist-git: the spec, `sources`, and any patches/files Fedora carries at that commit.
// 4. plasma-patches: discover/<major.minor>/<patch>, or discover/<patch> (the current
//    Plasma release) if there's no directory for this minor version. Checked to apply
//    with --fuzz=0 on top of Fedora's patches before anything is written. If it
//    doesn't apply, nothing changes until it's rebased.
//
// release is our own release number. if Fedora bumps, it'll add to our release.
// that means our release won't match Fedora's all the time, so be mindful of that.

// pkg is Fedora's package, name is ours. Ours provides, conflicts with and
// obsoletes Fedora's (and its subpackages), so it replaces it everywhere,
// including the comps groups we can't change.
let pkg = "plasma-discover";
let name = "ultramarine-plasma-discover";
// Upstream (KDE) and plasma-patches name
let base = "discover";
let dir = `ultramarine/${name}`;
let patch_name = "0001-Remove-Discover-updates-UI-in-favor-of-um.patch";

if labels.get("branch") == () {
    print(`${pkg}: needs the branch label (anda update -l branch=um45)`);
    terminate();
}
let branch = labels.branch;
branch.crop(2);
let release = bump::as_bodhi_ver(if branch == "rawhide" { "frawhide" } else { `f${branch}` });

// Bodhi and Koji are behind Anubis, which blocks anda's "AndaX" User-Agent,
// so use curl for them
fn curl(args) {
    let r = sh(`curl -fsSL -m 60 ${args}`, #{"stdout": "piped"});
    if r.outcome != "success" || r.ctx.rc != 0 {
        print(`plasma-discover: request failed: curl ${args}`);
        terminate();
    }
    return r.ctx.stdout;
}

// 1. Stable build
let update = curl(`"https://bodhi.fedoraproject.org/updates/?packages=${pkg}&releases=${release}&status=stable&rows_per_page=1"`).json().updates[0];
let nvr = "";
for build in update.builds {
    if build.nvr.starts_with(`${pkg}-`) && find_all(`^${pkg}-[\d.]+-[^-]+$`, build.nvr).len() != 0 {
        nvr = build.nvr;
    }
}
if nvr == "" {
    print(`${pkg}: no stable ${pkg} build in ${update.alias}`);
    terminate();
}
let version = find(`^${pkg}-([\d.]+)-`, nvr, 1);
let minor = find(`^(\d+\.\d+)`, version, 1);

// What the current spec was generated from
let old_nvr = if find_all(`(?m)^%global fedora_nvr `, rpm.f).len() != 0 {
    find(`(?m)^%global fedora_nvr\s+(\S+)`, rpm.f, 1)
} else {
    ""
};
let old_version = find(`(?m)^Version:\s*(\S+)$`, rpm.f, 1);
let old_rel = find(`(?m)^Release:\s*(\d+)`, rpm.f, 1).parse_int();

let patch_path = `${base}/${minor}/${patch_name}`;
let patch = "";
try {
    patch = gh_rawfile("Ultramarine-Linux/plasma-patches", "main", patch_path);
} catch {
    patch_path = `${base}/${patch_name}`;
    patch = gh_rawfile("Ultramarine-Linux/plasma-patches", "main", patch_path);
}
let patch_changed = open_file(`${dir}/${patch_name}`).read_string() != patch;
if nvr == old_nvr && !patch_changed {
    return;
}

// 2. dist-git commit of the stable build
let koji = curl(`-H "Content-Type: text/xml" --data '<?xml version="1.0"?><methodCall><methodName>getBuild</methodName><params><param><value><string>${nvr}</string></value></param></params></methodCall>' https://koji.fedoraproject.org/kojihub`);
let commit = find(`git\+https://src\.fedoraproject\.org/rpms/${pkg}(?:\.git)?#([0-9a-f]{40})`, koji, 1);

// 3. Fedora's spec, lookaside list and local files at that commit
let distgit = `https://src.fedoraproject.org/rpms/${pkg}/raw/${commit}/f`;
let fedora = curl(`"${distgit}/${pkg}.spec"`);
let lookaside = curl(`"${distgit}/sources"`);
if find_all(`(?m)^Release:\s*\d+%\{\?dist\}\s*$`, fedora).len() == 0 {
    print(`${pkg}: Fedora's Release isn't "<n>%{?dist}" (autorelease?), update.rhai needs adjusting`);
    terminate();
}
let fedora_rel = find(`(?m)^Release:\s*(\d+)%\{\?dist\}\s*$`, fedora, 1).parse_int();
// New version: Fedora's Release. Same version: max(ours + 1, Fedora's). Ties sort
// our way because .umXX > .fcXX.
let ours = if old_version == version { old_rel + 1 } else { 0 };
let rel = if ours > fedora_rel { ours } else { fedora_rel };

let spec = "";
let files = [];
// [number, file] of Fedora's local patches, to check ours on top of them
let fedora_patches = [];
for line in fedora.split("\n") {
    let out = line;
    let m = find_all(`^((?:Source|Patch)\d*:\s*)(\S+)\s*$`, line);
    if m.len() != 0 {
        let prefix = find(`^((?:Source|Patch)\d*:\s*)`, line, 1);
        let value = find(`^(?:Source|Patch)\d*:\s*(\S+)`, line, 1);
        if value.contains("://") {
            // kf6-rpm-macros isn't in the SRPM chroot, so use %{version} in KDE URLs
            value.replace("%{stable_kf6}", "stable");
            value.replace("%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}", "%{version}");
            // %{name} is ours now; upstream tarballs use Fedora's name.
            value.replace("%{name}", pkg);
        } else {
            let file = value;
            file.replace("%{name}", pkg);
            file.replace("%{version}", version);
            let escaped = file;
            escaped.replace(".", "\\.");
            let re = `(?m)^SHA512 \(${escaped}\) = ([0-9a-f]+)$`;
            if find_all(re, lookaside).len() != 0 {
                let sum = find(re, lookaside, 1);
                value = `https://src.fedoraproject.org/repo/pkgs/rpms/${pkg}/${file}/sha512/${sum}/${file}`;
            } else {
                files.push(file);
                if line.starts_with("Patch") {
                    fedora_patches.push([find(`^Patch(\d*):`, line, 1).parse_int(), file]);
                }
            }
        }
        out = `${prefix}${value}`;
    }
    if line.starts_with("Release:") {
        out = `Release: ${rel}%{?dist}`;
    }
    if line.starts_with("%autosetup") && !line.contains(" -C") {
        out.replace("%autosetup", "%autosetup -C");
    }
    if line.starts_with("URL:") {
        out.replace("%{name}", pkg);
    }
    if line.starts_with("Name:") {
        out = `Name:    ${name}`;
    }
    spec += out + "\n";
    // Replace Fedora's package and each %package <sub> (not -n, those keep their
    // own name). The main block goes after Release:, because rpm only defines
    // %{version} and %{release} once it has read those lines.
    let replaces = "";
    if line.starts_with("Release:") {
        replaces = pkg;
    } else if find_all(`^%package\s+[^-\s]\S*\s*$`, line).len() != 0 {
        replaces = `${pkg}-${find(`^%package\s+(\S+)`, line, 1)}`;
    }
    if replaces != "" {
        spec += `# Replaces Fedora's ${replaces}.
Provides:       ${replaces} = %{evr}
`;
        if replaces == pkg {
            spec += `Provides:       ${replaces}%{?_isa} = %{evr}
`;
        }
        spec += `Conflicts:      ${replaces}
Obsoletes:      ${replaces} < %{evr}
`;
    }
    if line.starts_with("## downstream patches") {
        spec += `# Updates are handled by um and System Settings > Updates (kcm_ultramarine_updates).
# Synced from https://github.com/Ultramarine-Linux/plasma-patches/blob/main/${patch_path}
Patch300: ${patch_name}
`;
    }
}
if !spec.contains("Patch300:") {
    print(`${pkg}: no "## downstream patches" section in Fedora's spec, update.rhai needs adjusting`);
    terminate();
}
spec.trim();
spec = `# Generated by update.rhai from Fedora's ${nvr}
# (dist-git ${commit}) plus Ultramarine's Discover updates patch. Don't edit by hand.
%global fedora_nvr ${nvr}

${spec}
`;

// 4. Check the patch against the new tarball, after Fedora's patches (%autosetup
//    applies them in number order, ours is 300), before writing anything
fedora_patches.sort(|a, b| a[0] - b[0]);
let apply_fedora = "";
for p in fedora_patches {
    if p[0] < 300 {
        apply_fedora += `curl -fsSL -m 60 "${distgit}/${p[1]}" | patch -d "$tmp/src" -p1 -s --fuzz=0
`;
    }
}
let check = sh(`set -eo pipefail
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/src"
cat > "$tmp/patch" <<'ANDA_PATCH_EOF'
${patch}
ANDA_PATCH_EOF
curl -fsSL "https://download.kde.org/stable/plasma/${version}/${base}-${version}.tar.xz" \
    | tar -xJ -C "$tmp/src" --strip-components=1
${apply_fedora}
patch -d "$tmp/src" -p1 --dry-run -s --fuzz=0 < "$tmp/patch"`, #{});
if check.outcome != "success" || check.ctx.rc != 0 {
    print(`${pkg}: ${patch_name} doesn't apply to ${version} with Fedora's patches (or the tarball is missing), not updating. Rebase it in plasma-patches/${base}/${minor}/.`);
    terminate();
}

// Write everything
for file in files {
    curl(`-o "${dir}/${file}" "${distgit}/${file}"`);
}
// Drop Fedora files the new spec doesn't use anymore
let manifest = `${dir}/fedora-files.txt`;
let present = ls(dir);
if present.contains(manifest) {
    for old in open_file(manifest).read_string().split("\n") {
        if old != "" && !files.contains(old) && present.contains(`${dir}/${old}`) {
            sh(`rm -f "${dir}/${old}"`, #{});
        }
    }
}
let list = "";
for file in files {
    list += file + "\n";
}
list.write(manifest);
if patch_changed {
    patch.write(`${dir}/${patch_name}`);
}
rpm.f = spec;
