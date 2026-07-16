from pathlib import Path


def test_template_helpers_doc_exists():
    path = Path("docs/TEMPLATE_HELPERS.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Template Helper Usage Guide" in content
    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content
    assert "Cooldown" in content


def test_templates_doc_exists_and_lists_templates():
    path = Path("docs/TEMPLATES.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "HyperKit Templates" in content
    assert "tap_counter" in content
    assert "flappy_mini" in content
    assert "swipe_runner" in content
    assert "puzzle_game" in content
    assert "quiz_game" in content
    assert "simple_physics" in content


def test_main_readme_links_template_helper_guide():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "Template Helper Usage Guide" in content
    assert "docs/TEMPLATE_HELPERS.md" in content
