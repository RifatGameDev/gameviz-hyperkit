from hyperkit.android import create_buildozer_spec, normalized_package_name


def test_normalized_package_name():
    assert normalized_package_name("Tap Counter Game") == "tap_counter_game"


def test_create_buildozer_spec(tmp_path):
    path = create_buildozer_spec(tmp_path, title="Tap Counter")
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "requirements = python3,kivy,gameviz-hyperkit" in content
