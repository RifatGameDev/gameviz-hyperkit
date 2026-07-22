# Generated Project Validation - Phase 55

HyperKit includes generated project validation for all polished built-in templates.

The command generates each template and validates its project structure without starting the graphical game window.

---

## Command

Run:

`hyperkit validate-generated-projects`

By default, temporary generated projects are automatically cleaned up after validation.

For debugging, a custom work directory can be provided:

`hyperkit validate-generated-projects --work-path generated-validation`

---

## Templates Validated

The command validates:

- tap_counter
- flappy_mini
- swipe_runner
- puzzle_game
- quiz_game
- simple_physics

---

## Validation Checks

For every generated project, the command checks:

- project generation succeeds
- project directory exists
- main.py exists
- hyperkit.toml exists
- assets directory exists
- main.py has valid Python syntax
- main.py imports HyperKit
- main.py has a game entry
- hyperkit.toml contains valid TOML
- generated files contain no forbidden local paths

---

## Runtime Testing

This command does not start the Kivy game window.

Interactive gameplay and visual behavior should still be tested manually using:

`python main.py`

Automated validation focuses on generated project structure, syntax, metadata, and portability.

---

## Recommended Validation Flow

Run:

`pytest`

`hyperkit validate-templates`

`hyperkit validate-generated-projects`

`hyperkit health`

`hyperkit release-check`

`hyperkit pre-release-audit`

---

## Current Status

All six polished templates are now covered by generated project validation.

This provides stronger protection against broken template generation before beta or stable release.