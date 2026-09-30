# GameViz HyperKit — Version History

This document summarizes the public releases and active development
milestones of HyperKit.

## Current Package Identity

- Package name: `gameviz-hyperkit`
- Import name: `hyperkit`
- CLI command: `hyperkit`
- Latest published PyPI release: `0.2.0`
- Active development version: `0.9.0b1`
- Public compatibility contract: API `1.0`

## Development Roadmap

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
          ← ACTIVE DEVELOPMENT
   ↓
v1.0.0  Stable Release
```

## 0.9.0b1 — Active Public Beta

Focus: API Freeze + Public Beta.

Current work includes:

- frozen intended 1.0 top-level public API
- API compatibility contract `1.0`
- exact export validation
- pinned public export count
- deterministic SHA-256 API fingerprint
- `hyperkit api-freeze-check`
- Python 3.9–3.12 public-beta validation workflow
- optional TestPyPI beta publication through Trusted Publishing
- feature freeze for broad new public API additions

## 0.8.0 — Development Milestone

Focus: Build, Publishing + Production Hardening.

Delivered:

- distribution artifact verification
- SHA-256 checksum and release-manifest generation
- isolated clean-install wheel verification
- gated TestPyPI/PyPI Trusted Publishing
- controlled build inputs
- store-oriented Android API 36 / AAB production profile
- Android signing readiness validation
- protected signed Android release workflow

The v0.8 closeout reached 1069 passing automated tests and completed local
distribution, clean-install, and TestPyPI target validation.

## 0.7.0 — Development Milestone

Focus: Content, Assets + Advanced Game Features.

Delivered:

- structured content manifests
- content lookup by id, kind, and tags
- reusable JSON-driven prefabs
- cached/preloaded JSON, CSV, and text data
- ordered multi-level progression
- reusable object pooling
- sprite frame-pattern generation
- content validation CLI

The v0.7 closeout reached 1032 passing automated tests.

## 0.6.0 — Development Milestone

Focus: Mobile Production Runtime + Performance.

Delivered:

- mobile performance profiles
- frame-hitch delta protection
- bounded fixed-step simulation
- runtime performance statistics
- pause/background/resume/stop lifecycle hardening
- registered-service lifecycle propagation
- lifecycle-aware audio behavior
- scene resource cleanup
- runtime safe-area updates
- touch move-noise filtering
- viewport-aware touch routing

The v0.6 closeout reached 998 passing automated tests.

## 0.5.0 — Development Milestone

Focus: Complete Games + Developer Tooling.

Delivered:

- six complete built-in small-game loops
- complete-game validation
- project diagnostics CLI
- runtime diagnostics and debug overlay
- Python 3.9–3.12 CI
- package build and `twine check` validation

The v0.5 closeout reached 973 passing automated tests.

## 0.4.0 — Development Milestone

Focus: Ads + Analytics + Game Systems.

Delivered foundations include:

- provider-based Ads architecture
- AdMob Android test-mode integration
- provider-based Analytics architecture
- Firebase Analytics Android integration
- game sessions and progression
- broad SDK subsystem hardening
- public API, CLI, health, release, and generated-project validation

The v0.4 closeout reached 949 passing automated tests.

## 0.3.0 — Development Milestone

Focus: Android + Mobile.

Delivered foundations include:

- Android configuration and build workflow
- mobile display profiles
- safe-area and viewport support
- runtime lifecycle integration
- touch/multi-pointer foundations
- Android environment diagnostics

## 0.2.0 — Published Release

Version `0.2.0` is the latest published PyPI release.

It introduced the core SDK/runtime foundation, including:

- SDK context and runtime lifecycle
- configuration and logging
- environment detection
- project configuration
- deprecation framework
- API compatibility helpers
- stable API `0.2` compatibility contract

## 0.1.x — Initial Public Releases

The initial public line established:

- Python package structure
- HyperKit CLI
- six starter templates
- scene and game-object systems
- input, score, persistence, physics, UI, assets, audio, animation,
  particles, camera, timers, levels, and other early helpers
- TestPyPI validation
- clean-install validation
- initial PyPI publication

## Versioning Direction

HyperKit uses semantic-style package versions:

`MAJOR.MINOR.PATCH`

Development versions may use suffixes such as `.dev0`, and release
candidates may use `rc1`, `rc2`, and so on.

The package version and public compatibility contract are intentionally
separate. At the v0.9 public-beta stage the package is `0.9.0b1`, while
the compatibility contract is frozen at API `1.0`.

The intended top-level public API for stable 1.0 is now frozen. The
remaining roadmap work is beta validation and stable-release certification,
not broad public API expansion.
