import ast
from pathlib import Path


TEMPLATE_MAIN = Path("src/hyperkit/templates/tap_counter/main.py")
TEMPLATE_README = Path("src/hyperkit/templates/tap_counter/README.md")
PHASE_DOC = Path("docs/TAP_COUNTER_POLISH_PHASE48.md")
README = Path("README.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_tap_counter_main_exists_and_has_valid_syntax():
    assert TEMPLATE_MAIN.exists()

    content = read(TEMPLATE_MAIN)
    ast.parse(content, filename=str(TEMPLATE_MAIN))


def test_tap_counter_main_uses_core_hyperkit_features():
    content = read(TEMPLATE_MAIN)

    assert "from hyperkit import" in content
    assert "GameObject" in content
    assert "Scene" in content
    assert "ScoreManager" in content
    assert "TextLabel" in content
    assert "ProgressBar" in content


def test_tap_counter_main_has_clear_scene_and_entry_point():
    content = read(TEMPLATE_MAIN)

    assert "class TapCounterScene(Scene):" in content
    assert "def start(self):" in content
    assert "def on_tap(self, x, y):" in content
    assert "Game(" in content
    assert ".set_scene(" in content
    assert ".run()" in content


def test_tap_counter_main_has_score_goal_and_feedback():
    content = read(TEMPLATE_MAIN)

    assert "self.tap_goal" in content
    assert "Goal Progress" in content
    assert "High Score" in content
    assert "Goal reached" in content
    assert "status_label" in content


def test_tap_counter_template_readme_is_polished():
    assert TEMPLATE_README.exists()

    content = read(TEMPLATE_README)

    assert "# Tap Counter Template" in content
    assert "What This Template Demonstrates" in content
    assert "How to Run" in content
    assert "Controls" in content
    assert "Customization Ideas" in content
    assert "ScoreManager" in content
    assert "ProgressBar" in content


def test_tap_counter_phase_doc_exists():
    assert PHASE_DOC.exists()

    content = read(PHASE_DOC)

    assert "Tap Counter Polish - Phase 48" in content
    assert "first production-quality polish pass" in content
    assert "hyperkit validate-templates" in content


def test_main_readme_links_tap_counter_polish_doc():
    content = read(README)

    assert "Tap Counter Polish - Phase 48" in content
    assert "docs/TAP_COUNTER_POLISH_PHASE48.md" in content


def test_health_checks_include_tap_counter_polish_doc():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/TAP_COUNTER_POLISH_PHASE48.md" in paths
    assert "tests/test_tap_counter_polish_phase48.py" in paths


def test_release_checks_include_tap_counter_polish_doc():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/TAP_COUNTER_POLISH_PHASE48.md" in check_names
    assert (
        "Required release test: tests/test_tap_counter_polish_phase48.py"
        in check_names
    )


def test_tap_counter_files_have_no_local_paths_or_escaped_newlines():
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
