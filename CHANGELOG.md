# Changelog

All notable changes to HyperKit will be documented in this file.

HyperKit follows a simple version history format for now:

- Added
- Changed
- Fixed
- Documentation
- Internal

---

## Unreleased

### Added

- Helper-based starter template upgrades.
- Template quality checklist tests.
- Release readiness checklist and package metadata validation.
- Template helper usage documentation.
- Screen bounds and world bounds helpers.
- Progress bar helper.
- UI progress bar helper.
- Camera follow helper.
- Level data loading helper.
- Input action mapping helper.
- Timer and cooldown helpers.
- Scene transition helper.
- Camera shake helper.
- Particle helper.
- Sprite animation helper.
- Animation helper.
- Audio playback helper.
- Image rendering support.
- Asset loading helper.

### Changed

- Upgraded `tap_counter` template with helper-based visual feedback.
- Upgraded `flappy_mini` template with helper-based gameplay feedback.
- Upgraded `swipe_runner` template with helper-based gameplay feedback.
- Upgraded `puzzle_game` template with helper-based puzzle feedback.
- Upgraded `quiz_game` template with helper-based quiz feedback.
- Upgraded `simple_physics` template with helper-based physics feedback.
- Improved template README files with gameplay and helper usage sections.
- Improved documentation structure for templates and helper systems.

### Fixed

- Template README consistency issues.
- Template helper documentation coverage.
- Package release readiness validation coverage.

### Documentation

- Added `docs/TEMPLATE_HELPERS.md`.
- Added `docs/TEMPLATE_QUALITY_CHECKLIST.md`.
- Added `docs/RELEASE_READINESS_CHECKLIST.md`.
- Added `docs/VERSION_HISTORY.md`.
- Added this `CHANGELOG.md`.

---

## 0.1.0

### Added

- Initial HyperKit package structure.
- `hyperkit` import package.
- `hyperkit` CLI command.
- Project generation with `hyperkit new`.
- Template listing with `hyperkit list-templates`.
- Project validation with `hyperkit validate`.
- Package information with `hyperkit info`.
- Doctor command with `hyperkit doctor`.
- Core `Game`, `Scene`, and `GameObject` structure.
- State management helper.
- Score and high-score helper.
- UI helpers including buttons and text labels.
- Responsive virtual canvas scaling.
- Starter templates:
  - `tap_counter`
  - `flappy_mini`
  - `swipe_runner`
  - `puzzle_game`
  - `quiz_game`
  - `simple_physics`
- Example demos.
- TestPyPI package publishing test.
