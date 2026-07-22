import json
from pathlib import Path

from hyperkit import generate_release_evidence_report


TRACKER_PATH = Path("docs/release-evidence/qa-tracker.json")
CERTIFICATION_DOCUMENT = Path(
    "docs/release-evidence/FINAL_QA_CERTIFICATION_PHASE65.md"
)
CERTIFICATION_OUTPUT = Path(
    "docs/release-evidence/final-certification-output.txt"
)

EXPECTED_TEMPLATES = {
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_all_six_templates_have_completed_statuses():
    tracker = json.loads(read(TRACKER_PATH))
    templates = tracker["templates"]

    assert set(templates) == EXPECTED_TEMPLATES

    for template_name, entry in templates.items():
        assert entry["status"] in {
            "pass",
            "pass_with_notes",
        }, f"{template_name} is not complete"

        assert entry["result_file"]


def test_release_evidence_report_is_fully_complete():
    report = generate_release_evidence_report(".")

    assert set(report.complete_templates) == EXPECTED_TEMPLATES
    assert report.complete_count == 6
    assert report.failed_count == 0
    assert report.all_complete


def test_final_certification_document_exists():
    assert CERTIFICATION_DOCUMENT.exists()

    content = read(CERTIFICATION_DOCUMENT)

    assert "# HyperKit Final QA Certification" in content
    assert (
        "Certification status: READY FOR TESTPYPI RC"
        in content
    )
    assert "Current validated version: 0.1.1.dev1" in content
    assert "Planned release candidate: 0.1.1rc1" in content
    assert (
        "Approved for TestPyPI release candidate preparation: Yes"
        in content
    )
    assert "Approved for stable PyPI publication: No" in content


def test_all_template_names_are_in_certification_document():
    content = read(CERTIFICATION_DOCUMENT)

    required_names = [
        "Tap Counter",
        "Flappy Mini",
        "Swipe Runner",
        "Puzzle Game",
        "Quiz Game",
        "Simple Physics",
    ]

    for name in required_names:
        assert name in content


def test_certification_output_exists_and_is_not_empty():
    assert CERTIFICATION_OUTPUT.exists()
    assert read(CERTIFICATION_OUTPUT).strip()


def test_certification_files_have_no_local_machine_paths():
    files = [
        CERTIFICATION_DOCUMENT,
        CERTIFICATION_OUTPUT,
    ]

    forbidden_terms = [
        "D:" + "\\AI\\HyperKit\\gameviz-hyperkit",
        "gameviz-hyperkit" + "\\src",
        "/" + "mnt/data",
    ]

    for path in files:
        content = read(path)

        for forbidden_term in forbidden_terms:
            assert forbidden_term not in content
