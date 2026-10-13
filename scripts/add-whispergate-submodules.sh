#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROLES_REL="ansible/roles"

declare -A MAP=(
  [ludus_ad_misconfigs]=whispergate.ludus_ad_misconfigs
  [ludus_dfir_iris]=whispergate.ludus_dfir_iris
  [ludus_evilginx_role]=whispergate.ludus_evilginx_role
  [ludus_forgejo]=whispergate.ludus_forgejo
  [ludus_gitlab_ce]=whispergate.ludus_gitlab_ce
  [ludus_jenkins_agent]=whispergate.ludus_jenkins_agent
  [ludus_jenkins_agent_windows]=whispergate.ludus_jenkins_agent_windows
  [ludus_jenkins_role]=whispergate.ludus_jenkins
  [ludus_litterbox_role]=whispergate.ludus_litterbox
  [ludus_litterbox_whiskers_agent]=whispergate.ludus_litterbox_whiskers_agent
  [ludus_maas_builders]=whispergate.ludus_maas_builders
  [ludus_mailhog_role]=whispergate.ludus_mailhog
  [ludus_misp]=whispergate.ludus_misp_role
  [ludus_nginx_redirector]=whispergate.ludus_nginx_redirector
  [ludus_pterodactyl_role]=whispergate.ludus_pterodactyl
  [ludus_pwndrop_role]=whispergate.ludus_pwndrop_role
  [ludus_sheepl_role]=whispergate.ludus_sheepl_role
  [ludus_thehive]=whispergate.ludus_thehive
  [ludus_threat_hunting]=whispergate.ludus_threat_hunting
  [ludus_vs_build_tools]=whispergate.ludus_vs_build_tools
  [ludus_mythic_teamserver]=whispergate.ludus_mythic_teamserver
  [ludus_wazuh_agent]=whispergate.ludus_wazuh_agent
)

cd "${ROOT}"
mkdir -p "${ROLES_REL}"

for repo in "${!MAP[@]}"; do
  path="${ROLES_REL}/${MAP[$repo]}"
  url="https://github.com/Whispergate/${repo}.git"
  if [[ -d "${path}/.git" ]] || [[ -f "${path}/.git" ]]; then
    echo "[=] ${MAP[$repo]} already present"
    continue
  fi
  echo "[+] submodule add ${url} -> ${path}"
  git submodule add "${url}" "${path}"
done

echo "[+] All submodules registered."
