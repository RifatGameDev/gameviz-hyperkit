# GameViz HyperKit — Roadmap to 1.0

HyperKit is now in completion and stabilization work rather than broad
feature discovery.

## Current State

- Latest published PyPI release: `0.2.0`
- Active development version: `0.4.0.dev0`
- Public compatibility contract: API `0.2`
- Active development branch:
  `feature/phase74-ads-analytics-game-systems`
- Current focus: Phase 75 SDK completion audit and hardening
- Automated regression baseline before the current documentation-sync phase:
  919 passing tests

## Completed Foundations

The current development line already includes:

- runtime context and lifecycle
- project configuration and compatibility helpers
- Android/mobile workflow foundations
- safe-area and viewport helpers
- provider-based ads architecture
- AdMob Android test-mode integration
- provider-based analytics architecture
- Firebase Analytics Android integration
- game session and progression systems
- scene and game-object systems
- shape-aware collision
- physics bodies, materials, triggers, layers, and masks
- geometry and vector helpers
- camera follow, camera shake, and bounds helpers
- UI labels, buttons, interaction routing, and progress bars
- canvas scaling and coordinate conversion
- save/persistence helpers
- score/high-score helpers
- timers and cooldowns
- level loading and object creation
- input action mapping
- audio lifecycle helpers
- tween and color animation
- sprite animation
- particle effects
- asset loading and discovery
- six built-in templates
- template validation and release evidence tooling
- project health, release readiness, and pre-release audit tooling

## Phase 75 — SDK Completion Audit

Phase 75 is a focused hardening pass across the complete SDK.

Completed hardening areas include:

- physics and collision
- GameObject collider behavior
- geometry/vector math
- UI button interaction
- camera and bounds
- save persistence
- canvas/layout scaling
- game state and scene transitions
- timers and cooldowns
- level system
- input action mapping
- audio
- progress bar UI
- particles
- animation/tween
- sprite animation
- assets
- game session and progression systems

Current closeout work:

- documentation synchronization
- template documentation alignment
- release/audit metadata cleanup
- public API review
- subsystem integration audit
- template regression validation
- Android/device smoke validation
- package build and clean-install validation

## Release Gates Before 1.0

HyperKit should not be called stable until all of these gates pass:

1. Full automated regression suite is green.
2. Built-in templates generate and validate successfully.
3. All six templates receive final runtime QA.
4. Android debug-build workflow is validated.
5. Core templates are smoke-tested on a physical Android device.
6. AdMob test-mode integration is validated without production ad IDs.
7. Firebase Analytics integration is validated in a real Android runtime.
8. Public imports and compatibility behavior are audited.
9. README, roadmap, changelog, examples, and template docs are synchronized.
10. Wheel and source distribution build successfully.
11. `twine check dist/*` passes.
12. A clean environment can install the built package and use the CLI.
13. A release candidate passes final QA.
14. The stable release is installed again from real PyPI and verified.

## Version Strategy

HyperKit does not need to publish every historical roadmap minor version.
Development can move directly through release-candidate milestones when the
required quality gates are satisfied.

| Version | Purpose | State |
| --- | --- | --- |
| `0.1.x` | Initial public alpha and template baseline | Released |
| `0.2.0` | Core SDK/runtime foundation | Released |
| `0.4.0.dev0` | Integrated mobile, ads, analytics, game systems, and completion hardening | Active development |
| next RC | End-to-end release candidate | Planned |
| `1.0.0` | Stable focused 2D mobile-game SDK | Target |

## 1.0 Scope

The 1.0 target is a focused SDK capable of producing complete small 2D
mobile games in categories such as:

- tap games
- flappy-style games
- swipe games
- endless runners
- simple shooters
- simple physics games
- puzzle games
- educational quiz games
- other small hypercasual and hybrid-casual designs

The target includes the reusable systems needed to finish those games:
runtime, rendering helpers, input, physics, UI, audio, persistence, game
state, templates, Android workflow, ads, analytics, and release tooling.

The 1.0 target does not include a general-purpose 3D engine or an editor
intended to replace Unity, Unreal Engine, or Godot.

## Feature Freeze Rule

After the Phase 75 completion checklist reaches zero:

- do not add unrelated feature categories
- fix integration and compatibility issues
- update documentation
- run release validation
- prepare the release candidate

New feature ideas that are not required for the stable scope should move to
post-1.0 planning.
