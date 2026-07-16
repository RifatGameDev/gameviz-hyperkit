from pathlib import Path


def read_template(template_name: str) -> str:
    return Path(f"src/hyperkit/templates/{template_name}/main.py").read_text(
        encoding="utf-8"
    )


def read_template_readme(template_name: str) -> str:
    return Path(f"src/hyperkit/templates/{template_name}/README.md").read_text(
        encoding="utf-8"
    )


def test_puzzle_game_template_uses_helper_systems():
    content = read_template("puzzle_game")

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content
    assert "ScoreManager" in content


def test_quiz_game_template_uses_helper_systems():
    content = read_template("quiz_game")

    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "InputActionMap" in content
    assert "ScoreManager" in content


def test_simple_physics_template_uses_helper_systems():
    content = read_template("simple_physics")

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content
    assert "Cooldown" in content


def test_puzzle_game_readme_mentions_helpers():
    content = read_template_readme("puzzle_game")

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content


def test_quiz_game_readme_mentions_helpers():
    content = read_template_readme("quiz_game")

    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "InputActionMap" in content
    assert "ScoreManager" in content


def test_simple_physics_readme_mentions_helpers():
    content = read_template_readme("simple_physics")

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content
    assert "Cooldown" in content
