# Agent notes

Ludus and LUX decide whether to refresh a role or blueprint by its version. A content change that leaves the version the same is easy to miss on sync. Bump the version in the same change as the code.

## What to bump

Use semantic versions (`MAJOR.MINOR.PATCH`). Patch for fixes, minor for new behavior, major when `role_vars`, range config, or required inputs change in a way existing ranges cannot absorb.

| You changed | Bump |
|---|---|
| Role tasks, handlers, defaults, vars, files, templates, or `meta/` | That role's version |
| `blueprints/<id>/` (`blueprint.yml`, `range-config.yml`, `requirements.yml`, or `scripts/labyrinth-range-config.patch`) | `version` in `blueprints/<id>/blueprint.yml` |
| More than one of the above | Each artifact you edited |

Role version file, in order:

1. `ansible/roles/<role>/meta/version.yml` — `version:`. This is what Ludus reads for a role added from a directory.
2. `ansible/roles/<role>/galaxy.yml` — `version:`, when the role ships as a collection and has no `meta/version.yml`.

Templates are not versioned on their own. A template change bumps the role that owns it. A blueprint config change bumps the blueprint, not a role, unless you also edited a role.

If `meta/version.yml` is missing, add it:

```yaml
# This is a Ludus specific version number used for roles that are not hosted
# on Ansible Galaxy. It allows Ludus to show the version of the role when
# added directly from its directory.
---
version: 1.0.0
```

Later changes increment that value. Do not leave a new file at the same version as an existing one.

Most roles under `ansible/roles/whispergate.*` are git submodules. Commit the version bump in the role repository, then update this repo's submodule pointer. `whispergate.ludus_labyrinth_bootstrap` is first-party; bump it here.

## Do not bump

- `manifest_version` in `source.yml` or `blueprint.yml` (schema version).
- `min_ansible_version`.
- Upstream product pins in defaults (`ludus_forgejo_version`, Elastic versions, and similar) unless the change is specifically to that pin.
- Dependency pins in `blueprints/<id>/requirements.yml` unless you are changing that pin. A requirements change still bumps the blueprint `version`.
- Docs-only edits (`README.md`, `LICENSE`, `NOTICE`) that do not change what Ludus installs.
