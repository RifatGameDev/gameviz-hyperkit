# Template Validation

HyperKit includes a built-in template validation command:

`hyperkit validate-templates`

This command checks the built-in starter templates before a release or TestPyPI validation build.

---

## What It Checks

For each built-in template, the command checks:

- template folder exists
- `main.py` exists
- `README.md` exists
- main.py has valid Python syntax
- `main.py` imports HyperKit
- `main.py` has a game entry
- template files do not contain local machine paths


---

## Supported Templates

The validation currently checks:

- `tap_counter`
- `flappy_mini`
- `swipe_runner`
- `puzzle_game`
- `quiz_game`
- `simple_physics`

---

## Usage

Run from the repository root:

`hyperkit validate-templates`

Check a specific repository path:

`hyperkit validate-templates --path .`

---

## Recommended Release Flow

Run this command before TestPyPI validation builds:

`pytest`

`hyperkit health`

`hyperkit release-check`

`hyperkit pre-release-audit`

`hyperkit validate-templates`