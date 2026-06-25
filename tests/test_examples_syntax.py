import ast
from pathlib import Path


def test_example_files_have_valid_python_syntax():
    example_files = Path("examples").glob("*/main.py")

    for path in example_files:
        ast.parse(path.read_text(encoding="utf-8"))
