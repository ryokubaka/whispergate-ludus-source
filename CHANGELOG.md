# Changelog

All notable changes to [whispergate-ludus-source](https://github.com/ryokubaka/whispergate-ludus-source) will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Each bullet uses a single tag:

- **[Add]** — New capability
- **[Improve]** — UX polish or refactor without a new feature
- **[Fix]** — Bug fix
- **[Docs]** — Documentation improvement

Write new notes under **[Unreleased]**. After merge to `dev`, CI promotes that
section to the next GitHub Release (patch by default). Put
`<!-- release: minor -->` or `<!-- release: major -->` in Unreleased when the
bump is not a patch. Do not invent a version heading on a feature branch.

---

## [Unreleased]

## [1.0.1] - 2026-11-12

- [Add] GitHub Actions CI. Release-script unit tests, `bash -n` on `scripts/*.sh`, and a changelog-driven GitHub Release after merge to `dev`.

## [1.0.0] - 2026-11-12

- [Add] Whispergate Ludus source with role submodules and the Labyrinth blueprint.
