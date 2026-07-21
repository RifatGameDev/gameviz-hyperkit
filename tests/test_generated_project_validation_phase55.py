from pathlib import Path

from hyperkit import (
    POLISHED_TEMPLATES,
    format_generated_project_validation_report,
    generate_generated_project_validation_report,
)


PHASE_DOC = Path("docs/GENERATED_PROJECT_VALIDATION_PHASE55.md")
STABILIZATION_DOC = Path("docs/TEMPLATE_STABILIZATION_CHECKLIST.md")
README = Path("README.md")


EXPECTED_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_polished_template_list_is_complete():
    assert POLISHED_TEMPLATES == EXPECTED_TEMPLATES


def test_generated_project_validation_passes_for_all_templates(tmp_path):
    report = generate_generated_project_validation_report(tmp_path)

    assert report.total == len(EXPECTED_TEMPLATES) * 10
    assert report.failed_count == 0
    assert report.passed


def test_generated_project_validation_contains_all_templates(tmp_path):
    report = generate_generated_project_validation_report(tmp_path)

    validated_templates = {
        check.template
        for check in report.checks
        if check.name == "Project generation"
    }

    assert validated_templates == set(EXPECTED_TEMPLATES)


def test_generated_project_validation_checks_required_files(tmp_path):
    report = generate_generated_project_validation_report(tmp_path)

    check_names = {check.name for check in report.checks}

    assert "Project generation" in check_names
    assert "Project directory exists" in check_names
    assert "main.py exists" in check_names
    assert "hyperkit.toml exists" in check_names
    assert "assets directory exists" in check_names
    assert "main.py syntax is valid" in check_names
    assert "main.py imports HyperKit" in check_names
    assert "main.py has game entry" in check_names
    assert "hyperkit.toml is valid" in check_names
    assert "No forbidden local paths" in check_names


def test_generated_project_validation_format_contains_summary(tmp_path):
    report = generate_generated_project_validation_report(tmp_path)
    output = format_generated_project_validation_report(report)

    assert "HyperKit Generated Project Validation" in output
    assert "Passed: 60/60" in output
    assert "Failed: 0" in output
    assert "Generated project validation status: PASS" in output


def test_generated_project_validation_doc_exists():
    assert PHASE_DOC.exists()

    content = read(PHASE_DOC)

    assert "# Generated Project Validation - Phase 55" in content
    assert "hyperkit validate-generated-projects" in content
    assert "main.py has valid Python syntax" in content
    assert "hyperkit.toml contains valid TOML" in content
    assert "does not start the Kivy game window" in content


def test_readme_documents_generated_project_validation():
    content = read(README)

    assert "hyperkit validate-generated-projects" in content
    assert "Generated Project Validation - Phase 55" in content
    assert "docs/GENERATED_PROJECT_VALIDATION_PHASE55.md" in content


def test_stabilization_checklist_mentions_generated_validation():
    content = read(STABILIZATION_DOC)

    assert "hyperkit validate-generated-projects" in content


def test_health_checks_include_generated_project_validation():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "src/hyperkit/generated_project_validation.py" in paths
    assert "docs/GENERATED_PROJECT_VALIDATION_PHASE55.md" in paths
    assert "tests/test_generated_project_validation_phase55.py" in paths


def test_release_checks_include_generated_project_validation():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert (
        "Required release file: "
        "src/hyperkit/generated_project_validation.py"
    ) in check_names

    assert (
        "Required release file: "
        "docs/GENERATED_PROJECT_VALIDATION_PHASE55.md"
    ) in check_names

    assert (
        "Required release test: "
        "tests/test_generated_project_validation_phase55.py"
    ) in check_names


def test_phase55_docs_have_balanced_markdown_fences():
    files = [
        PHASE_DOC,
        STABILIZATION_DOC,
    ]

    for path in files:
        content = read(path)
        assert content.count("```") % 2 == 0


def test_generated_projects_are_created_in_requested_work_path(tmp_path):
    report = generate_generated_project_validation_report(tmp_path)

    assert report.work_root == tmp_path.resolve()

    for template_name in EXPECTED_TEMPLATES:
        project_directory = tmp_path / f"phase55_{template_name}"
        assert project_directory.exists()
