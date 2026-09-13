| Version | Main goal                             | Current state |
| ------- | ------------------------------------- | ------------- |
| `0.1.2` | Public alpha baseline                 | ✅ Released    |
| `0.2.0` | Core SDK stabilization                | 🚧 Current    |
| `0.3.0` | Android & mobile workflow             | Not started   |
| `0.4.0` | Ads & analytics                       | Not started   |
| `0.5.0` | UI, audio, assets, save, game systems | Not started   |
| `0.6.0` | Complete example games                | Not started   |
| `0.7.0` | Developer tooling and CI              | Not started   |
| `0.8.0` | API stabilization                     | Not started   |
| `0.9.0` | Public beta                           | Not started   |
| `1.0.0` | Stable production SDK                 | Target        |



___________________________________________________________________________


# GameViz HyperKit — Fast Roadmap to 1.0.0

> Compressed roadmap designed to reduce branch/phase overhead while preserving the important technical work and release gates.

## Current State

- Public PyPI release: `0.1.2`
- Active development: `0.2.0.dev0`
- Phase 70 — Core API Foundation: complete
- Phase 71 — Runtime Lifecycle & SDK Context: implementation/tests complete; finish Git closeout
- Current automated test baseline: 491 passing tests

---

# Fast-Track Principle

Instead of creating one phase for every small subsystem, group related work into larger implementation phases.

Each implementation phase should still include:
- code
- automated tests
- documentation/changelog updates
- one feature branch
- one merge into `develop`

Each version still keeps a release-readiness phase before PyPI publication.

---

# 0.2.0 — Core SDK Foundation

## Phase 72 — Core Runtime Hardening

Combine all of these into one phase:

- Structured logging
- `hyperkit.toml` configuration loading and validation
- Runtime/platform detection
- Core error migration to `HyperKitError`
- Game/runtime lifecycle integration
- Deprecation helper
- Public API inventory and compatibility tests
- Documentation updates
- Regression tests

### Definition of done

- Runtime/context is integrated with the SDK
- Configuration is validated
- Logging is centralized
- Public API is explicitly tested
- Existing projects remain compatible
- Full test suite passes

## Phase 73 — Release HyperKit 0.2.0

- Final regression suite
- Python 3.9–3.12 validation
- Clean install test
- Build wheel and sdist
- `twine check`
- TestPyPI release candidate
- Clean candidate install
- Publish `0.2.0` to PyPI
- Tag `v0.2.0`
- GitHub release
- Merge release state back into `develop`

---

# 0.3.0 — Android & Mobile

## Phase 74 — Android + Mobile Workflow

Combine:

- Android project configuration
- Buildozer/SDK/NDK checks
- `hyperkit build android`
- Debug APK workflow
- Mobile input improvements
- Tap/swipe/hold foundation
- Responsive layout helpers
- Safe-area handling
- Device testing workflow
- Android diagnostics
- Release-build/signing guidance

### Definition of done

- A generated HyperKit project can be configured for Android
- Debug APK can be built
- Core templates can run on a real Android device
- Mobile input/layout behavior is validated

## Phase 75 — Release HyperKit 0.3.0

- Android smoke tests
- Full automated regression
- TestPyPI RC
- PyPI `0.3.0`
- Tag and GitHub release

---

# 0.4.0 — Monetization + Core Game Systems

## Phase 76 — Ads, Analytics, Assets, Audio, Save & UI

Combine:

### Service/provider foundation
- Provider interfaces through `SDKContext`
- Provider lifecycle
- Availability checks
- Desktop/mock providers

### Ads
- `AdsManager`
- Banner API
- Interstitial API
- Rewarded API
- AdMob Android provider
- Development/test mode
- Load/show/error callbacks

### Analytics
- `AnalyticsManager`
- Event tracking
- Screen/session tracking
- First provider integration

### Game systems
- Asset preloading/cache improvements
- Music/SFX channels
- Volume/mute controls
- Save namespaces and migrations
- Save corruption recovery
- UI panels/buttons/menus
- Scene stack/restart helpers
- Pause/game-over/session flow

### Definition of done

- Ads and analytics use the same provider architecture
- AdMob works in Android test mode
- Core persistence/audio/UI systems are suitable for complete small games
- Full regression suite passes

## Phase 77 — Release HyperKit 0.4.0

- Android monetization QA
- Full regression
- TestPyPI RC
- PyPI `0.4.0`
- Tag and GitHub release

---

# 0.5.0 — Complete Games + Developer Tooling

## Phase 78 — Production Examples & Tooling

Combine:

### Complete games
- Complete Tap game
- Complete Flappy-style game
- Complete Endless Runner
- Complete Puzzle game
- Complete Quiz game
- Complete Simple Shooter

Each game should demonstrate, where relevant:
- menu
- gameplay
- game-over/restart
- save data
- audio
- UI
- Android controls
- ads/analytics integration

### Developer tooling
- Improved `hyperkit doctor`
- Improved `hyperkit validate`
- Better CLI errors/output
- Debug/FPS overlay
- Runtime diagnostics
- Production-ready starter templates
- GitHub Actions
- Python 3.9–3.12 matrix
- Build/package validation

### Definition of done

- HyperKit can build several complete small games
- New users can create, validate, debug, and package projects with CLI tools
- CI automatically protects the package

## Phase 79 — Release HyperKit 0.5.0

- Desktop QA
- Android QA
- Example-game QA
- TestPyPI RC
- PyPI `0.5.0`
- Tag and GitHub release

---

# 0.9.0 — API Freeze / Public Beta

> Skip unnecessary intermediate minor releases after `0.5.0` if the SDK is ready. Semantic versioning does not require publishing every minor number.

## Phase 80 — API Stabilization + Beta

Combine:

- Review all public imports
- Normalize naming
- Finalize package/module structure
- Freeze `hyperkit.toml` candidate schema
- Finalize exception hierarchy
- Finalize runtime/provider lifecycle
- Deprecate accidental/obsolete APIs
- Complete API documentation
- Complete Android documentation
- Complete ads/analytics documentation
- Fresh-user installation test
- Full template QA
- Full complete-game QA
- Python 3.9–3.12 matrix
- Android device QA
- Performance/reliability smoke tests
- Feature freeze

### Definition of done

- No planned breaking API changes remain
- New users can install and build a game from docs alone
- Android and monetization workflows are validated
- Only bug fixes are allowed after beta freeze

## Phase 81 — Release HyperKit 0.9.0 Beta

- Final beta regression
- TestPyPI RC
- Publish `0.9.0` to PyPI
- Tag and GitHub release
- Collect and fix beta issues

---

# 1.0.0 — Stable

## Phase 82 — 1.0 Release Candidate

Combine:

- Resolve beta blockers
- Freeze public API
- Freeze config schema
- Freeze runtime lifecycle
- Freeze provider contracts
- Define 1.x compatibility promise
- Build `1.0.0rc1`
- Full automated tests
- Full template QA
- Full example-game QA
- Clean install QA
- Android build QA
- AdMob test-mode QA
- Documentation audit

## Phase 83 — Publish HyperKit 1.0.0

Final audit:

- No release-blocking issues
- Correct package metadata
- README/changelog/version history complete
- License and public URLs correct
- No local paths, secrets, or tokens
- Wheel and sdist pass `twine check`
- Clean `main` branch
- Publish `gameviz-hyperkit==1.0.0`
- Clean-install from real PyPI
- Verify CLI
- Verify project generation
- Tag `v1.0.0`
- Create GitHub release
- Merge `main` back into `develop`

---

# Compressed Version Tracker

| Version | Main Goal | Phases |
| --- | --- | --- |
| `0.1.2` | Public alpha baseline | Released |
| `0.2.0` | Core SDK foundation | 72–73 |
| `0.3.0` | Android & mobile | 74–75 |
| `0.4.0` | Ads, analytics & game systems | 76–77 |
| `0.5.0` | Complete games & developer tooling | 78–79 |
| `0.9.0` | API freeze & public beta | 80–81 |
| `1.0.0` | Stable SDK | 82–83 |

---

# Immediate Path

- [x] Phase 70 — Core API Foundation
- [~] Phase 71 — Runtime Lifecycle & SDK Context
- [ ] Phase 72 — Core Runtime Hardening
- [ ] Phase 73 — Release `0.2.0`
- [ ] Phase 74 — Android + Mobile Workflow
- [ ] Phase 75 — Release `0.3.0`
- [ ] Phase 76 — Ads, Analytics, Assets, Audio, Save & UI
- [ ] Phase 77 — Release `0.4.0`
- [ ] Phase 78 — Production Examples & Tooling
- [ ] Phase 79 — Release `0.5.0`
- [ ] Phase 80 — API Stabilization + Beta
- [ ] Phase 81 — Release `0.9.0`
- [ ] Phase 82 — `1.0.0` Release Candidate
- [ ] Phase 83 — Publish `1.0.0`

---

# Rules for Fast Development

1. One branch per large implementation phase, not per tiny subsystem.
2. Write tests while implementing the phase, not as a separate later phase.
3. Update docs/changelog before closing the same phase.
4. Run focused tests during development; run the full suite before merge.
5. Keep release validation separate from feature work.
6. Do not skip Android device QA, monetization test-mode QA, API freeze, or clean PyPI-install validation.
7. Skip unnecessary intermediate version numbers when there is no release value in publishing them.
