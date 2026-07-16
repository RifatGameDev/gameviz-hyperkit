# Release Readiness Checklist

This checklist is used before publishing a new HyperKit version.

HyperKit should only be released when the package, templates, examples, documentation, and tests are in a clean state.

---

## 1. Git Status

Before release:

```bash
git status
```

Expected:

```text
working tree clean
```

---

## 2. Test Suite

Run the full test suite:

```bash
pytest
```

Expected:

```text
all tests passed
```

---

## 3. Editable Install

Reinstall the package locally:

```bash
pip install -e .
```

Check the CLI:

```bash
hyperkit doctor
hyperkit info
hyperkit list-templates
```

---

## 4. Template Validation

Create and run important starter templates outside the package repo:

```bash
cd /d D:\AI\HyperKit
hyperkit new release-tap-test --template tap_counter
hyperkit new release-flappy-test --template flappy_mini
hyperkit new release-runner-test --template swipe_runner
```

Run each generated project:

```bash
cd release-tap-test
python main.py
```

Do not commit generated test projects.

---

## 5. Package Build

Build the package:

```bash
python -m build
```

Expected output:

```text
dist/
├── gameviz_hyperkit-<version>.tar.gz
└── gameviz_hyperkit-<version>-py3-none-any.whl
```

---

## 6. Package Check

Check the built files:

```bash
twine check dist/*
```

Expected:

```text
PASSED
```

---

## 7. Metadata Checklist

`pyproject.toml` should include:

- package name
- version
- description
- README reference
- Python version requirement
- author information
- dependencies
- CLI script entry point

Expected package identity:

```text
Package name: gameviz-hyperkit
Import name: hyperkit
CLI command: hyperkit
```

---

## 8. Documentation Checklist

Before release, confirm these files exist:

- `README.md`
- `docs/TEMPLATES.md`
- `docs/TEMPLATE_HELPERS.md`
- `docs/TEMPLATE_QUALITY_CHECKLIST.md`
- `docs/RELEASE_READINESS_CHECKLIST.md`

---

## 9. Current Publishing Rule

For now, HyperKit should stay on:

```text
GitHub + TestPyPI
```

Do not publish to real PyPI until the package is more stable.

---

## 10. Release Commit

Use a clear release preparation commit:

```bash
git add .
git commit -m "Prepare release readiness validation"
git push origin develop
```
