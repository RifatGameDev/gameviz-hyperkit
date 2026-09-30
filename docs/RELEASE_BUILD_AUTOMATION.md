# Release Build Automation

HyperKit 1.0 uses executable verification, stable-release certification, and protected publishing workflows.

## Core Release Checks

Start from the repository root:

`hyperkit api-freeze-check`

Then run:

`hyperkit stable-release-check`

followed by:

`hyperkit release-check`

and the final source-tree audit:

`hyperkit pre-release-audit`

These commands validate package metadata, documentation, required tests, version synchronization, roadmap state, templates, and release-readiness structure.

## Build the Python Distributions

Create a clean wheel and source distribution:

`python -m build`

Validate the package metadata:

`twine check dist/*`

Verify the built artifact structure and package version:

`hyperkit verify-dist`

## Artifact Integrity

Generate SHA-256 checksums and a machine-readable release manifest:

`hyperkit release-manifest`

Expected additional files:

```text
dist/SHA256SUMS
dist/release-manifest.json
```

The manifest records artifact filename, kind, size, SHA-256 digest, package version, and source commit when provided.

## Clean-install Verification

Every release requires clean-install verification from the built wheel:

`hyperkit verify-clean-install`

The command creates a fresh temporary virtual environment, installs the wheel, imports HyperKit, verifies the package version, and verifies `python -m hyperkit --version`.

The isolated environment is deleted after verification.

## Continuous Integration

The normal `.github/workflows/ci.yml` package job now performs:

1. package build
2. `twine check`
3. `hyperkit verify-dist`
4. checksum and release-manifest generation
5. clean-install verification
6. verified artifact upload

This makes package-installation regressions block normal CI instead of being discovered only at publication time.

## Public Beta Workflow

The historical v0.9 workflow:

`.github/workflows/public-beta.yml`

remains as beta release evidence. It validates the frozen API and may
publish only to TestPyPI.

## Stable Release Workflow

The v1.0 workflow:

`.github/workflows/stable-release.yml`

runs the Python 3.9–3.12 regression matrix, exact API freeze validation,
`stable-release-check`, all SDK release gates, package build, `twine
check`, distribution verification, release-manifest generation, and
fresh-wheel installation.

It also writes:

`dist/stable-release-certificate.json`

Real PyPI publication is disabled by default. It requires explicit
confirmation and workflow execution from `refs/tags/v1.0.1`.

## Controlled Release Workflow

The manual workflow:

`.github/workflows/release-package.yml`

runs the full test and release gates before any publication action.

It supports:

- verification only
- TestPyPI
- real PyPI

Real PyPI publication requires an explicit production confirmation input in addition to selecting the PyPI target. It also requires a stable `MAJOR.MINOR.PATCH` package version and the matching `v<version>` Git tag.

You can inspect target eligibility directly:

`hyperkit publish-check --target testpypi`

or:

`hyperkit publish-check --target pypi`

## Trusted Publishing

The release workflow uses GitHub OIDC with PyPI Trusted Publishing.

Configure the corresponding publishers/environments before using publication jobs:

- `testpypi`
- `pypi`

No PyPI API token is embedded in the workflow or repository.

## Build Repeatability

The controlled release workflow:

- checks out full source history
- derives `SOURCE_DATE_EPOCH` from the release source commit
- sets `PYTHONHASHSEED=0`
- removes previous build and distribution output
- generates SHA-256 identities for final artifacts

These controls make the build inputs explicit and the resulting artifacts traceable to the selected source commit.

## Android Production Release

Generate the store-oriented Android profile with:

`hyperkit init-android --production --overwrite`

Validate configuration and signing inputs:

`hyperkit android-release-doctor`

The production profile uses Android API 36, NDK 29, an AAB release artifact, and the python-for-android `develop` branch while preserving the older API 35 development/debug defaults.

The protected workflow:

`.github/workflows/android-production-release.yml`

builds a signed release AAB using protected GitHub environment secrets and uploads the AAB with a SHA-256 checksum.

## Publishing Rule

Use TestPyPI for release-candidate or packaging validation when useful.

A stable release may be published to real PyPI only after all required gates pass, including automated tests, template validation, package build validation, `twine check`, clean-install verification, release artifact verification, and required Android/provider QA for the target release.

The v1.0 stable workflow is the final certification path. Real PyPI
publication remains a separate explicit action after all stable gates pass.
