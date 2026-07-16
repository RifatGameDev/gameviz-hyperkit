import tomllib
from pathlib import Path


def test_changelog_exists_and_has_required_sections():
    path = Path("CHANGELOG.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "# Changelog" in content
    assert "## Unreleased" in content
    assert "## 0.1.0" in content
    assert "Added" in content
    assert "Changed" in content
    assert "Documentation" in content


def test_changelog_mentions_key_helpers_and_templates():
    content = Path("CHANGELOG.md").read_text(encoding="utf-8")

    required_terms = [
        "Particle",
        "Camera shake",
        "Progress",
        "Input action",
        "Level data",
        "tap_counter",
        "flappy_mini",
        "swipe_runner",
        "puzzle_game",
        "quiz_game",
        "simple_physics",
    ]

    for term in required_terms:
        assert term in content, f"CHANGELOG.md missing {term}"


def test_version_history_doc_exists():
    path = Path("docs/VERSION_HISTORY.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Version History" in content
    assert "gameviz-hyperkit" in content
    assert "hyperkit" in content
    assert "0.1.0" in content
    assert "0.2.0" in content


def test_version_history_mentions_package_identity():
    content = Path("docs/VERSION_HISTORY.md").read_text(encoding="utf-8")

    assert "Package name" in content
    assert "Import name" in content
    assert "CLI command" in content
    assert "gameviz-hyperkit" in content
    assert "hyperkit" in content


def test_pyproject_version_is_mentioned_in_changelog_or_version_history():
    with Path("pyproject.toml").open("rb") as file:
        data = tomllib.load(file)

    version = data["project"]["version"]

    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    version_history = Path("docs/VERSION_HISTORY.md").read_text(encoding="utf-8")

    assert version in changelog or version in version_history


def test_main_readme_links_changelog_and_version_history():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "Changelog" in content
    assert "CHANGELOG.md" in content
    assert "Version History" in content
    assert "docs/VERSION_HISTORY.md" in content
