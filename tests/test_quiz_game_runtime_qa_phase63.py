import json
from pathlib import Path

from hyperkit import generate_release_evidence_report


EVIDENCE_ROOT = Path(
    "docs/release-evidence/templates/quiz_game"
)
TRACKER_PATH = Path("docs/release-evidence/qa-tracker.json")

MANUAL_RESULT = EVIDENCE_ROOT / "manual-qa-result.md"
VALIDATION_OUTPUT = EVIDENCE_ROOT / "validation-output.txt"
RUNTIME_NOTES = EVIDENCE_ROOT / "runtime-notes.md"
SCREENSHOT = EVIDENCE_ROOT / "screenshot.png"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_quiz_game_runtime_evidence_files_exist():
    required_files = [
        MANUAL_RESULT,
        VALIDATION_OUTPUT,
        RUNTIME_NOTES,
        SCREENSHOT,
    ]

    for path in required_files:
        assert path.exists(), f"Missing evidence file: {path}"


def test_quiz_game_screenshot_is_valid_png():
    content = SCREENSHOT.read_bytes()

    assert len(content) > 8
    assert content.startswith(b"\x89PNG\r\n\x1a\n")


def test_quiz_game_tracker_entry_is_complete():
    tracker = json.loads(read(TRACKER_PATH))
    entry = tracker["templates"]["quiz_game"]

    assert entry["status"] in {"pass", "pass_with_notes"}
    assert (
        entry["result_file"]
        == "templates/quiz_game/manual-qa-result.md"
    )


def test_quiz_game_manual_result_is_completed():
    content = read(MANUAL_RESULT)

    assert "Template name: Quiz Game" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )
    assert "Approved for beta readiness: Yes" in content


def test_quiz_game_runtime_notes_are_completed():
    content = read(RUNTIME_NOTES)

    assert "# Quiz Game Runtime Notes" in content
    assert "Correct answers increased the score: Yes" in content
    assert "Wrong answers did not increase the score: Yes" in content
    assert "All four questions were reachable: Yes" in content
    assert "Tap after completion restarted the quiz: Yes" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )


def test_quiz_game_validation_output_is_not_empty():
    content = read(VALIDATION_OUTPUT)

    assert content.strip()
    assert "passed" in content.lower()


def test_quiz_game_evidence_has_no_local_paths():
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


def test_release_evidence_report_marks_quiz_game_complete():
    report = generate_release_evidence_report(".")

    expected_complete = {
        "tap_counter",
        "flappy_mini",
        "swipe_runner",
        "puzzle_game",
        "quiz_game",
    }

    assert expected_complete.issubset(
        set(report.complete_templates)
    )
    assert report.complete_count >= 5
    assert report.failed_count == 0
