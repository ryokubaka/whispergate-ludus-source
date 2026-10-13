# Ansible roles

Whispergate Ludus roles are **git submodules** under `whispergate.<role_name>/`. Ludus installs them when you add or sync this source (`git clone --recurse-submodules`).

| Submodule path | Upstream repository | License (see upstream) |
|----------------|---------------------|--------------------------|
| `whispergate.ludus_ad_misconfigs` | https://github.com/Whispergate/ludus_ad_misconfigs | GPL-2.0-or-later |
| `whispergate.ludus_dfir_iris` | https://github.com/Whispergate/ludus_dfir_iris | MIT |
| `whispergate.ludus_evilginx_role` | https://github.com/Whispergate/ludus_evilginx_role | BSD-2-Clause |
| `whispergate.ludus_forgejo` | https://github.com/Whispergate/ludus_forgejo | BSD-2-Clause |
| `whispergate.ludus_gitlab_ce` | https://github.com/Whispergate/ludus_gitlab_ce | BSD-2-Clause |
| `whispergate.ludus_jenkins` | https://github.com/Whispergate/ludus_jenkins_role | MIT |
| `whispergate.ludus_jenkins_agent` | https://github.com/Whispergate/ludus_jenkins_agent | BSD-2-Clause |
| `whispergate.ludus_jenkins_agent_windows` | https://github.com/Whispergate/ludus_jenkins_agent_windows | BSD-2-Clause |
| `whispergate.ludus_litterbox` | https://github.com/Whispergate/ludus_litterbox_role | MIT |
| `whispergate.ludus_litterbox_whiskers_agent` | https://github.com/Whispergate/ludus_litterbox_whiskers_agent | MIT |
| `whispergate.ludus_maas_builders` | https://github.com/Whispergate/ludus_maas_builders | BSD-2-Clause |
| `whispergate.ludus_mailhog` | https://github.com/Whispergate/ludus_mailhog_role | BSD-2-Clause |
| `whispergate.ludus_misp_role` | https://github.com/Whispergate/ludus_misp | MIT |
| `whispergate.ludus_mythic_teamserver` | https://github.com/Whispergate/ludus_mythic_teamserver | GPL-3.0 |
| `whispergate.ludus_nginx_redirector` | https://github.com/Whispergate/ludus_nginx_redirector | BSD-2-Clause |
| `whispergate.ludus_pterodactyl` | https://github.com/Whispergate/ludus_pterodactyl_role | BSD-2-Clause |
| `whispergate.ludus_pwndrop_role` | https://github.com/Whispergate/ludus_pwndrop_role | BSD-2-Clause |
| `whispergate.ludus_sheepl_role` | https://github.com/Whispergate/ludus_sheepl_role | BSD-2-Clause |
| `whispergate.ludus_thehive` | https://github.com/Whispergate/ludus_thehive | MIT |
| `whispergate.ludus_threat_hunting` | https://github.com/Whispergate/ludus_threat_hunting | BSD-2-Clause |
| `whispergate.ludus_vs_build_tools` | https://github.com/Whispergate/ludus_vs_build_tools | BSD-2-Clause |
| `whispergate.ludus_wazuh_agent` | https://github.com/Whispergate/ludus_wazuh_agent | Apache-2.0 |

First-party role (this repository, BSD-2-Clause):

| Role | Purpose |
|------|---------|
| `whispergate.ludus_labyrinth_bootstrap` | Automates Labyrinth post-deploy steps 4–8 on the Mythic VM |

Regenerate the submodule list with `scripts/role-inventory.tsv` after upstream changes.
