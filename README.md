# whispergate-ludus-source

Custom [Ludus](https://docs.ludus.cloud) source that aggregates [Whispergate](https://github.com/Whispergate) Ludus Ansible roles as **git submodules**, ships the [Labyrinth](https://github.com/Whispergate/Labyrinth) MAAS blueprint, and automates Labyrinth post-deploy steps 4–8 via `whispergate.ludus_labyrinth_bootstrap`.

Wrapper files in this repository are **BSD-2-Clause** (see [LICENSE](LICENSE)). Each submodule keeps its upstream license (see [NOTICE](NOTICE) and [ansible/roles/README.md](ansible/roles/README.md)).

## Quick start

```bash
git clone --recurse-submodules https://github.com/ryokubaka/whispergate-ludus-source.git
ludus source add https://github.com/ryokubaka/whispergate-ludus-source
ludus blueprint install whispergate-ludus-source/labyrinth
ludus blueprint apply whispergate-ludus-source/labyrinth
ludus range deploy
```

Optional: add [badsectorlabs/ludus-source-bsl](https://github.com/badsectorlabs/ludus-source-bsl) for the full Bad Sector Labs catalog. The Labyrinth blueprint `requirements.yml` already pulls Elastic and CommandoVM roles from GitHub.

## Layout

| Path | Purpose |
|------|---------|
| `source.yml` | Ludus source metadata |
| `ansible/roles/whispergate.*` | Submodule pointers to Whispergate roles |
| `ansible/roles/whispergate.ludus_labyrinth_bootstrap` | Post-deploy pipeline bootstrap (first-party) |
| `blueprints/labyrinth/` | Labyrinth range config + BSL dependencies |

## Labyrinth bootstrap (steps 4–8)

After range deploy, `whispergate.ludus_labyrinth_bootstrap` on the **Mythic** VM:

1. Creates a Mythic API token (or uses `labyrinth_mythic_api_token`).
2. Runs Whispergate [pipeline/setup.sh](https://github.com/Whispergate/Labyrinth/blob/main/pipeline/setup.sh) non-interactively.
3. Stages Daedalus/Sphinx eventing workflow files (UI import if GraphQL import is unavailable).
4. Writes Daedalus `.env` and restarts the container.
5. Verifies Forgejo loader repos and Jenkins jobs.

Useful `role_vars` on the mythic VM:

| Variable | Default | Description |
|----------|---------|-------------|
| `labyrinth_mirror_tooling` | `false` | When `true`, run Labyrinth’s Forgejo tool-mirror step (slow). |
| `labyrinth_mythic_api_token` | (empty) | Skip auto token creation when set. |
| `labyrinth_force_bootstrap` | `false` | Re-run even if state file exists. |

Re-run bootstrap only:

```bash
ludus range deploy -t user-defined-roles
```

## Refresh upstream Whispergate content

```bash
./scripts/pull-upstream.sh
git status
git commit -am "chore: sync Whispergate submodules and Labyrinth LICENSE"
```

Initial submodule registration (maintainers):

```bash
./scripts/add-whispergate-submodules.sh
```

## References

- [Whispergate](https://github.com/Whispergate)
- [Labyrinth](https://github.com/Whispergate/Labyrinth)
- [Ludus sources](https://docs.ludus.cloud/docs/using-ludus/sources)
- [ludus-source-template](https://github.com/badsectorlabs/ludus-source-template)
