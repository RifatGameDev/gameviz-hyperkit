# HyperKit v0.8 — Build, Publishing + Production Hardening

HyperKit v0.8 turns the existing development and validation toolchain into a controlled production-release workflow.

## Scope

The v0.8 milestone focuses on:

- verified Python distribution artifacts
- isolated clean-install validation
- artifact checksums and release manifests
- gated TestPyPI and PyPI publishing
- production Android release configuration
- Android signing readiness validation
- signed Android App Bundle workflow
- reproducible release inputs and release evidence

The public API freeze is not part of this milestone. API freeze remains scheduled for v0.9.

## Python Distribution Verification

After building the package:

```bash
python -m build
python -m twine check dist/*
hyperkit verify-dist
```

`hyperkit verify-dist` requires:

- exactly one wheel
- exactly one source distribution
- non-empty artifacts
- artifact filenames matching the active package version
- SHA-256 digests for each artifact

## Release Manifest and Checksums

Generate release metadata after distribution validation:

```bash
hyperkit release-manifest
```

This creates:

```text
dist/
├── gameviz_hyperkit-<version>-py3-none-any.whl
├── gameviz_hyperkit-<version>.tar.gz
├── SHA256SUMS
└── release-manifest.json
```

The JSON manifest records:

- package name
- package version
- source commit when supplied
- artifact filename
- artifact type
- artifact size
- SHA-256 digest

## Clean-Install Verification

Verify the built wheel in a fresh virtual environment:

```bash
hyperkit verify-clean-install
```

The verifier:

1. creates an isolated temporary virtual environment
2. installs the built wheel
3. imports `hyperkit`
4. verifies `hyperkit.__version__`
5. runs `python -m hyperkit --version`
6. requires the installed and CLI versions to match the built package version

The temporary environment is removed after verification.

## CI Package Hardening

The main CI package job now performs:

1. wheel and source-distribution build
2. `twine check`
3. `hyperkit verify-dist`
4. release checksum/manifest generation
5. fresh clean-install verification
6. upload of the verified release bundle

This keeps packaging regressions visible during normal development instead of discovering them only during a release.

## Gated Package Publishing Workflow

The manual workflow:

```text
.github/workflows/release-package.yml
```

supports three destinations:

- `none` — verify only
- `testpypi` — verify then publish to TestPyPI
- `pypi` — verify then publish to real PyPI

Real PyPI publication requires both:

- selecting the `pypi` target
- explicitly enabling the production confirmation input

Publishing uses GitHub OIDC / PyPI Trusted Publishing rather than storing a PyPI API token in the repository workflow.

The repository environments `testpypi` and `pypi` should be configured with the appropriate trusted-publisher rules and any desired manual approvals.

## Controlled Build Inputs

The release workflow:

- checks out full source history
- derives `SOURCE_DATE_EPOCH` from the source commit
- sets `PYTHONHASHSEED=0`
- removes previous build/dist output
- builds from a clean distribution directory
- records SHA-256 artifact identities

These controls improve build repeatability and make each uploaded artifact traceable to a source commit.

## Production Android Profile

The existing Phase 73 Android defaults remain available for the historically validated development/debug workflow.

For store-oriented builds, use the separate production profile:

```bash
hyperkit init-android --production --overwrite
```

The v0.8 production profile uses:

- target Android API 36
- minimum Android API 24
- Android NDK 29
- ARM64 default architecture
- AAB release artifact
- python-for-android `develop` branch
- SDK license acceptance

The production profile is separate from the older API 35 debug defaults so earlier validated workflows are not silently changed.

As of September 2026, Google Play requires new mobile apps and app updates submitted after August 31, 2026 to target Android 16 / API level 36 or higher, subject to Google's documented platform-specific exceptions and extension policy.

## Android Signing

python-for-android release signing uses these environment variables:

```text
P4A_RELEASE_KEYSTORE
P4A_RELEASE_KEYSTORE_PASSWD
P4A_RELEASE_KEYALIAS
P4A_RELEASE_KEYALIAS_PASSWD
```

HyperKit never prints their secret values.

Validate a production project before building:

```bash
hyperkit android-release-doctor --path .
```

The production doctor checks:

- project directory
- `main.py`
- `hyperkit.toml`
- `buildozer.spec`
- API 36
- NDK 29
- AAB output
- p4a `develop`
- all signing variables
- the configured keystore file exists

## Signed Android Production Workflow

The manual workflow:

```text
.github/workflows/android-production-release.yml
```

uses the protected `android-production` GitHub environment.

Configure these secrets in that environment:

```text
ANDROID_KEYSTORE_BASE64
ANDROID_KEYSTORE_PASSWORD
ANDROID_KEY_ALIAS
ANDROID_KEY_ALIAS_PASSWORD
```

The workflow:

1. generates a selected built-in HyperKit game
2. generates the production Android profile
3. reconstructs the signing keystore from the protected base64 secret
4. validates production/signing readiness
5. bundles the current HyperKit SDK source
6. builds with the current store-oriented Buildozer/python-for-android configuration
7. creates a signed release AAB
8. generates a SHA-256 checksum
9. uploads the AAB, checksum, and build specification as protected workflow artifacts

The keystore itself is not uploaded as an artifact.

## v0.8 Completion Rule

The v0.8 milestone is complete when:

- release artifact verification tests pass
- checksum and release-manifest tests pass
- clean-install verification tests pass
- production Android profile tests pass
- Android signing readiness tests pass
- package release workflow regression tests pass
- Android production workflow regression tests pass
- normal CI builds and clean-installs the package successfully
- Python 3.9–3.12 test matrix remains green
- all v0.7 regressions remain green
- wheel and source distribution pass `twine check`

The compatibility contract remains API `0.2` during v0.8.
Public API review and freeze remain scheduled for v0.9.
