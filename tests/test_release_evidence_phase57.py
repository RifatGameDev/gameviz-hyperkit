from pathlib import Path


QA_RESULT_TEMPLATE = Path("docs/MANUAL_QA_RESULT_TEMPLATE.md")
EVIDENCE_STRUCTURE_DOC = Path("docs/RELEASE_EVIDENCE_STRUCTURE.md")
EVIDENCE_ROOT_README = Path("docs/release-evidence/README.md")
MANUAL_QA_CHECKLIST = Path("docs/TEMPLATE_MANUAL_QA_CHECKLIST.md")
STABILIZATION_CHECKLIST = Path("docs/TEMPLATE_STABILIZATION_CHECKLIST.md")
README = Path("README.md")


TEMPLATES = {
    "tap_counter": "Tap Counter",
    "flappy_mini": "Flappy Mini",
    "swipe_runner": "Swipe Runner",
    "puzzle_game": "Puzzle Game",
    "quiz_game": "Quiz Game",
    "simple_physics": "Simple Physics",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_manual_qa_result_template_exists():
    assert QA_RESULT_TEMPLATE.exists()


def test_release_evidence_structure_doc_exists():
    assert EVIDENCE_STRUCTURE_DOC.exists()


def test_release_evidence_root_readme_exists():
    assert EVIDENCE_ROOT_README.exists()


def test_manual_qa_result_template_has_required_sections():
    content = read(QA_RESULT_TEMPLATE)

    assert "# Manual QA Result Template" in content
    assert "## Test Information" in content
    assert "## Automated Validation Results" in content
    assert "## Runtime Startup Result" in content
    assert "## Gameplay Result" in content
    assert "## Visual and Layout Result" in content
    assert "## Repeatability Result" in content
    assert "## Issues Found" in content
    assert "## Evidence Files" in content
    assert "## Final Decision" in content
    assert "## Sign-Off" in content


def test_manual_qa_result_template_has_result_options():
    content = read(QA_RESULT_TEMPLATE)

    assert "PASS" in content
    assert "PASS WITH NOTES" in content
    assert "FAIL" in content
    assert "Approved for beta readiness" in content
    assert "Approved for stable readiness" in content


def test_release_evidence_structure_mentions_expected_files():
    content = read(EVIDENCE_STRUCTURE_DOC)

    assert "manual-qa-result.md" in content
    assert "validation-output.txt" in content
    assert "runtime-notes.md" in content
    assert "screenshot.png" in content
    assert "demo.gif" in content
    assert "issue-notes.md" in content


def test_release_evidence_structure_mentions_all_templates():
    content = read(EVIDENCE_STRUCTURE_DOC)

    for template_name in TEMPLATES:
        assert template_name in content


def test_all_template_evidence_directories_exist():
    root = Path("docs/release-evidence/templates")

    for template_name in TEMPLATES:
        template_folder = root / template_name
        assert template_folder.exists()
        assert template_folder.is_dir()


def test_all_template_evidence_readmes_exist():
    root = Path("docs/release-evidence/templates")

    for template_name, display_name in TEMPLATES.items():
        readme = root / template_name / "README.md"

        assert readme.exists()

        content = read(readme)

        assert display_name in content
        assert "manual-qa-result.md" in content
        assert "validation-output.txt" in content
        assert "screenshot.png" in content


def test_manual_qa_checklist_links_result_and_evidence_docs():
    content = read(MANUAL_QA_CHECKLIST)

    assert "Manual QA Result Template" in content
    assert "MANUAL_QA_RESULT_TEMPLATE.md" in content
    assert "Release Evidence Workspace" in content
    assert "release-evidence/README.md" in content


def test_stabilization_checklist_links_result_and_evidence_docs():
    content = read(STABILIZATION_CHECKLIST)

    assert "Manual QA Result Template" in content
    assert "MANUAL_QA_RESULT_TEMPLATE.md" in content
    assert "Release Evidence Structure" in content
    assert "RELEASE_EVIDENCE_STRUCTURE.md" in content
    assert "Release Evidence Workspace" in content
    assert "release-evidence/README.md" in content


def test_main_readme_links_phase57_docs():
    content = read(README)

    assert "Manual QA Result Template" in content
    assert "docs/MANUAL_QA_RESULT_TEMPLATE.md" in content
    assert "Release Evidence Structure" in content
    assert "docs/RELEASE_EVIDENCE_STRUCTURE.md" in content
    assert "Release Evidence Workspace" in content
    assert "docs/release-evidence/README.md" in content


def test_health_checks_include_phase57_files():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/MANUAL_QA_RESULT_TEMPLATE.md" in paths
    assert "docs/RELEASE_EVIDENCE_STRUCTURE.md" in paths
    assert "docs/release-evidence/README.md" in paths
    assert "tests/test_release_evidence_phase57.py" in paths


def test_release_checks_include_phase57_files():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    required_files = [
        "docs/MANUAL_QA_RESULT_TEMPLATE.md",
        "docs/RELEASE_EVIDENCE_STRUCTURE.md",
        "docs/release-evidence/README.md",
        "docs/release-evidence/templates/tap_counter/README.md",
        "docs/release-evidence/templates/flappy_mini/README.md",
        "docs/release-evidence/templates/swipe_runner/README.md",
        "docs/release-evidence/templates/puzzle_game/README.md",
        "docs/release-evidence/templates/quiz_game/README.md",
        "docs/release-evidence/templates/simple_physics/README.md",
    ]

    for required_file in required_files:
        assert f"Required release file: {required_file}" in check_names

    assert (
        "Required release test: tests/test_release_evidence_phase57.py"
        in check_names
    )


def test_phase57_markdown_fences_are_balanced():
    files = [
        QA_RESULT_TEMPLATE,
        EVIDENCE_STRUCTURE_DOC,
        EVIDENCE_ROOT_README,
        MANUAL_QA_CHECKLIST,
        STABILIZATION_CHECKLIST,
    ]

    for path in files:
        content = read(path)
        assert content.count("```") % 2 == 0
