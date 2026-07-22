from pathlib import Path


DOC_PATH = Path("docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md")
README_PATH = Path("README.md")

EXPECTED_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


def read_doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_production_template_polish_checklist_exists():
    assert DOC_PATH.exists()


def test_production_template_polish_checklist_has_main_sections():
    content = read_doc()

    assert "# Production Template Polish Checklist" in content
    assert "## Purpose" in content
    assert "## Template Coverage" in content
    assert "## Code Quality Checklist" in content
    assert "## Gameplay Checklist" in content
    assert "## Visual Polish Checklist" in content
    assert "## Documentation Checklist" in content
    assert "## Media Checklist" in content
    assert "## Testing Checklist" in content
    assert "## Stable Release Target" in content


def test_production_template_polish_checklist_mentions_all_templates():
    content = read_doc()

    for template in EXPECTED_TEMPLATES:
        assert template in content


def test_production_template_polish_checklist_mentions_required_files():
    content = read_doc()

    assert "main.py" in content
    assert "README.md" in content
    assert "no local development paths" in content
    assert "no temporary debug files" in content


def test_production_template_polish_checklist_mentions_validation_commands():
    content = read_doc()

    assert "pytest" in content
    assert "hyperkit validate-templates" in content
    assert "hyperkit health" in content
    assert "hyperkit release-check" in content
    assert "hyperkit pre-release-audit" in content


def test_production_template_polish_checklist_mentions_media_files():
    content = read_doc()

    assert "screenshot.png" in content
    assert "demo.gif" in content
    assert "thumbnail.png" in content


def test_readme_links_production_template_polish_checklist():
    content = README_PATH.read_text(encoding="utf-8")

    assert "Production Template Polish Checklist" in content
    assert "docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md" in content


def test_health_checks_include_production_template_polish_checklist():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md" in paths
    assert "tests/test_production_template_polish_phase47.py" in paths


def test_release_checks_include_production_template_polish_checklist():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert (
        "Required release file: docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md"
        in check_names
    )
    assert (
        "Required release test: tests/test_production_template_polish_phase47.py"
        in check_names
    )


def test_production_template_polish_markdown_fences_are_balanced():
    content = read_doc()

    assert content.count("```") % 2 == 0
