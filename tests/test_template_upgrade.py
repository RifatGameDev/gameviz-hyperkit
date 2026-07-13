from pathlib import Path


def test_tap_counter_template_uses_helper_systems():
    content = Path("src/hyperkit/templates/tap_counter/main.py").read_text(
        encoding="utf-8"
    )

    assert "AssetManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content
    assert "BoundsManager" in content
    assert "InputActionMap" in content


def test_template_helper_showcase_example_exists():
    path = Path("examples/template_helper_showcase_demo/main.py")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "TemplateHelperShowcaseDemo" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
