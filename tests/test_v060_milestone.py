from pathlib import Path

import hyperkit


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")


def test_v060_development_version_and_api_contract():
    assert hyperkit.__version__ == "1.0.0"
    assert hyperkit.API_VERSION == "1.0"


def test_v060_public_performance_exports():
    expected = {
        "FixedStepClock",
        "FrameTimeController",
        "PerformanceMode",
        "PerformanceProfile",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )


def test_v060_docs_track_current_stage():
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
        "v0.6.0  Mobile Production "
        "Runtime + Performance"
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


def test_v060_health_tracks_milestone_artifacts():
    report = hyperkit.generate_health_report(
        "."
    )
    paths = {
        check.path
        for check in report.checks
    }

    expected = {
        "src/hyperkit/performance.py",
        "docs/V060_MOBILE_RUNTIME_PERFORMANCE.md",
        "tests/test_v060_performance.py",
        "tests/test_v060_mobile_runtime.py",
        "tests/test_v060_service_lifecycle.py",
        "tests/test_v060_milestone.py",
    }

    assert expected.issubset(
        paths
    )


def test_v060_release_report_tracks_milestone_artifacts():
    report = hyperkit.generate_release_report(
        "."
    )
    names = {
        check.name
        for check in report.checks
    }

    for path in (
        "src/hyperkit/performance.py",
        "docs/V060_MOBILE_RUNTIME_PERFORMANCE.md",
    ):
        assert (
            f"Required release file: {path}"
            in names
        )

    for path in (
        "tests/test_v060_performance.py",
        "tests/test_v060_mobile_runtime.py",
        "tests/test_v060_service_lifecycle.py",
        "tests/test_v060_milestone.py",
    ):
        assert (
            f"Required release test: {path}"
            in names
        )


def test_v060_pre_release_audit_remains_green():
    report = (
        hyperkit
        .generate_pre_release_audit_report(
            "."
        )
    )

    assert report.passed
