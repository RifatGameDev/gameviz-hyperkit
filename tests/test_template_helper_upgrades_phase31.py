from pathlib import Path


def read_template(template_name: str) -> str:
    return Path(f"src/hyperkit/templates/{template_name}/main.py").read_text(
        encoding="utf-8"
    )


def test_flappy_mini_template_uses_helper_systems():
    content = read_template("flappy_mini")

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content
    assert "ScoreManager" in content


def test_swipe_runner_template_uses_helper_systems():
    content = read_template("swipe_runner")

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "InputActionMap" in content
    assert "ScoreManager" in content


def test_flappy_mini_readme_mentions_helpers():
    content = Path("src/hyperkit/templates/flappy_mini/README.md").read_text(
        encoding="utf-8"
    )

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content


def test_swipe_runner_readme_mentions_helpers():
    content = Path("src/hyperkit/templates/swipe_runner/README.md").read_text(
        encoding="utf-8"
    )

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
