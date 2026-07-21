from pathlib import Path


RUNTIME_DOC = Path("docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md")
QA_CHECKLIST = Path("docs/TEMPLATE_MANUAL_QA_CHECKLIST.md")
STABILIZATION_DOC = Path("docs/TEMPLATE_STABILIZATION_CHECKLIST.md")
README = Path("README.md")


TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


DISPLAY_NAMES = [
    "Tap Counter",
    "Flappy Mini",
    "Swipe Runner",
    "Puzzle Game",
    "Quiz Game",
    "Simple Physics",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_runtime_readiness_doc_exists():
    assert RUNTIME_DOC.exists()


def test_manual_qa_checklist_exists():
    assert QA_CHECKLIST.exists()


def test_runtime_readiness_doc_mentions_all_templates():
    content = read(RUNTIME_DOC)

    assert "# Template Runtime Readiness - Phase 56" in content

    for template in TEMPLATES:
        assert template in content


def test_runtime_readiness_doc_mentions_automated_commands():
    content = read(RUNTIME_DOC)

    assert "pytest" in content
    assert "hyperkit validate-templates" in content
    assert "hyperkit validate-generated-projects" in content
    assert "hyperkit health" in content
    assert "hyperkit release-check" in content
    assert "hyperkit pre-release-audit" in content


def test_runtime_readiness_doc_mentions_manual_runtime_requirements():
    content = read(RUNTIME_DOC)

    assert "launch without startup errors" in content
    assert "open the graphical game window" in content
    assert "respond correctly to player input" in content
    assert "restart correctly" in content
    assert "python main.py" in content


def test_manual_qa_checklist_has_common_sections():
    content = read(QA_CHECKLIST)

    assert "## QA Environment" in content
    assert "## Common Startup Checklist" in content
    assert "## Screen and Layout QA" in content
    assert "## Repeat Run QA" in content
    assert "## QA Result" in content
    assert "## Release Rule" in content


def test_manual_qa_checklist_mentions_all_templates():
    content = read(QA_CHECKLIST)

    for display_name in DISPLAY_NAMES:
        assert display_name in content


def test_manual_qa_checklist_contains_generation_commands():
    content = read(QA_CHECKLIST)

    assert "--template tap-counter" in content
    assert "--template flappy-mini" in content
    assert "--template swipe-runner" in content
    assert "--template puzzle-game" in content
    assert "--template quiz-game" in content
    assert "--template simple-physics" in content


def test_stabilization_checklist_links_manual_qa_docs():
    content = read(STABILIZATION_DOC)

    assert "Template Runtime Readiness" in content
    assert "TEMPLATE_RUNTIME_READINESS_PHASE56.md" in content
    assert "Template Manual QA Checklist" in content
    assert "TEMPLATE_MANUAL_QA_CHECKLIST.md" in content


def test_main_readme_links_phase56_docs():
    content = read(README)

    assert "Template Runtime Readiness - Phase 56" in content
    assert "docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md" in content
    assert "Template Manual QA Checklist" in content
    assert "docs/TEMPLATE_MANUAL_QA_CHECKLIST.md" in content


def test_health_checks_include_phase56_docs():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md" in paths
    assert "docs/TEMPLATE_MANUAL_QA_CHECKLIST.md" in paths
    assert "tests/test_template_runtime_readiness_phase56.py" in paths


def test_release_checks_include_phase56_docs():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert (
        "Required release file: "
        "docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md"
    ) in check_names

    assert (
        "Required release file: "
        "docs/TEMPLATE_MANUAL_QA_CHECKLIST.md"
    ) in check_names

    assert (
        "Required release test: "
        "tests/test_template_runtime_readiness_phase56.py"
    ) in check_names


def test_phase56_docs_have_balanced_markdown_fences():
    files = [
        RUNTIME_DOC,
        QA_CHECKLIST,
        STABILIZATION_DOC,
    ]

    for path in files:
        content = read(path)
        assert content.count("```") % 2 == 0
