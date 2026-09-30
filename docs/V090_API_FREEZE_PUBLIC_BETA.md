# HyperKit v0.9 — API Freeze + Public Beta

HyperKit v0.9 freezes the intended public API for the 1.0 line and prepares the SDK for public beta validation.

## Scope

The v0.9 milestone focuses on:

- exact public API freeze
- API compatibility contract 1.0
- public API fingerprinting
- API freeze validation from the CLI
- beta package identity
- deprecation policy review
- public beta release workflow
- final documentation and compatibility review before 1.0

No broad new gameplay or runtime feature category should be added during v0.9.

## Beta Package Version

The active beta package version is:

`0.9.0b1`

The package version and API compatibility contract remain separate:

- package version: `0.9.0b1`
- compatibility contract: API `1.0`

The API contract represents the intended stable 1.0 public surface even though the package itself is still a beta.

## Frozen Public API

`hyperkit.FROZEN_PUBLIC_API` is the exact top-level export set intended for HyperKit 1.0.

The freeze requires:

- every frozen name exists
- no frozen name is missing
- no unexpected top-level export is added
- no duplicate name appears in `hyperkit.__all__`

Run:

```bash
hyperkit api-freeze-check
```

The command validates the exact public export set and reports:

- API contract version
- number of frozen exports
- deterministic SHA-256 API fingerprint
- freeze validation status

## Compatibility Contract

The compatibility helpers now use API `1.0`:

```python
from hyperkit import (
    API_VERSION,
    get_api_version,
    is_api_compatible,
    require_api_version,
)

assert API_VERSION == "1.0"
assert get_api_version() == "1.0"
assert is_api_compatible("1.0")
require_api_version("1.0")
```

Older `0.x` compatibility contracts are not treated as API-compatible with the frozen 1.0 contract.

## API Fingerprint

`get_api_fingerprint()` produces a deterministic SHA-256 fingerprint from the sorted frozen export names.

The fingerprint is useful for:

- release evidence
- CI regression detection
- beta compatibility checks
- confirming that the frozen export set has not drifted accidentally

The fingerprint describes exported names, not full Python call signatures. Signature and behavior regressions remain protected by the existing automated test suite and public API tests.

## Deprecation Policy

During the public beta:

- frozen public names should not be removed
- incompatible renames should not be introduced
- additions to the top-level frozen API require explicit freeze review
- obsolete behavior should use HyperKit's deprecation framework before removal
- any post-beta incompatible change must be documented before the stable 1.0 release

Existing deprecation helpers remain public:

- `HyperKitDeprecationWarning`
- `deprecated`
- `warn_deprecated`
- `build_deprecation_message`

## Public Beta Workflow

The manual workflow:

`.github/workflows/public-beta.yml`

performs:

1. Python 3.9–3.12 regression tests
2. exact API freeze validation
3. health/template/complete-game/generated-project validation
4. release readiness and pre-release audit
5. package build and `twine check`
6. distribution verification
7. release manifest generation
8. clean-install verification
9. beta publishing-target validation
10. upload of the verified beta bundle
11. optional TestPyPI publication through Trusted Publishing

The public beta workflow does not publish to real PyPI.

## Beta Validation Expectations

Before v1.0:

- beta package installs cleanly
- all six complete games remain valid
- Android/mobile regressions remain green
- Ads and Analytics regressions remain green
- production release tooling remains green
- frozen API does not drift
- documentation matches the frozen API and package identity
- no release-blocking beta issue remains unresolved

## v0.9 Completion Rule

The v0.9 milestone is complete when:

- exact frozen API tests pass
- API contract 1.0 compatibility tests pass
- API fingerprint tests pass
- beta version metadata tests pass
- API freeze CLI tests pass
- public beta workflow regression tests pass
- all v0.8 production-hardening regressions remain green
- Python 3.9–3.12 CI remains green
- wheel/sdist build and `twine check` remain green
- clean-install verification remains green
- full health/release/audit gates remain green

After v0.9, the next roadmap milestone is v1.0.0 Stable Release.
