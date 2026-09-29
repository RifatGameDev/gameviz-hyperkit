from pathlib import Path

import hyperkit


README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
CHANGELOG = Path("CHANGELOG.md")
SIMPLE_PHYSICS_README = Path(
    "src/hyperkit/templates/simple_physics/README.md"
)
SIMPLE_PHYSICS_DOC = Path(
    "docs/SIMPLE_PHYSICS_POLISH_PHASE53.md"
)


def read(path: Path) -> str:
    return path.read_text(
        encoding="utf-8"
    )


def test_readme_tracks_active_development_version():
    content = read(
        README
    )

    assert (
        f"Active development version: "
        f"`{hyperkit.__version__}`"
        in content
    )
    assert (
        "Latest published PyPI release: `0.2.0`"
        in content
    )


def test_readme_no_longer_claims_ads_are_missing():
    content = read(
        README
    )

    assert (
        "AdMob and analytics helper systems "
        "are not implemented yet"
        not in content
    )
    assert (
        "AdMob and Firebase Analytics integrations exist"
        in content
    )


def test_roadmap_tracks_completion_audit():
    content = read(
        ROADMAP
    )

    assert "Phase 75 — SDK Completion Audit" in content
    assert "0.6.0.dev0" in content
    assert "919 passing tests" in content
    assert "Feature Freeze Rule" in content


def test_changelog_records_phase75_hardening():
    content = read(
        CHANGELOG
    )

    assert "Phase 75 SDK completion audit and hardening" in content
    assert "919 passing tests" in content
    assert (
        "API compatibility contract remains `0.2`"
        in content
    )


def test_simple_physics_docs_match_physics_world_architecture():
    template_content = read(
        SIMPLE_PHYSICS_README
    )
    phase_content = read(
        SIMPLE_PHYSICS_DOC
    )

    for content in (
        template_content,
        phase_content,
    ):
        assert "PhysicsWorld" in content
        assert "PhysicsMaterial" in content
        assert "layers and masks" in content
