# Production Template Polish Checklist

This checklist defines what each HyperKit template should satisfy before being considered production-quality for a stable public release.

HyperKit is currently an early SDK preview. These checks help guide template improvements toward a future stable version.

---

## Purpose

A production-quality template should be:

- easy for beginners to understand
- visually clear
- simple to run
- free from local machine paths
- documented well
- tested through generated project smoke tests
- useful as a starting point for real prototypes

---

## Template Coverage

This checklist applies to all built-in templates:

- `tap_counter`
- `flappy_mini`
- `swipe_runner`
- `puzzle_game`
- `quiz_game`
- `simple_physics`

---

## Required Template Files

Each template should include:

- `main.py`
- `README.md`
- starter asset folders where needed
- clean example code
- no local development paths
- no temporary debug files

---

## Code Quality Checklist

Each template should:

- use clear class names
- use readable variable names
- keep game logic simple
- avoid unnecessary complexity
- avoid hard-coded local paths
- avoid unused imports
- avoid large duplicated code blocks
- use HyperKit helper systems where useful
- include a clear `Game(...).set_scene(...).run()` entry point

---

## Gameplay Checklist

Each template should provide:

- a clear starting state
- visible player feedback
- simple win, score, or progress logic where relevant
- restart or replay behavior where useful
- clear input behavior
- readable labels or instructions
- stable behavior when run multiple times

---

## Visual Polish Checklist

Each template should aim to include:

- clean layout
- readable text
- consistent spacing
- understandable colors
- simple visual feedback
- basic UI clarity
- optional screenshots or GIF documentation

---

## Documentation Checklist

Each template README should explain:

- what the template does
- how to run it
- main controls
- main files
- how to customize it
- what HyperKit helpers it demonstrates

---

## Media Checklist

Each template should eventually include:

- screenshot preview
- short demo GIF
- thumbnail image
- media README

Expected media files:

- `screenshot.png`
- `demo.gif`
- `thumbnail.png`

---

## Testing Checklist

Before a template is considered stable, it should pass:

- syntax tests
- generated project smoke tests
- template validation command
- release readiness checks
- final pre-release audit checks

Recommended commands:

`pytest`

`hyperkit validate-templates`

`hyperkit health`

`hyperkit release-check`

`hyperkit pre-release-audit`

---

## Stable Release Target

A template can be considered stable-ready when:

- it runs successfully from a generated project
- its README is clear
- its code is beginner-friendly
- it uses HyperKit systems correctly
- it has no broken paths or temporary files
- it has visual media documentation
- it passes all validation checks

---

## Current Status

This checklist is a planning and quality guide.

Actual template polishing will happen in later phases.