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
- synchronized package version metadata
- active development version in README and CHANGELOG
- Python module CLI entry point
- current roadmap completion state
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

Then perform clean-install verification from a fresh virtual environment using the built wheel before release.

## Publishing Rule

Use TestPyPI when release-candidate packaging validation is useful.

A stable release may be published to real PyPI only after the full release gates pass, including automated tests, template validation, package build validation, `twine check`, clean-install verification, and required Android/provider QA for the target release.
