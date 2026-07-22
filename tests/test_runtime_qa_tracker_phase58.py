import json
from pathlib import Path

from hyperkit import (
    ALLOWED_QA_STATUSES,
    TEMPLATE_DISPLAY_NAMES,
    format_release_evidence_report,
    generate_release_evidence_report,
    run_release_evidence_validation,
)


TRACKER_PATH = Path("docs/release-evidence/qa-tracker.json")
TRACKER_DOC = Path("docs/RUNTIME_QA_TRACKER_PHASE58.md")
EVIDENCE_STRUCTURE_DOC = Path("docs/RELEASE_EVIDENCE_STRUCTURE.md")
EVIDENCE_ROOT_README = Path("docs/release-evidence/README.md")
MANUAL_QA_CHECKLIST = Path("docs/TEMPLATE_MANUAL_QA_CHECKLIST.md")
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


def test_runtime_qa_tracker_exists():
    assert TRACKER_PATH.exists()


def test_runtime_qa_tracker_contains_valid_json():
    tracker = json.loads(read(TRACKER_PATH))

    assert tracker["schema_version"] == 1
    assert isinstance(tracker["templates"], dict)


def test_runtime_qa_tracker_contains_all_templates():
    tracker = json.loads(read(TRACKER_PATH))
    templates = tracker["templates"]

    assert list(templates.keys()) == EXPECTED_TEMPLATES
    assert list(TEMPLATE_DISPLAY_NAMES.keys()) == EXPECTED_TEMPLATES


def test_runtime_qa_tracker_uses_allowed_statuses():
    tracker = json.loads(read(TRACKER_PATH))

    for template_entry in tracker["templates"].values():
        assert template_entry["status"] in ALLOWED_QA_STATUSES


def test_runtime_qa_tracker_supports_incremental_progress():
    tracker = json.loads(read(TRACKER_PATH))
    statuses = {
        template_entry["status"]
        for template_entry in tracker["templates"].values()
    }

    assert statuses
    assert statuses.issubset(ALLOWED_QA_STATUSES)


def test_release_evidence_structure_validation_passes():
    report = generate_release_evidence_report(".")

    assert report.total > 0
    assert report.failed_count == 0
    assert report.passed


def test_release_evidence_progress_counts_are_consistent():
    report = generate_release_evidence_report(".")

    tracked_total = (
        report.complete_count
        + report.pending_count
        + report.qa_failed_count
    )

    assert tracked_total == len(EXPECTED_TEMPLATES)


def test_release_evidence_report_contains_progress_summary():
    report = generate_release_evidence_report(".")
    output = format_release_evidence_report(report)

    assert "HyperKit Release Evidence Validation" in output
    assert "Structure checks failed: 0" in output
    assert "Completed QA evidence:" in output
    assert f"/{len(EXPECTED_TEMPLATES)}" in output
    assert "Evidence structure validation status: PASS" in output
    assert "Evidence completion status:" in output


def test_development_evidence_validation_returns_success():
    result = run_release_evidence_validation(
        ".",
        require_complete=False,
    )

    assert result == 0


def test_strict_evidence_validation_matches_completion_state():
    report = generate_release_evidence_report(".")

    result = run_release_evidence_validation(
        ".",
        require_complete=True,
    )

    expected_result = 0 if report.all_complete else 1

    assert result == expected_result


def test_runtime_qa_tracker_doc_exists():
    assert TRACKER_DOC.exists()

    content = read(TRACKER_DOC)

    assert "# Runtime QA Tracker - Phase 58" in content
    assert "hyperkit validate-release-evidence" in content
    assert "--require-complete" in content
    assert "pass_with_notes" in content


def test_release_evidence_docs_mention_validation_command():
    files = [
        EVIDENCE_STRUCTURE_DOC,
        EVIDENCE_ROOT_README,
        MANUAL_QA_CHECKLIST,
    ]

    for path in files:
        content = read(path)
        assert "hyperkit validate-release-evidence" in content


def test_main_readme_documents_release_evidence_validation():
    content = read(README)

    assert "hyperkit validate-release-evidence" in content
    assert "Runtime QA Tracker - Phase 58" in content
    assert "docs/RUNTIME_QA_TRACKER_PHASE58.md" in content


def test_health_checks_include_phase58_files():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "src/hyperkit/release_evidence.py" in paths
    assert "docs/RUNTIME_QA_TRACKER_PHASE58.md" in paths
    assert "docs/release-evidence/qa-tracker.json" in paths
    assert "tests/test_runtime_qa_tracker_phase58.py" in paths


def test_release_checks_include_phase58_files():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert (
        "Required release file: src/hyperkit/release_evidence.py"
        in check_names
    )

    assert (
        "Required release file: docs/RUNTIME_QA_TRACKER_PHASE58.md"
        in check_names
    )

    assert (
        "Required release file: docs/release-evidence/qa-tracker.json"
        in check_names
    )

    assert (
        "Required release test: tests/test_runtime_qa_tracker_phase58.py"
        in check_names
    )


def test_phase58_markdown_fences_are_balanced():
    files = [
        TRACKER_DOC,
        EVIDENCE_STRUCTURE_DOC,
        EVIDENCE_ROOT_README,
        MANUAL_QA_CHECKLIST,
        README,
    ]

    for path in files:
        content = read(path)
        assert content.count("```") % 2 == 0
