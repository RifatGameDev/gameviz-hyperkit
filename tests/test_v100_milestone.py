from pathlib import Path

import hyperkit

from hyperkit.api_contract import (
    FROZEN_API_EXPORT_COUNT,
    FROZEN_API_FINGERPRINT,
)


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")


def test_v100_stable_version_and_api_contract():
    assert hyperkit.__version__ == "1.0.0"
    assert hyperkit.API_VERSION == "1.0"
    assert FROZEN_API_EXPORT_COUNT == 256
    assert len(
        FROZEN_API_FINGERPRINT
    ) == 64


def test_v100_docs_track_stable_release():
    readme = README.read_text(
        encoding="utf-8"
    )
    roadmap = ROADMAP.read_text(
        encoding="utf-8"
    )
    changelog = CHANGELOG.read_text(
        encoding="utf-8"
    )

    assert (
        "Stable package version: `1.0.0`"
        in readme
    )
    assert (
        "Package maturity: Production / Stable"
        in readme
    )
    assert (
        "Public compatibility contract: API `1.0`"
        in readme
    )
    assert (
        "v1.0.0  Stable Release"
        in roadmap
    )
    assert (
        "CURRENT DEVELOPMENT STAGE"
        in roadmap
    )
    assert (
        "Active package version: `1.0.0`"
        in roadmap
    )
    assert "## 1.0.0" in changelog
    assert "Stable Release" in changelog


def test_v100_health_tracks_stable_artifacts():
    report = hyperkit.generate_health_report(
        "."
    )

    paths = {
        check.path
        for check in report.checks
    }

    expected = {
        "src/hyperkit/stable_release.py",
        "docs/V100_STABLE_RELEASE.md",
        ".github/workflows/stable-release.yml",
        "tests/test_v100_stable_release.py",
        "tests/test_v100_cli.py",
        "tests/test_v100_workflow.py",
        "tests/test_v100_milestone.py",
    }

    assert expected.issubset(
        paths
    )


def test_v100_release_report_tracks_stable_artifacts():
    report = hyperkit.generate_release_report(
        "."
    )

    names = {
        check.name
        for check in report.checks
    }

    for path in (
        "src/hyperkit/stable_release.py",
        "docs/V100_STABLE_RELEASE.md",
        ".github/workflows/stable-release.yml",
    ):
        assert (
            f"Required release file: {path}"
            in names
        )

    for path in (
        "tests/test_v100_stable_release.py",
        "tests/test_v100_cli.py",
        "tests/test_v100_workflow.py",
        "tests/test_v100_milestone.py",
    ):
        assert (
            f"Required release test: {path}"
            in names
        )

    assert (
        "Stable release certification command"
        in names
    )
    assert (
        "Stable release workflow"
        in names
    )


def test_v100_pre_release_audit_remains_green():
    report = (
        hyperkit
        .generate_pre_release_audit_report(
            "."
        )
    )

    assert report.passed
