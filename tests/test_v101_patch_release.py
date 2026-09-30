from pathlib import Path

import hyperkit

from hyperkit.api_contract import (
    FROZEN_API_EXPORT_COUNT,
    FROZEN_API_FINGERPRINT,
)
from hyperkit.stable_release import STABLE_PACKAGE_VERSION


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")
VERSION_HISTORY = Path("docs/VERSION_HISTORY.md")
PATCH_DOC = Path("docs/V101_PATCH_RELEASE.md")
WORKFLOW = Path(".github/workflows/stable-release.yml")


def test_v101_package_identity_and_api_contract():
    assert hyperkit.__version__ == "1.0.1"
    assert STABLE_PACKAGE_VERSION == "1.0.1"
    assert hyperkit.API_VERSION == "1.0"
    assert FROZEN_API_EXPORT_COUNT == 256
    assert len(FROZEN_API_FINGERPRINT) == 64


def test_v101_current_release_docs_are_synchronized():
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    changelog = CHANGELOG.read_text(encoding="utf-8")
    history = VERSION_HISTORY.read_text(encoding="utf-8")
    patch_doc = PATCH_DOC.read_text(encoding="utf-8")

    assert "Latest published PyPI release: `1.0.1`" in readme
    assert "Stable package version: `1.0.1`" in readme
    assert "Active development version: `1.0.1`" in readme
    assert "v1.0.1  Stable Patch Release" in roadmap
    assert "Active package version: `1.0.1`" in roadmap
    assert "## 1.0.1 - 2026-09-30" in changelog
    assert "## 1.0.1 — Stable Patch Release" in history
    assert "# HyperKit v1.0.1 — Stable Patch Release" in patch_doc


def test_v101_workflow_requires_matching_tag():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "refs/tags/v1.0.1" in workflow
    assert "hyperkit-1.0.1-stable-bundle" in workflow
    assert "Publish stable HyperKit 1.0.1 to PyPI" in workflow


def test_v101_stable_release_report_passes():
    report = hyperkit.generate_stable_release_report(".")
    assert report.package_version == "1.0.1"
    assert report.passed
