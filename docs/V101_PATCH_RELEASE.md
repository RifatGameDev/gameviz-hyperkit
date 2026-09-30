# HyperKit v1.0.1 — Stable Patch Release

HyperKit v1.0.1 is the first stable patch release of GameViz HyperKit.

## Patch Release Identity

- Package: `gameviz-hyperkit`
- Import: `hyperkit`
- CLI: `hyperkit`
- Stable package version: `1.0.1`
- Public compatibility contract: API `1.0`
- Frozen top-level public exports: `256`
- Frozen API fingerprint remains unchanged from v1.0.0:
  `80bdc58a8590797b01faa0305ec3aac22ed81ea17fc98b8d9a02ec211fa70d75`

## Purpose

v1.0.1 republishes the synchronized post-release documentation and release-validation updates that were made after the original v1.0.0 publication.

The patch does not intentionally expand or break the frozen public API. Its main purpose is to make the package metadata, PyPI long description, repository documentation, and protected release workflow agree on the current stable release.

## Included Updates

- package and module version synchronized to `1.0.1`
- README current-release status synchronized to `1.0.1`
- roadmap and version-history current-release markers synchronized
- changelog records the v1.0.1 patch release
- stable-release certification updated for `1.0.1`
- protected PyPI publication requires Git tag `v1.0.1`
- Android production release default version updated to `1.0.1`
- Python 3.9–3.12 CI remains required
- frozen API `1.0`, 256-name export surface, and API fingerprint remain unchanged

## Required Validation

Before publication, the release source must pass:

```bash
pytest -q
hyperkit api-freeze-check
hyperkit stable-release-check
hyperkit health
hyperkit validate-templates
hyperkit validate-complete-games
hyperkit validate-generated-projects
hyperkit release-check
hyperkit pre-release-audit
python -m build
python -m twine check dist/*
hyperkit verify-dist
hyperkit release-manifest
hyperkit verify-clean-install
```

## Protected Publication

Real PyPI publication is disabled by default.

Publishing v1.0.1 requires:

- package version exactly `1.0.1`
- explicit `publish_pypi` confirmation
- workflow execution from Git tag `v1.0.1`
- all stable-release jobs passing
- protected `pypi` environment
- PyPI Trusted Publishing / GitHub OIDC

## Historical Note

HyperKit v1.0.0 remains the first stable release. v1.0.1 is a compatible patch release in the same API `1.0` line.
