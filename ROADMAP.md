# GameViz HyperKit — Roadmap to 1.0

This is the authoritative HyperKit development roadmap.

## Version Path

```text
v0.1.0  Foundation / Initial SDK
   ↓
v0.2.0  Core SDK
   ↓
v0.3.0  Android + Mobile
   ↓
v0.4.0  Ads + Analytics + Game Systems
   ↓
v0.5.0  Complete Games + Developer Tooling
   ↓
v0.6.0  Mobile Production Runtime + Performance
   ↓
v0.7.0  Content, Assets + Advanced Game Features
   ↓
v0.8.0  Build, Publishing + Production Hardening
   ↓
v0.9.0  API Freeze + Public Beta
   ↓
v1.0.0  Stable Release
          ← CURRENT DEVELOPMENT STAGE
```

## Current State

- Latest published PyPI release: `0.2.0`
- Active package version: `1.0.0`
- Public compatibility contract: API `1.0`
- Active development branch: `feature/v1.0-stable-release`
- Current focus: v1.0 Stable Release
- v0.4 final automated regression checkpoint: 949 passing tests
- v0.4 automated closeout:
  - project health: 133/133
  - template validation: 42/42
  - generated-project validation: 90/90
  - release readiness: 117/117
  - pre-release audit: 10/10

## Completed v0.4 Closeout

### Phase 75 — SDK Completion Audit

Phase 75 completed the large SDK hardening pass across physics, collision,
geometry, UI, layout, persistence, state, transitions, timers, levels,
input, audio, particles, animation, sprites, assets, game systems, public
API checks, CLI integration, generated-project validation, documentation,
health checks, and release-readiness tooling.

The Phase 75 documentation synchronization stage used a 919 passing tests
baseline before the later closeout work raised the suite to 949 passing
tests.

### v0.4 Foundation Delivered

- Android/mobile workflow foundation
- safe-area and viewport helpers
- Ads provider architecture
- AdMob Android test-mode integration
- Analytics provider architecture
- Firebase Analytics Android integration
- game sessions and progression
- physics world and collision system
- UI interaction and layout helpers
- assets, audio, save, animation, particles, levels, timers, bounds
- six generated starter games
- release, health, audit, and generated-project tooling

## v0.5.0 — Complete Games + Developer Tooling

The v0.5 milestone turns the existing systems into a more complete
developer workflow.

### Complete Games

The built-in game set remains:

- Tap Counter
- Flappy Mini
- Swipe Runner
- Puzzle Game
- Quiz Game
- Simple Physics

Every built-in game must provide:

- runnable game entry
- player input
- score and persistent high score
- progress feedback
- completion/game-over state
- restart flow

The command:

`hyperkit validate-complete-games`

must pass for all six games.

### Developer Tooling

v0.5 includes:

- `RuntimeDiagnostics`
- `RuntimeSnapshot`
- `DebugOverlay`
- `hyperkit diagnostics`
- `hyperkit validate-complete-games`
- Python 3.9–3.12 general CI workflow
- existing generated-project and release diagnostics

### v0.5 Definition of Done

- all complete-game checks pass
- all six generated games remain valid
- runtime diagnostics tests pass
- project diagnostics CLI works
- Python 3.9–3.12 CI matrix is defined
- v0.4 Android/Ads/Analytics/Game Systems regressions remain green
- full pytest suite passes
- health/template/generated-project/release/audit commands remain green

v0.5 completed with 973 passing automated tests, complete-game validation
54/54, generated-project validation 90/90, release readiness 115/115,
pre-release audit 10/10, Python 3.9–3.12 CI, and successful wheel/sdist
plus `twine check`.

## v0.6.0 — Mobile Production Runtime + Performance

The v0.6 milestone hardens the existing game runtime for mobile use.

### Runtime Performance

- `PerformanceMode`
- `PerformanceProfile`
- `FrameTimeController`
- `FixedStepClock`
- frame-delta clamping before scene updates
- bounded fixed-step backlog handling
- runtime performance statistics from `Game`

### Lifecycle and Resource Reliability

- explicit scene pause/background/resume/stop hooks
- idempotent `Game.stop()`
- active-touch cancellation on suspension/shutdown
- runtime lifecycle propagation to registered services
- lifecycle-aware `AudioManager`
- scene object cleanup through `release_resources()`
- cleanup of old scenes during scene transitions

### Mobile Input Tuning

- optional touch-move filtering with `move_min_distance`
- `Game(touch_move_min_distance=...)`
- pointer cancellation count from `TouchTracker.cancel_all()`

### v0.6 Definition of Done

- frame timing and fixed-step tests pass
- lifecycle stress tests pass
- runtime service lifecycle tests pass
- scene resource cleanup tests pass
- touch filtering tests pass
- all v0.5 regressions remain green
- Python 3.9–3.12 CI remains green
- package wheel/sdist and `twine check` remain green

v0.6 completed with 998 passing automated tests, project health 142/142,
template validation 42/42, complete-game validation 54/54,
generated-project validation 90/90, release readiness 121/121,
pre-release audit 10/10, Python 3.9–3.12 CI, and package build/twine
validation.

## v0.7.0 — Content, Assets + Advanced Game Features

The v0.7 milestone expands content-driven game creation and reusable gameplay systems.

### Content and Asset Workflow

- `ContentManifest`, `ContentItem`, and `ContentManager`
- content lookup by id, kind, and tag
- image/audio/font/JSON/CSV/TXT content loading
- content asset validation
- opt-in JSON/CSV/TXT data cache
- `preload_data(...)` and cache management

### Reusable Game Content

- `Prefab` and `PrefabLibrary`
- JSON-driven reusable GameObject definitions
- top-level and nested-data prefab overrides
- `LevelSequence` ordered multi-level progression
- looping, previous/next/reset, and load helpers

### Advanced Reusable Game Features

- generic `ObjectPool` with capacity limits and acquire/release callbacks
- `SpriteAnimation.from_pattern(...)` for numbered frame sequences

### v0.7 Definition of Done

- content manifest tests pass
- prefab tests pass
- cached asset/preload tests pass
- level sequence tests pass
- object pooling tests pass
- sprite frame-pattern tests pass
- all v0.6 regressions remain green
- all six complete games remain valid
- Python 3.9–3.12 CI remains green
- package wheel/sdist and `twine check` remain green

v0.7 completed with 1032 passing automated tests, project health 155/155,
template validation 42/42, complete-game validation 54/54,
generated-project validation 90/90, release readiness 134/134,
pre-release audit 10/10, Python 3.9–3.12 CI, and package build/twine
validation.

## v0.8.0 — Build, Publishing + Production Hardening

The v0.8 milestone converts release guidance into executable production gates.

### Python Distribution Hardening

- `DistributionArtifact`, `DistributionReport`, and SHA-256 validation
- `hyperkit verify-dist`
- `hyperkit release-manifest`
- `hyperkit verify-clean-install`
- isolated fresh-wheel import and CLI verification
- `SHA256SUMS` and `release-manifest.json`
- CI package artifact upload after verification

### Publishing Automation

- manual `release-package.yml` workflow
- full automated release gates before publication
- TestPyPI and real PyPI destinations
- explicit real-PyPI confirmation
- GitHub OIDC / PyPI Trusted Publishing
- protected `testpypi` and `pypi` environments

### Android Production Hardening

- separate production profile preserving the historical API 35 debug defaults
- production target API 36
- NDK 29
- AAB release artifact
- python-for-android `develop` branch
- release-signing readiness validation
- `hyperkit android-release-doctor`
- protected signed Android production workflow
- artifact checksum generation

### v0.8 Definition of Done

- distribution artifact verification tests pass
- release checksum/manifest tests pass
- clean-install verification tests pass
- production Android configuration tests pass
- signing-readiness tests pass
- package publishing workflow regression tests pass
- Android production workflow regression tests pass
- normal CI performs clean-install package verification
- Python 3.9–3.12 CI remains green
- all v0.7 regressions remain green
- wheel/sdist and `twine check` remain green

v0.8 completed with 1069 passing automated tests, project health 165/165,
template validation 42/42, complete-game validation 54/54,
generated-project validation 90/90, release readiness 147/147,
pre-release audit 10/10, clean wheel installation, distribution verification,
release-manifest generation, and TestPyPI publishing-target validation.

## v0.9.0 — API Freeze + Public Beta

The v0.9 milestone freezes the intended top-level public API for HyperKit 1.0
and validates the SDK as a public beta.

### Public API Freeze

- package beta version `0.9.0b1`
- compatibility contract API `1.0`
- exact `FROZEN_PUBLIC_API` export set
- pinned export count and SHA-256 API fingerprint
- missing/unexpected/duplicate export rejection
- `hyperkit api-freeze-check`
- feature freeze for broad new public surface

### Compatibility and Deprecation Review

- API 1.0 major-version compatibility rules
- frozen API validation in CI and release readiness
- existing deprecation framework retained for future compatibility transitions
- incompatible public renames/removals blocked during beta without explicit freeze review

### Public Beta Validation

- Python 3.9–3.12 beta regression matrix
- full health/template/complete-game/generated-project/release/audit gates
- wheel/sdist build and `twine check`
- distribution manifest and clean-install verification
- optional TestPyPI publication through Trusted Publishing
- no real-PyPI publication from the dedicated beta workflow

### v0.9 Definition of Done

- exact frozen API tests pass
- compatibility contract 1.0 tests pass
- API fingerprint and export-count tests pass
- API freeze CLI tests pass
- public beta workflow tests pass
- all v0.8 regressions remain green
- Python 3.9–3.12 CI remains green
- wheel/sdist and `twine check` remain green
- clean-install verification remains green
- health/release/pre-release audits remain green

v0.9 completed locally with 1091 passing automated tests, project health
171/171, template validation 42/42, complete-game validation 54/54,
generated-project validation 90/90, release readiness 155/155,
pre-release audit 10/10, API contract `1.0`, 256 frozen exports, and the
pinned API fingerprint.

## v1.0.0 — Stable Release

The v1.0 milestone certifies the frozen SDK as the first stable HyperKit
release.

### Stable Release Certification

- package version exactly `1.0.0`
- package maturity `Production / Stable`
- compatibility contract remains API `1.0`
- frozen top-level export set remains exactly 256 names
- frozen API fingerprint remains unchanged
- `hyperkit stable-release-check`
- machine-readable stable-release certificate
- stable release documentation and version history

### Stable Package and Publication Gates

- full automated regression suite
- Python 3.9–3.12 CI
- API freeze validation
- health/template/complete-game/generated-project validation
- release readiness and pre-release audit
- wheel and source distribution build
- `twine check dist/*`
- distribution verification and SHA-256 release manifest
- clean environment installation
- protected `v1.0.0` stable-release workflow
- explicit confirmation before real-PyPI publication

### v1.0 Definition of Done

- package and module versions are synchronized at `1.0.0`
- stable package classifier is present
- frozen API contract and fingerprint remain unchanged
- stable-release certification tests pass
- stable workflow regression tests pass
- all v0.9 and earlier regressions remain green
- Python 3.9–3.12 CI remains green
- wheel/sdist and `twine check` pass
- clean-install verification passes
- stable release certificate is generated successfully
- final local release checkpoint passes

Real PyPI publication is a separate explicit release action after these
gates pass.

## Stable API Rule

The API `1.0` top-level surface is stable. Backward-compatible fixes can
ship in patch releases, and backward-compatible additions can ship in later
1.x minor releases. Incompatible public API changes require a future major
version.
