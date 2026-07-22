import json
from pathlib import Path

from hyperkit import generate_release_evidence_report


EVIDENCE_ROOT = Path(
    "docs/release-evidence/templates/tap_counter"
)
TRACKER_PATH = Path("docs/release-evidence/qa-tracker.json")

MANUAL_RESULT = EVIDENCE_ROOT / "manual-qa-result.md"
VALIDATION_OUTPUT = EVIDENCE_ROOT / "validation-output.txt"
RUNTIME_NOTES = EVIDENCE_ROOT / "runtime-notes.md"
SCREENSHOT = EVIDENCE_ROOT / "screenshot.png"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_tap_counter_runtime_evidence_files_exist():
    required_files = [
        MANUAL_RESULT,
        VALIDATION_OUTPUT,
        RUNTIME_NOTES,
        SCREENSHOT,
    ]

    for path in required_files:
        assert path.exists(), f"Missing evidence file: {path}"


def test_tap_counter_screenshot_is_not_empty():
    assert SCREENSHOT.stat().st_size > 0


def test_tap_counter_tracker_entry_is_complete():
    tracker = json.loads(read(TRACKER_PATH))
    entry = tracker["templates"]["tap_counter"]

    assert entry["status"] in {"pass", "pass_with_notes"}
    assert (
        entry["result_file"]
        == "templates/tap_counter/manual-qa-result.md"
    )


def test_tap_counter_manual_result_is_completed():
    content = read(MANUAL_RESULT)

    assert "Template name: Tap Counter" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )
    assert "Approved for beta readiness: Yes" in content


def test_tap_counter_runtime_notes_are_completed():
    content = read(RUNTIME_NOTES)

    assert "# Tap Counter Runtime Notes" in content
    assert "Tap input worked: Yes" in content
    assert "Score increased correctly: Yes" in content
    assert "High score persisted after restarting" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )


def test_tap_counter_validation_output_is_not_empty():
    content = read(VALIDATION_OUTPUT)

    assert content.strip()
    assert "passed" in content.lower()


def test_tap_counter_evidence_has_no_repository_absolute_path():
    files = [
        MANUAL_RESULT,
        VALIDATION_OUTPUT,
        RUNTIME_NOTES,
    ]

    forbidden = "D:" + "\\AI\\HyperKit\\gameviz-hyperkit"

    for path in files:
        assert forbidden not in read(path)


def test_release_evidence_report_marks_tap_counter_complete():
    report = generate_release_evidence_report(".")

    assert "tap_counter" in report.complete_templates
    assert report.complete_count >= 1
    assert report.failed_count == 0
