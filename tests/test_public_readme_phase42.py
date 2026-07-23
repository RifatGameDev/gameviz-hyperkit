from pathlib import Path


README_PATH = Path("README.md")


def readme_content() -> str:
    return README_PATH.read_text(encoding="utf-8")


def test_public_readme_exists():
    assert README_PATH.exists()


def test_public_readme_has_package_identity():
    content = readme_content()

    assert "gameviz-hyperkit" in content
    assert "Import name: `hyperkit`" in content
    assert "CLI command: `hyperkit`" in content


def test_public_readme_explains_current_status():
    content = readme_content()

    assert "Current package version: `0.1.2`" in content
    assert (
        "Installation command: "
        "`pip install gameviz-hyperkit`"
        in content
    )
    assert "Package maturity: Alpha / early SDK preview" in content
    assert "API stability target: future `1.0.0`" in content
    assert "Supported Python versions: Python 3.9–3.12" in content


def test_public_readme_has_quick_start():
    content = readme_content()

    assert "## Quick Start" in content
    assert "hyperkit new my-game --template tap-counter" in content
    assert "cd my-game" in content
    assert "hyperkit run" in content
    assert "python main.py" in content


def test_public_readme_lists_templates():
    content = readme_content()

    assert "tap_counter" in content
    assert "flappy_mini" in content
    assert "swipe_runner" in content
    assert "puzzle_game" in content
    assert "quiz_game" in content
    assert "simple_physics" in content


def test_public_readme_mentions_limitations_and_roadmap():
    content = readme_content()

    assert "## Current Limitations" in content
    assert "Android APK build support remains experimental" in content
    assert "AdMob and analytics helper systems are not implemented yet" in content
    assert "## Roadmap" in content
    assert "Stable API milestone for version `1.0.0`" in content


def test_public_readme_links_core_docs():
    content = readme_content()

    assert "docs/VERSION_HISTORY.md" in content
    assert "CHANGELOG.md" in content
    assert "docs/TEMPLATE_HELPERS.md" in content
    assert "docs/TEMPLATES.md" in content
    assert "docs/RELEASE_READINESS_CHECKLIST.md" in content
    assert "docs/FINAL_PRE_RELEASE_AUDIT.md" in content


def test_public_readme_has_balanced_code_fences():
    content = readme_content()

    assert content.count("```") % 2 == 0


def test_public_readme_has_no_escaped_newline_artifacts():
    content = readme_content()

    assert "\\n" not in content
