from pathlib import Path

import hyperkit


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")


def test_v080_development_version_and_api_contract():
    assert hyperkit.__version__ == "0.8.0.dev0"
    assert hyperkit.API_VERSION == "0.2"


def test_v080_public_release_build_exports():
    expected = {
        "CleanInstallResult",
        "DistributionArtifact",
        "DistributionCheck",
        "DistributionReport",
        "ReleaseBuildError",
        "discover_distribution_artifacts",
        "generate_distribution_report",
        "run_clean_install_verification",
        "validate_publish_target",
        "write_checksum_manifest",
        "write_release_manifest",
    }

    assert expected.issubset(
        set(
            hyperkit.__all__
        )
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )


def test_v080_docs_track_current_stage():
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
        "`0.8.0.dev0`"
        in readme
    )
    assert (
        "v0.8.0  Build, Publishing + "
        "Production Hardening"
        in roadmap
    )
    assert (
        "CURRENT DEVELOPMENT STAGE"
        in roadmap
    )
    assert (
        "Current development version: "
        "``0.8.0.dev0``."
        in changelog
    )


def test_v080_health_tracks_milestone_artifacts():
    report = (
        hyperkit
        .generate_health_report(
            "."
        )
    )

    paths = {
        check.path
        for check in report.checks
    }

    expected = {
        "src/hyperkit/release_build.py",
        "src/hyperkit/android_release.py",
        "docs/V080_BUILD_PUBLISHING_PRODUCTION_HARDENING.md",
        ".github/workflows/release-package.yml",
        ".github/workflows/android-production-release.yml",
        "tests/test_v080_release_build.py",
        "tests/test_v080_android_production.py",
        "tests/test_v080_cli.py",
        "tests/test_v080_workflows.py",
        "tests/test_v080_milestone.py",
    }

    assert expected.issubset(
        paths
    )


def test_v080_release_report_tracks_milestone_artifacts():
    report = (
        hyperkit
        .generate_release_report(
            "."
        )
    )

    names = {
        check.name
        for check in report.checks
    }

    for path in (
        "src/hyperkit/release_build.py",
        "src/hyperkit/android_release.py",
        "docs/V080_BUILD_PUBLISHING_PRODUCTION_HARDENING.md",
        ".github/workflows/release-package.yml",
        ".github/workflows/android-production-release.yml",
    ):
        assert (
            f"Required release file: {path}"
            in names
        )

    for path in (
        "tests/test_v080_release_build.py",
        "tests/test_v080_android_production.py",
        "tests/test_v080_cli.py",
        "tests/test_v080_workflows.py",
        "tests/test_v080_milestone.py",
    ):
        assert (
            f"Required release test: {path}"
            in names
        )

    assert (
        "Distribution verification command"
        in names
    )
    assert (
        "Trusted publishing workflow"
        in names
    )
    assert (
        "Android production release workflow"
        in names
    )


def test_v080_pre_release_audit_remains_green():
    report = (
        hyperkit
        .generate_pre_release_audit_report(
            "."
        )
    )

    assert report.passed
