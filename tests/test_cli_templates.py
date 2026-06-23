from pathlib import Path

import pytest

from hyperkit.cli import copy_template, normalize_template_name


def test_normalize_template_name_accepts_dash_and_underscore():
    assert normalize_template_name("tap-counter") == "tap-counter"
    assert normalize_template_name("tap_counter") == "tap-counter"
    assert normalize_template_name("flappy-mini") == "flappy-mini"
    assert normalize_template_name("flappy_mini") == "flappy-mini"


def test_copy_template_creates_tap_counter_project(tmp_path: Path):
    project_path = tmp_path / "tap_game"

    copy_template("tap_counter", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_rejects_unknown_template(tmp_path: Path):
    with pytest.raises(ValueError):
        copy_template("unknown_template", tmp_path / "bad_game")
