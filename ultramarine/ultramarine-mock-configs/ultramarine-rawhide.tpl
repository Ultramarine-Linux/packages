# {% set rawhide = 45 %}
config_opts['rawhide'] = '45'

config_opts['root'] = 'ultramarine-{{ releasever }}-{{ target_arch }}'
config_opts['dist'] = 'um{{ releasever }}'  # only useful for --resultdir variable subst
config_opts['macros']['%dist'] = '.um{{ releasever }}'
config_opts['macros']['%ultramarine'] = '{{ releasever }}'
config_opts['chroot_setup_cmd'] = 'install @buildsys-build'
config_opts['buildroot_pkgs'] = 'terra-release terra-release-extras ultramarine-release ultramarine-release-basic'
config_opts['package_manager'] = 'dnf5'
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]
config_opts['mirrored'] = True
config_opts['plugin_conf']['root_cache_enable'] = True
config_opts['plugin_conf']['yum_cache_enable'] = True
config_opts['plugin_conf']['ccache_enable'] = True
config_opts['plugin_conf']['ccache_opts']['compress'] = 'on'
config_opts['plugin_conf']['ccache_opts']['max_cache_size'] = '10G'
# repos
dnf_conf = """

[main]
keepcache=1
debuglevel=2a
#reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
exclude = fedora-release*
syslog_device=
install_weak_deps=0
metadata_expire=0
best=1
module_platform_id=platform:um{{ releasever }}
protected_packages=
user_agent={{ user_agent }}

{%- macro rawhide_gpg_keys() -%}
file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-$releasever-primary
{%- for version in [rawhide, rawhide|int - 1, rawhide|int + 1]
%} file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ version }}-primary
{%- endfor %}
{%- endmacro %}

[ultramarine]
name=ultramarine
baseurl=https://repos.fyralabs.com/um$releasever/
type=rpm-md
skip_if_unavailable=False
gpgcheck=1
gpgkey=https://repos.fyralabs.com/um$releasever/key.asc
repo_gpgcheck=1
enabled=1
enabled_metadata=1
priority=50

[terra]
name=Terra $releasever
baseurl=https://repos.fyralabs.com/terra$releasever
type=rpm-md
skip_if_unavailable=False
gpgcheck=1
gpgkey=https://repos.fyralabs.com/terra$releasever/key.asc
repo_gpgcheck=1
enabled=1
enabled_metadata=1
#metadata_expire=4h

[local-rawhide-build]
name=local-rawhide
baseurl=https://kojipkgs.fedoraproject.org/repos/rawhide/latest/$basearch/
cost=2000
# enabled only if not mirrored, and rawhide
enabled={% if not mirrored and releasever == 'rawhide' %}1{% else %}0{% endif %}
skip_if_unavailable=False

[local]
name=local
baseurl=https://kojipkgs.fedoraproject.org/repos/rawhide/latest/$basearch/
cost=2000
enabled={{ not mirrored }}
skip_if_unavailable=False

{% if mirrored %}
[fedora]
name=fedora
metalink=https://mirrors.fedoraproject.org/metalink?repo=rawhide&arch=$basearch
gpgkey={{ rawhide_gpg_keys() }}
gpgcheck=1
skip_if_unavailable=False
{% endif %}
"""

config_opts['dnf.conf'] = dnf_conf
config_opts['dnf5.conf'] = dnf_conf
