# Final Pre-release Audit

HyperKit includes a final audit command:

`hyperkit pre-release-audit`

This command performs the last safe check before preparing a build or release candidate.

## What It Checks

- release readiness report
- project root files
- README.md
- pyproject.toml
- temporary cleanup scripts
- local machine path leaks
- markdown code fence balance
- escaped newline artifacts
- important README documentation links
- final audit documentation
- final audit tests

## Usage

Run from the package repository root:

`hyperkit pre-release-audit`

Check a specific path:

`hyperkit pre-release-audit --path .`

## Recommended Final Flow

Run these commands before preparing a release candidate:

`pytest`

`hyperkit health`

`hyperkit release-check`

`hyperkit pre-release-audit`

`python -m build`

`twine check dist/*`

## Publishing Rule

For now, HyperKit should remain on GitHub and TestPyPI.

Do not publish to real PyPI until the SDK and templates are stable enough for public users.