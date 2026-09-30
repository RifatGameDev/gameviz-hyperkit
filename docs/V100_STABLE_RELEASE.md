# HyperKit v1.0.0 — Stable Release

HyperKit v1.0.0 is the first stable release of GameViz HyperKit.

## Stable Package Identity

- Package: `gameviz-hyperkit`
- Import: `hyperkit`
- CLI: `hyperkit`
- Stable package version: `1.0.0`
- Public compatibility contract: API `1.0`
- Frozen top-level public exports: `256`
- Frozen API fingerprint:
  `80bdc58a8590797b01faa0305ec3aac22ed81ea17fc98b8d9a02ec211fa70d75`

## What Stable Means

For the 1.0 line:

- the top-level public API is frozen
- API `1.0` compatibility is the stable contract
- incompatible public removals or renames require a future major-version transition
- existing behavior remains protected by the full automated regression suite
- deprecations should use HyperKit's deprecation framework before removal
- package, template, Android, Ads, Analytics, runtime, and release tooling remain covered by release gates

## Final Certification

Run:

```bash
hyperkit stable-release-check
```

The stable certification verifies:

- package version is exactly `1.0.0`
- package/module versions match
- Production/Stable package classifier is present
- API contract remains `1.0`
- exact frozen API still matches
- frozen export count remains `256`
- frozen fingerprint remains unchanged
- release readiness passes
- pre-release audit passes
- real-PyPI target eligibility passes
- stable README, roadmap, changelog, version history, docs, and workflow are synchronized

## Final Package Build

Build from a clean tree:

```bash
python -m build
python -m twine check dist/*
hyperkit verify-dist
hyperkit release-manifest
hyperkit verify-clean-install
hyperkit stable-release-check
```

## Stable Release Certificate

The stable workflow generates:

```text
dist/stable-release-certificate.json
```

The certificate records:

- package version
- API version
- frozen export count
- API fingerprint
- source commit
- stable certification checks

## Stable Release Workflow

The manual workflow:

```text
.github/workflows/stable-release.yml
```

performs:

1. Python 3.9–3.12 regression tests
2. exact API freeze validation
3. final stable-release certification
4. health/template/complete-game/generated-project validation
5. release readiness and pre-release audit
6. clean package build
7. `twine check`
8. distribution verification
9. release manifest generation
10. fresh-wheel clean-install verification
11. stable release certificate generation
12. verified artifact upload
13. optional real-PyPI publication through Trusted Publishing

## Real PyPI Safeguards

The stable workflow does not publish by default.

Real PyPI publication requires:

- package version exactly `1.0.0`
- explicit `publish_pypi` confirmation
- workflow execution from Git tag `v1.0.0`
- all verification jobs passing
- the protected `pypi` environment
- PyPI Trusted Publishing / GitHub OIDC

No PyPI API token is stored in the repository workflow.

## Android and Provider QA

The stable SDK retains the v0.8 production Android workflow and provider QA foundations.

Before treating a specific Android application as production-ready, that application's own release still needs its relevant device/provider checks, signing setup, store configuration, and app-specific QA.

## Post-1.0 Versioning

After v1.0.0:

- backward-compatible fixes belong in patch releases such as `1.0.1`
- backward-compatible additions may use later minor releases such as `1.1.0`
- incompatible public API changes require a future major version

The `1.0` compatibility contract remains the baseline stable contract until intentionally superseded.
