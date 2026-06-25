from pathlib import Path

import pytest

from hyperkit.cli import (
    copy_template,
    create_project,
    normalize_template_name,
    read_project_metadata,
    validate_project,
)


def test_normalize_template_name_accepts_dash_and_underscore():
    assert normalize_template_name("tap-counter") == "tap-counter"
    assert normalize_template_name("tap_counter") == "tap-counter"

    assert normalize_template_name("flappy-mini") == "flappy-mini"
    assert normalize_template_name("flappy_mini") == "flappy-mini"

    assert normalize_template_name("swipe-runner") == "swipe-runner"
    assert normalize_template_name("swipe_runner") == "swipe-runner"

    assert normalize_template_name("puzzle-game") == "puzzle-game"
    assert normalize_template_name("puzzle_game") == "puzzle-game"

    assert normalize_template_name("quiz-game") == "quiz-game"
    assert normalize_template_name("quiz_game") == "quiz-game"

    assert normalize_template_name("simple-physics") == "simple-physics"
    assert normalize_template_name("simple_physics") == "simple-physics"


def test_copy_template_creates_tap_counter_project(tmp_path: Path):
    project_path = tmp_path / "tap_game"

    copy_template("tap_counter", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_creates_flappy_mini_project(tmp_path: Path):
    project_path = tmp_path / "flappy_game"

    copy_template("flappy_mini", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_creates_swipe_runner_project(tmp_path: Path):
    project_path = tmp_path / "swipe_game"

    copy_template("swipe_runner", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_creates_puzzle_game_project(tmp_path: Path):
    project_path = tmp_path / "puzzle_game"

    copy_template("puzzle_game", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_creates_quiz_game_project(tmp_path: Path):
    project_path = tmp_path / "quiz_game"

    copy_template("quiz_game", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_creates_simple_physics_project(tmp_path: Path):
    project_path = tmp_path / "simple_physics"

    copy_template("simple_physics", project_path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()


def test_copy_template_rejects_unknown_template(tmp_path: Path):
    with pytest.raises(ValueError):
        copy_template("unknown_template", tmp_path / "bad_game")


def test_create_project_writes_metadata(tmp_path: Path):
    project_path = tmp_path / "my_game"

    create_project("my_game", "tap_counter", project_path)

    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "hyperkit.toml").exists()

    metadata = read_project_metadata(project_path)

    assert metadata["project"]["name"] == "my_game"
    assert metadata["project"]["template"] == "tap-counter"
    assert metadata["run"]["main"] == "main.py"


def test_validate_project_accepts_generated_project(tmp_path: Path):
    project_path = tmp_path / "valid_game"

    create_project("valid_game", "swipe_runner", project_path)

    is_valid, issues = validate_project(project_path)

    assert is_valid
    assert issues == []


def test_validate_project_rejects_missing_metadata(tmp_path: Path):
    project_path = tmp_path / "old_game"
    project_path.mkdir()
    (project_path / "main.py").write_text("print('hello')", encoding="utf-8")

    is_valid, issues = validate_project(project_path)

    assert not is_valid
    assert "Missing hyperkit.toml project metadata" in issues
