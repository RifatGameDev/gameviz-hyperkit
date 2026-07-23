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

No unreleased changes are currently documented.

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