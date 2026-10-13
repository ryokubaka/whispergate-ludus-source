#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABYRINTH_REPO="${LABYRINTH_REPO:-https://github.com/Whispergate/Labyrinth.git}"
LABYRINTH_REF="${LABYRINTH_REF:-main}"
BP_DIR="${ROOT}/blueprints/labyrinth"
PATCH_FILE="${ROOT}/scripts/labyrinth-range-config.patch"

cd "${ROOT}"

echo "[*] Updating Whispergate role submodules..."
git submodule update --init --recursive
git submodule update --remote --merge

TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

echo "[*] Fetching Labyrinth ${LABYRINTH_REF}..."
git clone --depth 1 --branch "${LABYRINTH_REF}" --single-branch "${LABYRINTH_REPO}" "${TMP}/labyrinth"

cp "${TMP}/labyrinth/LICENSE" "${BP_DIR}/LICENSE"

if [[ -f "${PATCH_FILE}" ]]; then
  echo "[*] Merging upstream range-config.yml with local patch..."
  cp "${TMP}/labyrinth/range-config.yml" "${BP_DIR}/range-config.yml.upstream"
  cp "${BP_DIR}/range-config.yml" "${BP_DIR}/range-config.yml.ours"
  cp "${TMP}/labyrinth/range-config.yml" "${BP_DIR}/range-config.yml"
  if ! git apply --directory=blueprints/labyrinth "${PATCH_FILE}" 2>/dev/null; then
    echo "[!] Patch did not apply cleanly; keeping committed range-config.yml"
    mv "${BP_DIR}/range-config.yml.ours" "${BP_DIR}/range-config.yml"
  fi
  rm -f "${BP_DIR}/range-config.yml.upstream" "${BP_DIR}/range-config.yml.ours"
else
  echo "[!] No ${PATCH_FILE}; only refreshed LICENSE from upstream"
fi

echo "[+] Done. Review git diff and commit submodule + blueprint updates."
