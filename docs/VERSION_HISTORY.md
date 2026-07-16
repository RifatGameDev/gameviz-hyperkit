# Version History

This document explains the version history and development direction of HyperKit.

---

## Current Package Identity

Package name:

gameviz-hyperkit

Import name:

hyperkit

CLI command:

hyperkit

---

## Version 0.1.0

Version `0.1.0` is the first working public development version of HyperKit.

It introduced the core SDK structure:

- package structure
- CLI command
- starter templates
- basic game loop structure
- scene system
- game object system
- score system
- UI helpers
- responsive canvas scaling
- local package build
- TestPyPI publishing test

This version was mainly focused on proving that HyperKit can work as a Python package and CLI-based starter kit for simple 2D mobile-style game prototypes.

---

## Unreleased Development Work

After `0.1.0`, HyperKit development focused on improving the SDK and making templates more useful for real prototypes.

Main areas improved:

- assets
- image rendering
- audio
- animation
- sprite animation
- particles
- camera shake
- scene transitions
- timers
- cooldowns
- input action mapping
- level data loading
- camera follow
- screen and world bounds
- progress bars
- helper-based template upgrades
- template quality tests
- release readiness tests
- documentation

---

## Versioning Plan

HyperKit currently uses simple semantic-style versioning:

MAJOR.MINOR.PATCH

Example:

0.1.0

Recommended meaning:

- PATCH update: bug fixes and small documentation updates
- MINOR update: new helpers, new templates, or meaningful SDK improvements
- MAJOR update: breaking changes in public API or project structure

---

## Suggested Next Version

The next package version should likely be:

0.2.0

Reason:

The current development work adds many new helper systems, template upgrades, tests, and documentation. This is more than a patch update.

---

## Release Stability Notes

HyperKit is still in early development.

For now, recommended publishing target:

GitHub + TestPyPI

Real PyPI publishing should wait until:

- helper APIs are stable
- template structure is stable
- documentation is complete
- generated projects are tested across key templates
- package build and metadata validation pass consistently
