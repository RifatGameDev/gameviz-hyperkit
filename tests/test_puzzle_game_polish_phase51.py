import ast
from pathlib import Path


TEMPLATE_MAIN = Path("src/hyperkit/templates/puzzle_game/main.py")
TEMPLATE_README = Path("src/hyperkit/templates/puzzle_game/README.md")
PHASE_DOC = Path("docs/PUZZLE_GAME_POLISH_PHASE51.md")
README = Path("README.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_puzzle_game_main_exists_and_has_valid_syntax():
    assert TEMPLATE_MAIN.exists()

    content = read(TEMPLATE_MAIN)
    ast.parse(content, filename=str(TEMPLATE_MAIN))


def test_puzzle_game_main_uses_core_hyperkit_features():
    content = read(TEMPLATE_MAIN)

    assert "from hyperkit import" in content
    assert "AssetManager" in content
    assert "BoundsManager" in content
    assert "CameraShake" in content
    assert "GameObject" in content
    assert "InputActionMap" in content
    assert "ParticleEmitter" in content
    assert "ProgressBar" in content
    assert "Scene" in content
    assert "ScoreManager" in content
    assert "ScreenBounds" in content
    assert "TextLabel" in content


def test_puzzle_game_main_has_clear_scene_and_entry_point():
    content = read(TEMPLATE_MAIN)

    assert "class PuzzleGameScene(Scene):" in content
    assert "def start(self):" in content
    assert "def update(self, dt):" in content
    assert "def on_tap(self, x, y):" in content
    assert "Game(" in content
    assert ".set_scene(" in content
    assert ".run()" in content


def test_puzzle_game_main_has_puzzle_gameplay_logic():
    content = read(TEMPLATE_MAIN)

    assert "self.grid_size" in content
    assert "self.tiles" in content
    assert "self.active_tile_index" in content
    assert "_create_grid" in content
    assert "_find_tapped_tile" in content
    assert "_handle_correct_tap" in content
    assert "_handle_wrong_tap" in content
    assert "_restart" in content


def test_puzzle_game_template_readme_is_polished():
    assert TEMPLATE_README.exists()

    content = read(TEMPLATE_README)

    assert "# Puzzle Game Template" in content
    assert "Features" in content
    assert "Run" in content
    assert "Gameplay" in content
    assert "Helper Systems Used" in content
    assert "Customization Ideas" in content
    assert "ScoreManager" in content
    assert "ProgressBar" in content
    assert "CameraShake" in content


def test_puzzle_game_phase_doc_exists():
    assert PHASE_DOC.exists()

    content = read(PHASE_DOC)

    assert "Puzzle Game Polish - Phase 51" in content
    assert "first production-quality polish pass" in content
    assert "hyperkit validate-templates" in content


def test_main_readme_links_puzzle_game_polish_doc():
    content = read(README)

    assert "Puzzle Game Polish - Phase 51" in content
    assert "docs/PUZZLE_GAME_POLISH_PHASE51.md" in content


def test_health_checks_include_puzzle_game_polish_doc():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/PUZZLE_GAME_POLISH_PHASE51.md" in paths
    assert "tests/test_puzzle_game_polish_phase51.py" in paths


def test_release_checks_include_puzzle_game_polish_doc():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/PUZZLE_GAME_POLISH_PHASE51.md" in check_names
    assert (
        "Required release test: tests/test_puzzle_game_polish_phase51.py"
        in check_names
    )


def test_puzzle_game_files_have_no_local_paths_or_escaped_newlines():
    files = [TEMPLATE_MAIN, TEMPLATE_README, PHASE_DOC]

    forbidden_terms = [
        "D:\\AI\\HyperKit\\gameviz-hyperkit",
        "/mnt/data",
        "\\n\\n",
    ]

    for path in files:
        content = read(path)

        for term in forbidden_terms:
            assert term not in content
