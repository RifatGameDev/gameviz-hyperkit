from pathlib import Path


SUMMARY_DOC = Path("docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md")
CHECKLIST_DOC = Path("docs/TEMPLATE_STABILIZATION_CHECKLIST.md")
README = Path("README.md")

TEMPLATES_DISPLAY = [
    "Tap Counter",
    "Flappy Mini",
    "Swipe Runner",
    "Puzzle Game",
    "Quiz Game",
    "Simple Physics",
]

TEMPLATES_PACKAGE = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]

PHASES = [
    "Phase 48",
    "Phase 49",
    "Phase 50",
    "Phase 51",
    "Phase 52",
    "Phase 53",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_template_polish_summary_doc_exists():
    assert SUMMARY_DOC.exists()


def test_template_stabilization_checklist_doc_exists():
    assert CHECKLIST_DOC.exists()


def test_template_polish_summary_mentions_all_templates_and_phases():
    content = read(SUMMARY_DOC)

    assert "# Template Polish Summary - Phase 54" in content
    assert "Templates Polished" in content
    assert "Phase Coverage" in content

    for template in TEMPLATES_DISPLAY:
        assert template in content

    for phase in PHASES:
        assert phase in content


def test_template_polish_summary_mentions_common_improvements():
    content = read(SUMMARY_DOC)

    assert "clearer beginner-friendly code" in content
    assert "score and high-score display" in content
    assert "progress bar feedback" in content
    assert "camera shake feedback" in content
    assert "particle feedback" in content
    assert "improved template README files" in content


def test_template_polish_summary_mentions_helper_systems():
    content = read(SUMMARY_DOC)

    assert "AssetManager" in content
    assert "BoundsManager" in content
    assert "ScoreManager" in content
    assert "ProgressBar" in content
    assert "ParticleEmitter" in content
    assert "CameraShake" in content


def test_template_stabilization_checklist_mentions_all_templates():
    content = read(CHECKLIST_DOC)

    assert "# Template Stabilization Checklist" in content
    assert "Template List" in content

    for template in TEMPLATES_PACKAGE:
        assert template in content


def test_template_stabilization_checklist_has_required_sections():
    content = read(CHECKLIST_DOC)

    assert "## Code Stability Checklist" in content
    assert "## Gameplay Stability Checklist" in content
    assert "## Generated Project Checklist" in content
    assert "## Documentation Checklist" in content
    assert "## Media Checklist" in content
    assert "## Test Checklist" in content
    assert "## Beta-Ready Criteria" in content
    assert "## Stable-Ready Criteria" in content


def test_template_stabilization_checklist_mentions_validation_commands():
    content = read(CHECKLIST_DOC)

    assert "pytest" in content
    assert "hyperkit validate-templates" in content
    assert "hyperkit health" in content
    assert "hyperkit release-check" in content
    assert "hyperkit pre-release-audit" in content


def test_main_readme_links_phase54_docs():
    content = read(README)

    assert "Template Polish Summary - Phase 54" in content
    assert "docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md" in content
    assert "Template Stabilization Checklist" in content
    assert "docs/TEMPLATE_STABILIZATION_CHECKLIST.md" in content


def test_health_checks_include_phase54_docs():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md" in paths
    assert "docs/TEMPLATE_STABILIZATION_CHECKLIST.md" in paths
    assert "tests/test_template_polish_summary_phase54.py" in paths


def test_release_checks_include_phase54_docs():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md" in check_names
    assert "Required release file: docs/TEMPLATE_STABILIZATION_CHECKLIST.md" in check_names
    assert (
        "Required release test: tests/test_template_polish_summary_phase54.py"
        in check_names
    )


def test_phase54_docs_have_no_local_paths_or_escaped_newlines():
    files = [SUMMARY_DOC, CHECKLIST_DOC]

    forbidden_terms = [
        "D:\\AI\\HyperKit\\gameviz-hyperkit",
        "/mnt/data",
        "\\n\\n",
    ]

    for path in files:
        content = read(path)

        for term in forbidden_terms:
            assert term not in content
