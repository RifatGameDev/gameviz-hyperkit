# Release Readiness Checklist

This checklist is used before publishing a new HyperKit package version or producing a production Android release.

A release should proceed only when the package, templates, generated projects, documentation, build artifacts, and required platform QA are clean.

---

## 1. Git Status

Before release:

```bash
git status
```

Expected:

```text
working tree clean
```

---

## 2. Full Automated Tests

Run:

```bash
pytest -q
```

Expected:

```text
all tests passed
```

---

## 3. SDK Validation Gates

Run:

```bash
hyperkit health
hyperkit api-freeze-check
hyperkit stable-release-check
hyperkit validate-templates
hyperkit validate-complete-games
hyperkit validate-generated-projects
hyperkit release-check
hyperkit pre-release-audit
```

Every command must pass.

For stable 1.0, both `api-freeze-check` and `stable-release-check` are
required gates. The API check verifies the exact frozen 1.0 top-level public
export set, pinned export count, and API fingerprint. The stable release
check also verifies package identity, Production/Stable metadata, release
readiness, documentation synchronization, and real-PyPI target eligibility.

---

## 4. Generated Game Runtime Check

Create important starter games outside the package repository:

```bash
cd <workspace-outside-the-repository>
hyperkit new release-tap-test --template tap-counter
hyperkit new release-flappy-test --template flappy-mini
hyperkit new release-runner-test --template swipe-runner
```

Run the generated games as appropriate for the target release.

Do not commit generated release-test projects.

---

## 5. Clean Package Build

Remove stale package output, then build:

```bash
python -m build
```

Expected:

```text
dist/
├── gameviz_hyperkit-<version>.tar.gz
└── gameviz_hyperkit-<version>-py3-none-any.whl
```

---

## 6. Twine Validation

Run:

```bash
twine check dist/*
```

Expected:

```text
PASSED
```

---

## 7. Distribution Verification

Run:

```bash
hyperkit verify-dist
```

The command must confirm exactly one wheel and one source distribution, correct version identity, non-empty artifacts, and valid SHA-256 digests.

---

## 8. Release Artifact Manifest

Run:

```bash
hyperkit release-manifest
```

Confirm:

```text
dist/SHA256SUMS
dist/release-manifest.json
```

are present.

---

## 9. Clean-install Verification

Run clean-install verification against the built wheel:

```bash
hyperkit verify-clean-install
```

The result must report `PASS`.

This is required in addition to editable-development installation tests.

---

## 10. Package Metadata

Confirm `pyproject.toml` contains:

- package name
- package version
- description
- README reference
- Python requirement
- author information
- runtime dependencies
- CLI entry points

Expected identity:

```text
Package name: gameviz-hyperkit
Import name: hyperkit
CLI command: hyperkit
```

---

## 11. Documentation

Confirm these files are current:

- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/VERSION_HISTORY.md`
- `docs/RELEASE_BUILD_AUTOMATION.md`
- `docs/RELEASE_READINESS_CHECKLIST.md`
- current-version milestone documentation

---

## 12. Production Android Configuration

For a store-oriented Android release, generate the production profile:

```bash
hyperkit init-android --production --overwrite
```

Then run:

```bash
hyperkit android-release-doctor
```

The production doctor must pass before a signed Android release build.

The v0.8 production profile expects API 36, NDK 29, AAB output, and p4a `develop`.

---

## 13. Android Signing Secrets

Production Android signing requires:

```text
P4A_RELEASE_KEYSTORE
P4A_RELEASE_KEYSTORE_PASSWD
P4A_RELEASE_KEYALIAS
P4A_RELEASE_KEYALIAS_PASSWD
```

Never commit a keystore or signing passwords.

For the GitHub production workflow, store signing inputs in the protected `android-production` environment using:

```text
ANDROID_KEYSTORE_BASE64
ANDROID_KEYSTORE_PASSWORD
ANDROID_KEY_ALIAS
ANDROID_KEY_ALIAS_PASSWORD
```

---

## 14. Controlled Publishing

The preferred package release workflow is:

```text
.github/workflows/release-package.yml
```

Use `none` for verification only, `testpypi` for package validation, or `pypi` for real PyPI.

Real PyPI additionally requires:

- the explicit production confirmation input
- a stable `MAJOR.MINOR.PATCH` package version
- the matching `v<version>` Git tag

Validate the selected destination with:

```bash
hyperkit publish-check --target testpypi
hyperkit publish-check --target pypi
```

The workflow uses Trusted Publishing / OIDC; do not store PyPI API tokens in the repository.

---

## 15. Publishing Rule

For HyperKit 1.0 stable certification, use the dedicated workflow:

```text
.github/workflows/stable-release.yml
```

It validates Python 3.9–3.12, the frozen API, all SDK release gates, package
artifacts, clean installation, and the stable-release certificate.

Real PyPI publication is disabled by default and requires:

- explicit `publish_pypi` confirmation
- package version exactly `1.0.0`
- Git tag exactly `v1.0.0`
- the protected `pypi` environment
- all stable certification jobs passing

The historical public-beta workflow remains available as release evidence
for v0.9 and only targets TestPyPI.

Publish the stable release to real PyPI only after the full release gates
pass, including tests, template validation, build validation, `twine check`,
release artifact verification, clean-install verification, stable
certification, and required Android/provider QA for the target release.

---

## 16. Release Commit

Use a clear release preparation commit and the intended release branch:

```bash
git add .
git commit -m "Prepare HyperKit release"
git push origin <release-branch>
```
