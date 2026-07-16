# Release Build Automation

HyperKit includes a release readiness command:

`hyperkit release-check`

This command checks whether the package looks ready for a release preparation step.

## What It Checks

- project health report
- README.md
- CHANGELOG.md
- pyproject.toml
- required documentation files
- required release test files
- package identity in README
- version notes in CHANGELOG
- build command guidance
- twine check command guidance

## Usage

Run from the package repository root:

`hyperkit release-check`

Check a specific path:

`hyperkit release-check --path .`

## Manual Release Commands

After `hyperkit release-check` passes, run:

`pytest`

`python -m build`

`twine check dist/*`

## Current Publishing Rule

For now, HyperKit should remain on GitHub and TestPyPI.

Do not publish to real PyPI until the SDK and templates are more stable.