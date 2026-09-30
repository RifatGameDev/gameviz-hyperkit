# Changelog

All notable changes to GameViz HyperKit are documented in this file.

HyperKit currently uses the following change categories:

- Added
- Changed
- Fixed
- Documentation
- Internal
- Validation

---

## Unreleased

Current development version: ``0.8.0.dev0``.

### Added

- v0.8 Build, Publishing + Production Hardening milestone.
- Distribution artifact discovery, version validation, size validation, and SHA-256 hashing.
- `hyperkit verify-dist`, `hyperkit release-manifest`, and `hyperkit verify-clean-install`.
- `SHA256SUMS` and machine-readable `release-manifest.json` generation.
- Fresh virtual-environment wheel installation and CLI verification.
- Manual gated TestPyPI/PyPI Trusted Publishing workflow.
- Separate store-oriented Android production profile targeting API 36 with NDK 29, AAB output, and p4a `develop`.
- Android release-signing readiness checks that never print secret values.
- `hyperkit android-release-doctor`.
- Protected signed Android production AAB workflow.
- v0.8 release-build, production-Android, CLI, and workflow regression coverage.
- v0.7 Content, Assets + Advanced Game Features milestone.
- `ContentManifest`, `ContentItem`, and `ContentManager`.
- Tagged and kind-based content lookup with asset validation.
- `Prefab` and `PrefabLibrary` for JSON-driven reusable GameObjects.
- Opt-in cached JSON/CSV/TXT loading plus `preload_data(...)`.
- `LevelSequence` for ordered multi-level progression.
- Generic `ObjectPool` with capacity and lifecycle callbacks.
- `SpriteAnimation.from_pattern(...)` for numbered frame sequences.
- v0.7 content, prefab, pool, level-sequence, asset-cache, and sprite regression coverage.
- v0.6 Mobile Production Runtime + Performance milestone.
- `PerformanceMode` and `PerformanceProfile` mobile runtime presets.
- `FrameTimeController` frame-hitch protection.
- `FixedStepClock` bounded fixed-step simulation support.
- `Game.performance_stats()` runtime timing telemetry.
- Scene lifecycle hooks for pause, background, resume, and stop.
- Scene resource cleanup through `release_resources()`.
- Runtime lifecycle propagation to all registered SDK services.
- Touch move-noise filtering with `move_min_distance`.
- Runtime safe-area updates through `Game.update_safe_area()` and `MobileDisplayProfile.with_safe_area()`.
- v0.6 mobile performance, lifecycle, cleanup, and input regression coverage.
- v0.5 Complete Games + Developer Tooling milestone.
- `RuntimeDiagnostics` and immutable `RuntimeSnapshot` performance data.
- Optional `DebugOverlay` for FPS, frame-time, and dropped-frame feedback.
- Complete-game validator for all six built-in game templates.
- `hyperkit diagnostics` project diagnostics command.
- `hyperkit validate-complete-games` CLI command.
- General Python 3.9–3.12 GitHub Actions CI workflow.
- v0.5 complete-game, diagnostics, CLI, and CI regression coverage.
- Phase 75 SDK completion audit and hardening from the v0.4 closeout.
- Expanded physics world, collision manifolds, body/material, trigger, layer, and mask support.
- Stronger geometry, camera, bounds, layout, persistence, state, transition, timer, level, input, audio, UI, particle, animation, sprite, asset, and game-system helpers.

### Changed

- Package development version advanced to `0.8.0.dev0`.
- Normal CI now validates built distributions, writes artifact manifests, performs fresh-wheel installation checks, and uploads the verified distribution bundle.
- Production Android configuration is intentionally separate from the historically validated API 35 development/debug defaults.
- Release publication is now workflow-gated instead of relying on manual upload commands.
- v0.7 advanced the package development version to `0.7.0.dev0`.
- Game content can now be described and loaded through reusable manifests and prefabs instead of only direct code references.
- Data-heavy games can opt into cached/preloaded JSON, CSV, and text assets.
- `Game` now clamps large frame deltas before scene updates.
- `Game.stop()` is idempotent and Kivy shutdown now uses the stop lifecycle instead of treating shutdown as backgrounding.
- Active pointers are cancelled when the game is paused, backgrounded, or stopped.
- Scene changes release the previous scene before starting the replacement.
- `AudioManager` now responds to runtime pause/background/resume/stop lifecycle events.
- Runtime services registered under multiple names are notified only once per lifecycle event.
- Package development version advanced to `0.6.0.dev0`.
- Tap Counter now has a complete round, game-over/completion state, and restart flow.
- Built-in templates are treated as complete small-game starters rather than prototype-only examples.
- v0.5 advanced the package development version to `0.5.0.dev0`.
- Simple Physics uses the reusable PhysicsWorld architecture.
- Public development documentation distinguishes the latest published PyPI release from the active development version.
- The authoritative roadmap now follows v0.5 through v1.0 instead of skipping directly from v0.4 to release-candidate work.

### Validation

- v0.7 closeout finished with 1032 passing automated tests before v0.8 development started.
- v0.7 closeout passed health 155/155, templates 42/42, complete games 54/54, generated projects 90/90, release readiness 134/134, pre-release audit 10/10, Python 3.9–3.12 CI, and package build/twine validation.
- v0.6 closeout finished with 998 passing automated tests before v0.7 development started.
- v0.6 closeout passed health 142/142, templates 42/42, complete games 54/54, generated projects 90/90, release readiness 121/121, pre-release audit 10/10, Python 3.9–3.12 CI, and package build/twine validation.
- v0.5 closeout finished with 973 passing automated tests before v0.6 development started.
- v0.5 closeout passed complete-game validation 54/54, generated-project validation 90/90, release readiness 115/115, pre-release audit 10/10, Python 3.9–3.12 CI, and package build/twine validation.
- v0.4 closeout finished with 949 passing automated tests before v0.5 development started.
- v0.4 closeout reports passed: health 133/133, templates 42/42, generated projects 90/90, release readiness 117/117, pre-release audit 10/10.
- Phase 75 regression suite reached 919 passing tests before documentation synchronization.
- API compatibility contract remains `0.2` while package development continues at `0.8.0.dev0`.

---

## 0.2.0 - 2026-09-13

### Added

- Phase 70 core API foundation.
- Base `HyperKitError` exception hierarchy.
- SDK configuration foundation with `SDKConfig`.
- Public API compatibility versioning.
- `API_VERSION`, `get_api_version`, `is_api_compatible`, and `require_api_version`.
- Regression tests for the new core API foundation.
- Phase 71 runtime lifecycle and SDK context foundation.
- `RuntimeState` lifecycle model.
- `SDKContext` for configuration, services, and runtime metadata.
- Runtime service registry.
- Default SDK context management.
- Runtime lifecycle regression tests.
- Phase 72 core runtime hardening.
- Structured HyperKit logging.
- Runtime platform and environment detection.
- Versioned `hyperkit.toml` project configuration loading.
- HyperKit deprecation framework.
- Runtime lifecycle integration for games.
- Stable `0.2` public API contract.
- Public API regression validation.
- Runtime environment metadata support.
- Project configuration schema versioning.
- Game runtime start and stop helpers.

### Changed

- Package version advanced from `0.1.2` to `0.2.0`.
- Core SDK architecture prepared for the HyperKit `0.2.0` release.
- Runtime services now share a common SDK context and lifecycle foundation.
- Phase 68 release-readiness tests preserve the historical `0.1.1` release evidence without hard-coding the active package version.
- Public release documentation updated for HyperKit `0.2.0`.
- Public API compatibility checks expanded for the `0.2` SDK contract.

### Internal

- Completed the HyperKit `0.2.0` core SDK development cycle.
- Added runtime, logging, environment, lifecycle, project configuration, deprecation, and API-contract modules.
- Added Phase 70, Phase 71, and Phase 72 regression coverage.

### Validation

- Public API contract validation passed.
- Phase 72 completion tests passed.
- Full automated regression suite reached 529 passing tests before release preparation.
- Package supports Python 3.9 through Python 3.12.
- Wheel and source distribution validation is required before publication.

---

## 0.1.2 - 2026-07-23

### Changed

- Updated the public README for the current PyPI release workflow.
- Improved PyPI installation instructions.
- Improved the quick-start workflow.
- Standardized template names using dash-style CLI examples.
- Added Python version support information.
- Corrected the public GitHub repository links.
- Improved package identity and project-link documentation.
- Simplified the public development and build instructions.

### Fixed

- Removed outdated TestPyPI-only release-status information.
- Corrected README command formatting around `cd my-game`.
- Restored the conditional `tomli` dependency for Python versions below 3.11.
- Corrected repository URLs from the old `gameviz-rifat` path to `RifatGameDev`.
- Corrected the release branch documentation state.

### Documentation

- Added clearer PyPI installation verification commands.
- Added a public project-links section.
- Improved CLI command documentation.
- Improved template aliases documentation.
- Improved the limitations and roadmap sections.
- Added a contributing section.

### Validation

- Package version synchronized between `pyproject.toml` and `hyperkit.__version__`.
- Public README tests updated for version `0.1.2`.
- Full automated test suite required before publication.
- Wheel and source distribution validation required before publication.

---

## 0.1.1 - 2026-07-22

### Added

- Six polished built-in starter templates:
  - Tap Counter
  - Flappy Mini
  - Swipe Runner
  - Puzzle Game
  - Quiz Game
  - Simple Physics
- Complete manual runtime QA evidence for every built-in template.
- Generated-project validation.
- Strict release-evidence validation.
- Installed-package validation.
- Project health report command.
- Release readiness command.
- Final pre-release audit command.
- Runtime evidence tracker.
- Template-specific QA result tests.

### Changed

- Improved template gameplay feedback.
- Improved restart behavior across templates.
- Improved score and high-score persistence.
- Improved CLI project generation.
- Improved CLI error handling.
- Improved generated-project documentation.
- Improved runtime stability across all six templates.
- Added vertical pipe-gap variation to Flappy Mini.
- Improved release preparation and package validation workflows.

### Fixed

- Added Python 3.9 and Python 3.10 TOML compatibility.
- Added a conditional `tomli` dependency for Python versions below 3.11.
- Fixed the Python 3.10 startup failure caused by direct `tomllib` imports.
- Fixed local-machine paths appearing in committed QA evidence.
- Fixed template documentation consistency issues.
- Fixed release-readiness validation coverage.

### Validation

- Validated through TestPyPI using release candidate `0.1.1rc2`.
- Verified using clean installed-package environments.
- Verified on Python 3.10 and Python 3.11.
- All six templates passed manual runtime QA.
- Published publicly on PyPI as `0.1.1`.

---

## 0.1.1rc2 - TestPyPI Release Candidate

### Fixed

- Added `tomli` as a conditional dependency for Python versions below 3.11.
- Added a compatibility fallback from `tomllib` to `tomli`.
- Fixed `ModuleNotFoundError` on Python 3.9 and Python 3.10.
- Corrected Python compatibility metadata.

### Validation

- Tested with Python 3.10.
- Tested with Python 3.11.
- Verified CLI startup.
- Verified template listing.
- Verified generated-project creation.
- Verified installed-package isolation from local source code.

### Notes

- This release candidate superseded `0.1.1rc1`.
- It became the validated source for stable release `0.1.1`.

---

## 0.1.1rc1 - TestPyPI Release Candidate

### Added

- First complete release-candidate build.
- Six-template installed-package validation.
- Runtime QA certification.
- Clean TestPyPI installation validation.
- Release-candidate readiness evidence.

### Validation

- Wheel build passed.
- Source distribution build passed.
- Twine validation passed.
- TestPyPI upload passed.
- Clean Python 3.11 installation passed.

### Notes

- A Python 3.10 compatibility issue was discovered.
- The compatibility issue was corrected in `0.1.1rc2`.

---

## 0.1.1.dev1 - TestPyPI Validation Build

### Added

- Initial TestPyPI upload validation.
- Clean package-installation validation.
- Final pre-release audit command.
- Release readiness command.
- Project health report command.
- Template generation validation.

### Notes

- This version was used only for TestPyPI workflow validation.
- It was not intended for real PyPI publication.

---

## 0.1.0

### Added

- Initial HyperKit package structure.
- `hyperkit` Python import package.
- `hyperkit` command-line interface.
- Project generation with `hyperkit new`.
- Template listing with `hyperkit list-templates`.
- Project validation with `hyperkit validate`.
- Package information with `hyperkit info`.
- Environment checks with `hyperkit doctor`.
- Core `Game` system.
- Core `Scene` system.
- Core `GameObject` system.
- State-management helpers.
- Score and high-score helpers.
- Save and persistence helpers.
- Tap and click input.
- Swipe input.
- Collision helpers.
- Basic physics helpers.
- Text and UI helpers.
- Responsive virtual canvas scaling.
- Asset-loading helpers.
- Image-rendering support.
- Audio helpers.
- Animation helpers.
- Particle helpers.
- Camera helpers.
- Timer helpers.
- Screen-bound helpers.
- Progress-bar helpers.

### Core Helpers

- Particle helper
- Camera shake helper
- Progress bar helper
- Input action mapping helper
- Level data loading helper

### Templates

- `tap_counter`
- `flappy_mini`
- `swipe_runner`
- `puzzle_game`
- `quiz_game`
- `simple_physics`

### Internal

- Initial automated test suite.
- Example demonstration projects.
- Initial packaging configuration.
- Initial TestPyPI package workflow.
