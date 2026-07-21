from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


TEMPLATE_DISPLAY_NAMES = {
    "tap_counter": "Tap Counter",
    "flappy_mini": "Flappy Mini",
    "swipe_runner": "Swipe Runner",
    "puzzle_game": "Puzzle Game",
    "quiz_game": "Quiz Game",
    "simple_physics": "Simple Physics",
}


ALLOWED_QA_STATUSES = {
    "pending",
    "in_progress",
    "pass",
    "pass_with_notes",
    "fail",
}


PASSING_QA_STATUSES = {
    "pass",
    "pass_with_notes",
}


REQUIRED_PASS_EVIDENCE = [
    "manual-qa-result.md",
    "validation-output.txt",
    "runtime-notes.md",
    "screenshot.png",
]


REQUIRED_FAIL_EVIDENCE = [
    "manual-qa-result.md",
    "validation-output.txt",
    "runtime-notes.md",
    "issue-notes.md",
]


@dataclass
class ReleaseEvidenceCheck:
    name: str
    passed: bool
    message: str
    template: str | None = None


@dataclass
class ReleaseEvidenceReport:
    root: Path
    checks: list[ReleaseEvidenceCheck] = field(default_factory=list)
    template_statuses: dict[str, str] = field(default_factory=dict)
    complete_templates: list[str] = field(default_factory=list)
    pending_templates: list[str] = field(default_factory=list)
    failed_templates: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    @property
    def total(self) -> int:
        return len(self.checks)

    @property
    def passed_count(self) -> int:
        return sum(1 for check in self.checks if check.passed)

    @property
    def failed_count(self) -> int:
        return self.total - self.passed_count

    @property
    def template_count(self) -> int:
        return len(TEMPLATE_DISPLAY_NAMES)

    @property
    def complete_count(self) -> int:
        return len(self.complete_templates)

    @property
    def pending_count(self) -> int:
        return len(self.pending_templates)

    @property
    def qa_failed_count(self) -> int:
        return len(self.failed_templates)

    @property
    def all_complete(self) -> bool:
        return (
            self.passed
            and self.complete_count == self.template_count
            and self.qa_failed_count == 0
        )

    def add(
        self,
        name: str,
        passed: bool,
        message: str,
        template: str | None = None,
    ) -> None:
        self.checks.append(
            ReleaseEvidenceCheck(
                name=name,
                passed=passed,
                message=message,
                template=template,
            )
        )


def _read_json(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    parsed = json.loads(content)

    if not isinstance(parsed, dict):
        raise ValueError("Tracker root must be a JSON object.")

    return parsed


def _required_evidence_for_status(status: str) -> list[str]:
    if status in PASSING_QA_STATUSES:
        return REQUIRED_PASS_EVIDENCE

    if status == "fail":
        return REQUIRED_FAIL_EVIDENCE

    return []


def _validate_tracker_file(
    report: ReleaseEvidenceReport,
    tracker_path: Path,
) -> dict[str, Any] | None:
    report.add(
        name="QA tracker exists",
        passed=tracker_path.exists(),
        message=str(tracker_path),
    )

    if not tracker_path.exists():
        return None

    try:
        tracker = _read_json(tracker_path)

        report.add(
            name="QA tracker contains valid JSON",
            passed=True,
            message="Valid JSON tracker",
        )

        return tracker
    except (json.JSONDecodeError, ValueError) as exc:
        report.add(
            name="QA tracker contains valid JSON",
            passed=False,
            message=f"{type(exc).__name__}: {exc}",
        )

        return None


def _validate_tracker_metadata(
    report: ReleaseEvidenceReport,
    tracker: dict[str, Any],
) -> dict[str, Any] | None:
    schema_version = tracker.get("schema_version")

    report.add(
        name="QA tracker schema version",
        passed=schema_version == 1,
        message=f"schema_version={schema_version}",
    )

    templates = tracker.get("templates")
    templates_valid = isinstance(templates, dict)

    report.add(
        name="QA tracker templates section",
        passed=templates_valid,
        message=(
            "Templates section found"
            if templates_valid
            else "Missing or invalid templates section"
        ),
    )

    if not templates_valid:
        return None

    return templates


def _validate_template_entry(
    report: ReleaseEvidenceReport,
    template_name: str,
    display_name: str,
    entry: Any,
    evidence_root: Path,
) -> None:
    entry_valid = isinstance(entry, dict)

    report.add(
        name="Tracker entry exists",
        passed=entry_valid,
        message=(
            "Tracker entry found"
            if entry_valid
            else "Missing or invalid tracker entry"
        ),
        template=template_name,
    )

    if not entry_valid:
        return

    tracked_display_name = entry.get("display_name")
    display_name_valid = tracked_display_name == display_name

    report.add(
        name="Tracker display name",
        passed=display_name_valid,
        message=f"display_name={tracked_display_name}",
        template=template_name,
    )

    status = entry.get("status")
    status_valid = status in ALLOWED_QA_STATUSES

    report.add(
        name="Tracker status",
        passed=status_valid,
        message=f"status={status}",
        template=template_name,
    )

    if not status_valid:
        return

    report.template_statuses[template_name] = status

    template_folder = evidence_root / "templates" / template_name
    folder_exists = template_folder.exists() and template_folder.is_dir()

    report.add(
        name="Evidence folder exists",
        passed=folder_exists,
        message=str(template_folder),
        template=template_name,
    )

    readme_path = template_folder / "README.md"

    report.add(
        name="Evidence folder README exists",
        passed=readme_path.exists(),
        message=str(readme_path),
        template=template_name,
    )

    required_files = _required_evidence_for_status(status)
    missing_files = [
        filename
        for filename in required_files
        if not (template_folder / filename).exists()
    ]

    if status in PASSING_QA_STATUSES:
        evidence_complete = len(missing_files) == 0

        report.add(
            name="Passing QA evidence is complete",
            passed=evidence_complete,
            message=(
                "All required passing evidence found"
                if evidence_complete
                else f"Missing: {', '.join(missing_files)}"
            ),
            template=template_name,
        )

        result_file = entry.get("result_file", "")
        result_file_valid = isinstance(
            result_file, str) and bool(result_file.strip())

        report.add(
            name="Tracker result file is recorded",
            passed=result_file_valid,
            message=(
                result_file
                if result_file_valid
                else "Result file path is missing"
            ),
            template=template_name,
        )

        if evidence_complete and result_file_valid:
            report.complete_templates.append(template_name)

    elif status == "fail":
        evidence_complete = len(missing_files) == 0

        report.add(
            name="Failed QA evidence is complete",
            passed=evidence_complete,
            message=(
                "All required failure evidence found"
                if evidence_complete
                else f"Missing: {', '.join(missing_files)}"
            ),
            template=template_name,
        )

        report.failed_templates.append(template_name)

    else:
        report.add(
            name="Incomplete QA status is allowed",
            passed=True,
            message="Runtime QA evidence is not yet required",
            template=template_name,
        )

        report.pending_templates.append(template_name)


def generate_release_evidence_report(
    root: str | Path = ".",
) -> ReleaseEvidenceReport:
    root_path = Path(root).resolve()
    report = ReleaseEvidenceReport(root=root_path)

    evidence_root = root_path / "docs" / "release-evidence"
    tracker_path = evidence_root / "qa-tracker.json"

    report.add(
        name="Release evidence root exists",
        passed=evidence_root.exists(),
        message=str(evidence_root),
    )

    tracker = _validate_tracker_file(report, tracker_path)

    if tracker is None:
        return report

    templates = _validate_tracker_metadata(report, tracker)

    if templates is None:
        return report

    for template_name, display_name in TEMPLATE_DISPLAY_NAMES.items():
        entry = templates.get(template_name)

        _validate_template_entry(
            report=report,
            template_name=template_name,
            display_name=display_name,
            entry=entry,
            evidence_root=evidence_root,
        )

    unexpected_templates = sorted(
        set(templates.keys()) - set(TEMPLATE_DISPLAY_NAMES.keys())
    )

    report.add(
        name="QA tracker has no unexpected templates",
        passed=len(unexpected_templates) == 0,
        message=(
            "No unexpected templates"
            if not unexpected_templates
            else f"Unexpected: {', '.join(unexpected_templates)}"
        ),
    )

    return report


def format_release_evidence_report(
    report: ReleaseEvidenceReport,
) -> str:
    lines: list[str] = []

    lines.append("HyperKit Release Evidence Validation")
    lines.append("=" * 36)
    lines.append(f"Root: {report.root}")
    lines.append("")
    lines.append(
        f"Structure checks passed: "
        f"{report.passed_count}/{report.total}"
    )
    lines.append(f"Structure checks failed: {report.failed_count}")
    lines.append("")
    lines.append(
        f"Completed QA evidence: "
        f"{report.complete_count}/{report.template_count}"
    )
    lines.append(f"Pending or in progress: {report.pending_count}")
    lines.append(f"Failed QA results: {report.qa_failed_count}")
    lines.append("")

    for check in report.checks:
        status = "OK" if check.passed else "FAIL"
        template_prefix = (
            f"{check.template} - "
            if check.template is not None
            else ""
        )

        lines.append(
            f"[{status}] {template_prefix}"
            f"{check.name} - {check.message}"
        )

    lines.append("")

    if not report.passed:
        lines.append("Evidence structure validation status: FAIL")
        lines.append("Fix the failed evidence structure checks.")
    else:
        lines.append("Evidence structure validation status: PASS")

        if report.all_complete:
            lines.append("Evidence completion status: COMPLETE")
        else:
            lines.append("Evidence completion status: IN PROGRESS")

    return "\n".join(lines)


def run_release_evidence_validation(
    root: str | Path = ".",
    require_complete: bool = False,
) -> int:
    report = generate_release_evidence_report(root)

    print(format_release_evidence_report(report))

    if not report.passed:
        return 1

    if require_complete and not report.all_complete:
        print("")
        print(
            "Strict evidence validation failed: "
            "runtime QA evidence is not complete."
        )
        return 1

    return 0
