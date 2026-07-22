import json
from pathlib import Path

from hyperkit import generate_release_evidence_report


EVIDENCE_ROOT = Path(
    "docs/release-evidence/templates/swipe_runner"
)
TRACKER_PATH = Path("docs/release-evidence/qa-tracker.json")

MANUAL_RESULT = EVIDENCE_ROOT / "manual-qa-result.md"
VALIDATION_OUTPUT = EVIDENCE_ROOT / "validation-output.txt"
RUNTIME_NOTES = EVIDENCE_ROOT / "runtime-notes.md"
SCREENSHOT = EVIDENCE_ROOT / "screenshot.png"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_swipe_runner_runtime_evidence_files_exist():
    required_files = [
        MANUAL_RESULT,
        VALIDATION_OUTPUT,
        RUNTIME_NOTES,
        SCREENSHOT,
    ]

    for path in required_files:
        assert path.exists(), f"Missing evidence file: {path}"


def test_swipe_runner_screenshot_is_valid_png():
    content = SCREENSHOT.read_bytes()

    assert len(content) > 8
    assert content.startswith(b"\x89PNG\r\n\x1a\n")


def test_swipe_runner_tracker_entry_is_complete():
    tracker = json.loads(read(TRACKER_PATH))
    entry = tracker["templates"]["swipe_runner"]

    assert entry["status"] in {"pass", "pass_with_notes"}
    assert (
        entry["result_file"]
        == "templates/swipe_runner/manual-qa-result.md"
    )


def test_swipe_runner_manual_result_is_completed():
    content = read(MANUAL_RESULT)

    assert "Template name: Swipe Runner" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )
    assert "Approved for beta readiness: Yes" in content


def test_swipe_runner_runtime_notes_are_completed():
    content = read(RUNTIME_NOTES)

    assert "# Swipe Runner Runtime Notes" in content
    assert "Swipe left changed the lane: Yes" in content
    assert "Swipe right changed the lane: Yes" in content
    assert "Collision triggered game over: Yes" in content
    assert "Tap after game over restarted the game: Yes" in content
    assert "Swipe after game over restarted the game: Yes" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )


def test_swipe_runner_validation_output_is_not_empty():
    content = read(VALIDATION_OUTPUT)

    assert content.strip()
    assert "passed" in content.lower()


def test_swipe_runner_evidence_has_no_local_paths():
    files = [
        MANUAL_RESULT,
        VALIDATION_OUTPUT,
        RUNTIME_NOTES,
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


def test_release_evidence_report_marks_swipe_runner_complete():
    report = generate_release_evidence_report(".")

    assert "tap_counter" in report.complete_templates
    assert "flappy_mini" in report.complete_templates
    assert "swipe_runner" in report.complete_templates
    assert report.complete_count >= 3
    assert report.failed_count == 0
