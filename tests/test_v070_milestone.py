from pathlib import Path

import hyperkit


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")


def test_v070_development_version_and_api_contract():
    assert hyperkit.__version__ == "1.0.0"
    assert hyperkit.API_VERSION == "1.0"


def test_v070_public_content_and_gameplay_exports():
    expected = {
        "ContentError",
        "ContentItem",
        "ContentManager",
        "ContentManifest",
        "Prefab",
        "PrefabError",
        "PrefabLibrary",
        "ObjectPool",
        "ObjectPoolError",
        "LevelSequence",
        "LevelSequenceError",
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


def test_v070_docs_track_current_stage():
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
        "v0.7.0  Content, Assets + "
        "Advanced Game Features"
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


def test_v070_health_tracks_milestone_artifacts():
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
        "src/hyperkit/content.py",
        "src/hyperkit/prefab.py",
        "src/hyperkit/pool.py",
        "src/hyperkit/level_sequence.py",
        "docs/V070_CONTENT_ASSETS_ADVANCED_FEATURES.md",
        "tests/test_v070_content.py",
        "tests/test_v070_prefab.py",
        "tests/test_v070_pool.py",
        "tests/test_v070_level_sequence.py",
        "tests/test_v070_asset_cache.py",
        "tests/test_v070_sprite_pattern.py",
        "tests/test_v070_cli.py",
        "tests/test_v070_milestone.py",
    }

    assert expected.issubset(
        paths
    )


def test_v070_release_report_tracks_milestone_artifacts():
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
        "src/hyperkit/content.py",
        "src/hyperkit/prefab.py",
        "src/hyperkit/pool.py",
        "src/hyperkit/level_sequence.py",
        "docs/V070_CONTENT_ASSETS_ADVANCED_FEATURES.md",
    ):
        assert (
            f"Required release file: {path}"
            in names
        )

    for path in (
        "tests/test_v070_content.py",
        "tests/test_v070_prefab.py",
        "tests/test_v070_pool.py",
        "tests/test_v070_level_sequence.py",
        "tests/test_v070_asset_cache.py",
        "tests/test_v070_sprite_pattern.py",
        "tests/test_v070_cli.py",
        "tests/test_v070_milestone.py",
    ):
        assert (
            f"Required release test: {path}"
            in names
        )


def test_v070_pre_release_audit_remains_green():
    report = (
        hyperkit
        .generate_pre_release_audit_report(
            "."
        )
    )

    assert report.passed
