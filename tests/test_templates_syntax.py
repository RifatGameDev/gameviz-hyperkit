import ast
from pathlib import Path


def test_tap_counter_template_has_valid_python_syntax():
    path = Path("src/hyperkit/templates/tap_counter/main.py")
    ast.parse(path.read_text(encoding="utf-8"))


def test_flappy_mini_template_has_valid_python_syntax():
    path = Path("src/hyperkit/templates/flappy_mini/main.py")
    ast.parse(path.read_text(encoding="utf-8"))


def test_swipe_runner_template_has_valid_python_syntax():
    path = Path("src/hyperkit/templates/swipe_runner/main.py")
    ast.parse(path.read_text(encoding="utf-8"))


def test_puzzle_game_template_has_valid_python_syntax():
    path = Path("src/hyperkit/templates/puzzle_game/main.py")
    ast.parse(path.read_text(encoding="utf-8"))
