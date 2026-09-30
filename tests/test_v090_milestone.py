from pathlib import Path

import hyperkit
from hyperkit.api_contract import (
    FROZEN_API_EXPORT_COUNT,
    FROZEN_API_FINGERPRINT,
)


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")


def test_v090_beta_version_and_frozen_api_contract():
    assert hyperkit.__version__ == "1.0.0"
    assert hyperkit.API_VERSION == "1.0"
    assert FROZEN_API_EXPORT_COUNT == 256
    assert len(
        FROZEN_API_FINGERPRINT
    ) == 64


def test_v090_docs_track_current_stage():
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
        "Active development version: "
        "`1.0.0`"
        in readme
    )
    assert (
        "Package maturity: "
        "Production / Stable"
        in readme
    )
    assert (
        "Public compatibility contract: "
        "API `1.0`"
        in readme
    )
    assert (
        "v0.9.0  API Freeze + Public Beta"
        in roadmap
    )
    assert (
        "CURRENT DEVELOPMENT STAGE"
        in roadmap
    )
    assert (
        "Current development version: "
        "``1.0.0``."
        in changelog
    )


def test_v090_health_tracks_milestone_artifacts():
    report = hyperkit.generate_health_report(
        "."
    )

    paths = {
        check.path
        for check in report.checks
    }

    expected = {
        "docs/V090_API_FREEZE_PUBLIC_BETA.md",
        ".github/workflows/public-beta.yml",
        "tests/test_v090_api_freeze.py",
        "tests/test_v090_cli.py",
        "tests/test_v090_workflows.py",
        "tests/test_v090_milestone.py",
    }

    assert expected.issubset(
        paths
    )


def test_v090_release_report_tracks_milestone_artifacts():
    report = hyperkit.generate_release_report(
        "."
    )

    names = {
        check.name
        for check in report.checks
    }

    for path in (
        "docs/V090_API_FREEZE_PUBLIC_BETA.md",
        ".github/workflows/public-beta.yml",
    ):
        assert (
            f"Required release file: {path}"
            in names
        )

    for path in (
        "tests/test_v090_api_freeze.py",
        "tests/test_v090_cli.py",
        "tests/test_v090_workflows.py",
        "tests/test_v090_milestone.py",
    ):
        assert (
            f"Required release test: {path}"
            in names
        )

    assert (
        "Frozen API exact-match check"
        in names
    )
    assert (
        "Public beta workflow"
        in names
    )


def test_v090_pre_release_audit_remains_green():
    report = (
        hyperkit
        .generate_pre_release_audit_report(
            "."
        )
    )

    assert report.passed
