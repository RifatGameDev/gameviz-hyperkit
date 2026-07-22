import json
from pathlib import Path

from hyperkit import generate_release_evidence_report

TEMPLATE_MAIN = Path(
    "src/hyperkit/templates/flappy_mini/main.py"
)

EVIDENCE_ROOT = Path(
    "docs/release-evidence/templates/flappy_mini"
)
TRACKER_PATH = Path("docs/release-evidence/qa-tracker.json")

MANUAL_RESULT = EVIDENCE_ROOT / "manual-qa-result.md"
VALIDATION_OUTPUT = EVIDENCE_ROOT / "validation-output.txt"
RUNTIME_NOTES = EVIDENCE_ROOT / "runtime-notes.md"
SCREENSHOT = EVIDENCE_ROOT / "screenshot.png"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_flappy_mini_runtime_evidence_files_exist():
    required_files = [
        MANUAL_RESULT,
        VALIDATION_OUTPUT,
        RUNTIME_NOTES,
        SCREENSHOT,
    ]

    for path in required_files:
        assert path.exists(), f"Missing evidence file: {path}"


def test_flappy_mini_screenshot_is_valid_png():
    content = SCREENSHOT.read_bytes()

    assert len(content) > 8
    assert content.startswith(b"\x89PNG\r\n\x1a\n")


def test_flappy_mini_tracker_entry_is_complete():
    tracker = json.loads(read(TRACKER_PATH))
    entry = tracker["templates"]["flappy_mini"]

    assert entry["status"] in {"pass", "pass_with_notes"}
    assert (
        entry["result_file"]
        == "templates/flappy_mini/manual-qa-result.md"
    )


def test_flappy_mini_manual_result_is_completed():
    content = read(MANUAL_RESULT)

    assert "Template name: Flappy Mini" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )
    assert "Approved for beta readiness: Yes" in content


def test_flappy_mini_runtime_notes_are_completed():
    content = read(RUNTIME_NOTES)

    assert "# Flappy Mini Runtime Notes" in content
    assert "Tap moved the bird upward: Yes" in content
    assert "Gravity moved the bird downward: Yes" in content
    assert "Pipe collision triggered game over: Yes" in content
    assert "Tap after game over restarted the game: Yes" in content
    assert (
        "Final result: PASS" in content
        or "Final result: PASS WITH NOTES" in content
    )


def test_flappy_mini_validation_output_is_not_empty():
    content = read(VALIDATION_OUTPUT)

    assert content.strip()
    assert "passed" in content.lower()


def test_flappy_mini_evidence_has_no_local_paths():
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


def test_release_evidence_report_marks_flappy_mini_complete():
    report = generate_release_evidence_report(".")

    assert "tap_counter" in report.complete_templates
    assert "flappy_mini" in report.complete_templates
    assert report.complete_count >= 2
    assert report.failed_count == 0


def test_flappy_mini_randomizes_pipe_gap_position():
    content = read(TEMPLATE_MAIN)

    assert "import random" in content
    assert "self.pipe_gap" in content
    assert "self.pipe_min_gap_center" in content
    assert "self.pipe_max_gap_center" in content
    assert "def _randomize_pipe_gap(self):" in content
    assert "random.randint(" in content
    assert "self._randomize_pipe_gap()" in content
