from pathlib import Path

import hyperkit


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")


def test_v050_development_version_and_api_contract():
    assert hyperkit.__version__ == "1.0.0"
    assert hyperkit.API_VERSION == "1.0"


def test_v050_public_developer_tooling_exports():
    expected = {
        "DebugOverlay",
        "RuntimeDiagnostics",
        "RuntimeSnapshot",
        "COMPLETE_GAME_TEMPLATES",
        "CompleteGameReport",
        "generate_complete_game_report",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )


def test_v050_docs_track_current_stage():
    readme = README.read_text(
        encoding="utf-8"
    )
    roadmap = ROADMAP.read_text(
        encoding="utf-8"
    )
    changelog = CHANGELOG.read_text(
        encoding="utf-8"
    )

    assert "Active development version: `1.0.0`" in readme
    assert "v0.5.0  Complete Games + Developer Tooling" in roadmap
    assert "CURRENT DEVELOPMENT STAGE" in roadmap
    assert "Current development version: ``1.0.0``." in changelog


def test_v050_health_tracks_milestone_artifacts():
    report = hyperkit.generate_health_report(
        "."
    )
    paths = {
        check.path
        for check in report.checks
    }

    expected = {
        "src/hyperkit/devtools.py",
        "src/hyperkit/complete_games.py",
        "docs/V050_COMPLETE_GAMES_TOOLING.md",
        ".github/workflows/ci.yml",
    }

    assert expected.issubset(
        paths
    )


def test_v050_release_report_tracks_milestone_artifacts():
    report = hyperkit.generate_release_report(
        "."
    )
    names = {
        check.name
        for check in report.checks
    }

    assert (
        "Required release file: "
        "docs/V050_COMPLETE_GAMES_TOOLING.md"
        in names
    )
    assert (
        "Required release file: "
        "src/hyperkit/devtools.py"
        in names
    )
    assert (
        "Required release file: "
        "src/hyperkit/complete_games.py"
        in names
    )


def test_v050_pre_release_audit_remains_green():
    report = (
        hyperkit
        .generate_pre_release_audit_report(
            "."
        )
    )

    assert report.passed
