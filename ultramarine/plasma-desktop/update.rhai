import "andax/bump_extras.rhai" as bump;

// plasma-desktop.spec is generated from Fedora's spec. don't edit by hand.
//
// 1. Bodhi: upstream plasma-desktop build
// 2. Koji: the dist-git commit that build came from
// 3. dist-git: the spec, `sources`, and any patches Fedora carries at that commit.
// 4. plasma-patches: plasma-desktop/<major.minor>/<patch>, checked to apply with
//    --fuzz=0 before anything is written. If it doesn't apply, or there's no patch
//    for a new Plasma minor version yet, nothing changes until it's rebased.
//
// release is our own release number. if Fedora bumps, it'll add to our release.
// that means our release won't match Fedora's all the time, so be mindful of that.

let pkg = "plasma-desktop";
let dir = "ultramarine/plasma-desktop";
let patch_name = "0001-taskmanager-show-launcher-drop-in-actions.patch";

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
        print(`plasma-desktop: request failed: curl ${args}`);
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

let patch = gh_rawfile("Ultramarine-Linux/plasma-patches", "main", `${pkg}/${minor}/${patch_name}`);
let patch_changed = open_file(`${dir}/${patch_name}`).read_string() != patch;
if nvr == old_nvr && !patch_changed {
    return;
}

// 4. Check the patch against the new tarball before writing anything
let check = sh(`set -eo pipefail
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/patch" <<'ANDA_PATCH_EOF'
${patch}
ANDA_PATCH_EOF
curl -fsSL "https://download.kde.org/stable/plasma/${version}/${pkg}-${version}.tar.xz" \
    | tar -xJ -C "$tmp" --strip-components=1 --wildcards '*/applets/taskmanager/*'
patch -d "$tmp" -p1 --dry-run -s --fuzz=0 < "$tmp/patch"`, #{});
if check.outcome != "success" || check.ctx.rc != 0 {
    print(`${pkg}: ${patch_name} doesn't apply to ${version} (or the tarball is missing), not updating. Rebase it in plasma-patches/${pkg}/${minor}/.`);
    terminate();
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
            }
        }
        out = `${prefix}${value}`;
    }
    if line.starts_with("Release:") {
        out = `Release: ${rel}%{?dist}`;
    }
    spec += out + "\n";
    if line.starts_with("## downstream patches") {
        spec += `# Show plasma/kickeractions drop-in actions in the task manager context menu.
# Synced from https://github.com/Ultramarine-Linux/plasma-patches/tree/main/${pkg}/${minor}
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
# (dist-git ${commit}) plus Ultramarine's task manager patch. Don't edit by hand.
%global fedora_nvr ${nvr}

${spec}
`;

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
