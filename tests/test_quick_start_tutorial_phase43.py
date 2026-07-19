from pathlib import Path


DOC_PATH = Path("docs/QUICK_START_TUTORIAL.md")
README_PATH = Path("README.md")


def read_doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_quick_start_tutorial_exists():
    assert DOC_PATH.exists()


def test_quick_start_tutorial_has_main_sections():
    content = read_doc()

    assert "# Beginner Quick Start Tutorial" in content
    assert "## Requirements" in content
    assert "## Create Your First Game" in content
    assert "## Generated Project Structure" in content
    assert "## Common Problems" in content
    assert "## Next Steps" in content


def test_quick_start_tutorial_mentions_testpypi_install():
    content = read_doc()

    assert "TestPyPI" in content
    assert "gameviz-hyperkit==0.1.1.dev1" in content
    assert "--index-url https://test.pypi.org/simple/" in content
    assert "--extra-index-url https://pypi.org/simple/" in content


def test_quick_start_tutorial_has_first_game_commands():
    content = read_doc()

    assert "hyperkit doctor" in content
    assert "hyperkit new my-first-game --template tap_counter" in content
    assert "cd my-first-game" in content
    assert "python main.py" in content


def test_quick_start_tutorial_lists_all_templates():
    content = read_doc()

    assert "tap_counter" in content
    assert "flappy_mini" in content
    assert "swipe_runner" in content
    assert "puzzle_game" in content
    assert "quiz_game" in content
    assert "simple_physics" in content


def test_quick_start_tutorial_has_basic_code_example():
    content = read_doc()

    assert "from hyperkit import Game, GameObject, Scene" in content
    assert "class MyScene(Scene):" in content
    assert "def on_tap(self, x, y):" in content
    assert "Game(title=\"My First HyperKit Game\")" in content


def test_quick_start_tutorial_mentions_validation():
    content = read_doc()

    assert "hyperkit validate" in content
    assert "Status: valid" in content


def test_readme_links_quick_start_tutorial():
    content = README_PATH.read_text(encoding="utf-8")

    assert "Beginner Quick Start Tutorial" in content
    assert "docs/QUICK_START_TUTORIAL.md" in content


def test_health_checks_include_quick_start_tutorial():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/QUICK_START_TUTORIAL.md" in paths
    assert "tests/test_quick_start_tutorial_phase43.py" in paths


def test_release_checks_include_quick_start_tutorial():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/QUICK_START_TUTORIAL.md" in check_names
    assert (
        "Required release test: tests/test_quick_start_tutorial_phase43.py"
        in check_names
    )


def test_quick_start_tutorial_markdown_fences_are_balanced():
    content = read_doc()

    assert content.count("```") % 2 == 0
