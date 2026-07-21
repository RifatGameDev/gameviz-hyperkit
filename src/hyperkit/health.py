from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class HealthCheck:
    name: str
    path: str
    passed: bool
    message: str


@dataclass
class HealthReport:
    root: Path
    checks: list[HealthCheck] = field(default_factory=list)

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

    def add_check(self, name: str, path: str, exists: bool) -> None:
        self.checks.append(
            HealthCheck(
                name=name,
                path=path,
                passed=exists,
                message="OK" if exists else "Missing",
            )
        )


REQUIRED_PATHS = {
    "Package metadata": "pyproject.toml",
    "Main README": "README.md",
    "Changelog": "CHANGELOG.md",
    "Templates documentation": "docs/TEMPLATES.md",
    "Template helper guide": "docs/TEMPLATE_HELPERS.md",
    "Template quality checklist": "docs/TEMPLATE_QUALITY_CHECKLIST.md",
    "Release readiness checklist": "docs/RELEASE_READINESS_CHECKLIST.md",
    "Version history": "docs/VERSION_HISTORY.md",
    "Generated project smoke docs": "docs/GENERATED_PROJECT_SMOKE_TESTS.md",
    "Package source": "src/hyperkit/__init__.py",
    "CLI source": "src/hyperkit/cli.py",
    "Templates folder": "src/hyperkit/templates",
    "Examples folder": "examples",
    "Tests folder": "tests",
    "Template quality tests": "tests/test_template_quality_phase34.py",
    "Release readiness tests": "tests/test_release_readiness_phase35.py",
    "Changelog tests": "tests/test_changelog_phase36.py",
    "Generated project smoke tests": "tests/test_generated_project_smoke_phase37.py",
    "Generated project smoke docs": "docs/GENERATED_PROJECT_SMOKE_TESTS.md",
    "Project health docs": "docs/PROJECT_HEALTH_REPORT.md",
    "Package source": "src/hyperkit/__init__.py",
    "Release build automation docs": "docs/RELEASE_BUILD_AUTOMATION.md",
    "Release build automation tests": "tests/test_release_check_phase39.py",
    "Generated project smoke tests": "tests/test_generated_project_smoke_phase37.py",
    "Release build automation tests": "tests/test_release_check_phase39.py",
    "Final pre-release audit docs": "docs/FINAL_PRE_RELEASE_AUDIT.md",
    "Final pre-release audit source": "src/hyperkit/audit.py",
    "Final pre-release audit tests": "tests/test_pre_release_audit_phase40.py",
    "Beginner quick-start tutorial": "docs/QUICK_START_TUTORIAL.md",
    "Beginner quick-start tutorial tests": "tests/test_quick_start_tutorial_phase43.py",
    "Public README tests": "tests/test_public_readme_phase42.py",
    "Template media guide": "docs/TEMPLATE_MEDIA_GUIDE.md",
    "Template screenshots documentation": "docs/TEMPLATE_SCREENSHOTS.md",
    "Template media tests": "tests/test_template_media_phase44.py",
    "Tap Counter media folder": "docs/media/templates/tap_counter/README.md",
    "Flappy Mini media folder": "docs/media/templates/flappy_mini/README.md",
    "Swipe Runner media folder": "docs/media/templates/swipe_runner/README.md",
    "Puzzle Game media folder": "docs/media/templates/puzzle_game/README.md",
    "Quiz Game media folder": "docs/media/templates/quiz_game/README.md",
    "Simple Physics media folder": "docs/media/templates/simple_physics/README.md",
    "CLI error message docs": "docs/CLI_ERROR_MESSAGES.md",
    "CLI error message tests": "tests/test_cli_error_messages_phase45.py",
    "Template validation source": "src/hyperkit/template_validation.py",
    "Template validation docs": "docs/TEMPLATE_VALIDATION.md",
    "Template validation tests": "tests/test_template_validation_phase46.py",
    "Production template polish checklist": "docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md",
    "Production template polish tests": "tests/test_production_template_polish_phase47.py",
    "Tap Counter polish docs": "docs/TAP_COUNTER_POLISH_PHASE48.md",
    "Tap Counter polish tests": "tests/test_tap_counter_polish_phase48.py",
    "Flappy Mini polish docs": "docs/FLAPPY_MINI_POLISH_PHASE49.md",
    "Flappy Mini polish tests": "tests/test_flappy_mini_polish_phase49.py",
    "Swipe Runner polish docs": "docs/SWIPE_RUNNER_POLISH_PHASE50.md",
    "Swipe Runner polish tests": "tests/test_swipe_runner_polish_phase50.py",
    "Puzzle Game polish docs": "docs/PUZZLE_GAME_POLISH_PHASE51.md",
    "Puzzle Game polish tests": "tests/test_puzzle_game_polish_phase51.py",
    "Quiz Game polish docs": "docs/QUIZ_GAME_POLISH_PHASE52.md",
    "Quiz Game polish tests": "tests/test_quiz_game_polish_phase52.py",
    "Simple Physics polish docs": "docs/SIMPLE_PHYSICS_POLISH_PHASE53.md",
    "Simple Physics polish tests": "tests/test_simple_physics_polish_phase53.py",
    "Template polish summary docs": "docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md",
    "Template stabilization checklist": "docs/TEMPLATE_STABILIZATION_CHECKLIST.md",
    "Template polish summary tests": "tests/test_template_polish_summary_phase54.py",
    "Generated project validation source": (
        "src/hyperkit/generated_project_validation.py"
    ),
    "Generated project validation docs": (
        "docs/GENERATED_PROJECT_VALIDATION_PHASE55.md"
    ),
    "Generated project validation tests": (
        "tests/test_generated_project_validation_phase55.py"
    ),
    "Template runtime readiness docs": (
        "docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md"
    ),
    "Template manual QA checklist": (
        "docs/TEMPLATE_MANUAL_QA_CHECKLIST.md"
    ),
    "Template runtime readiness tests": (
        "tests/test_template_runtime_readiness_phase56.py"
    ),
    "Manual QA result template": "docs/MANUAL_QA_RESULT_TEMPLATE.md",
    "Release evidence structure docs": "docs/RELEASE_EVIDENCE_STRUCTURE.md",
    "Release evidence workspace": "docs/release-evidence/README.md",
    "Release evidence tests": (
        "tests/test_release_evidence_phase57.py"
    ),

    "Release evidence validation source": (
        "src/hyperkit/release_evidence.py"
    ),
    "Runtime QA tracker docs": (
        "docs/RUNTIME_QA_TRACKER_PHASE58.md"
    ),
    "Runtime QA tracker data": (
        "docs/release-evidence/qa-tracker.json"
    ),
    "Runtime QA tracker tests": (
        "tests/test_runtime_qa_tracker_phase58.py"
    ),
}


REQUIRED_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


def generate_health_report(root: str | Path = ".") -> HealthReport:
    root_path = Path(root).resolve()
    report = HealthReport(root=root_path)

    for name, relative_path in REQUIRED_PATHS.items():
        path = root_path / relative_path
        report.add_check(name=name, path=relative_path, exists=path.exists())

    for template_name in REQUIRED_TEMPLATES:
        template_folder = root_path / "src" / "hyperkit" / "templates" / template_name
        main_file = template_folder / "main.py"
        readme_file = template_folder / "README.md"

        report.add_check(
            name=f"Template folder: {template_name}",
            path=template_folder.relative_to(root_path).as_posix(),
            exists=template_folder.exists(),
        )

        report.add_check(
            name=f"Template main.py: {template_name}",
            path=main_file.relative_to(root_path).as_posix(),
            exists=main_file.exists(),
        )

        report.add_check(
            name=f"Template README: {template_name}",
            path=readme_file.relative_to(root_path).as_posix(),
            exists=readme_file.exists(),
        )

    return report


def format_health_report(report: HealthReport) -> str:
    lines: list[str] = []

    lines.append("HyperKit Project Health Report")
    lines.append("=" * 32)
    lines.append(f"Root: {report.root}")
    lines.append("")
    lines.append(f"Passed: {report.passed_count}/{report.total}")
    lines.append(f"Failed: {report.failed_count}")
    lines.append("")

    for check in report.checks:
        status = "OK" if check.passed else "MISSING"
        lines.append(f"[{status}] {check.name} - {check.path}")

    lines.append("")

    if report.passed:
        lines.append("Project health status: PASS")
    else:
        lines.append("Project health status: FAIL")

    return "\n".join(lines)


def run_health_check(root: str | Path = ".") -> int:
    report = generate_health_report(root)
    print(format_health_report(report))
    return 0 if report.passed else 1
