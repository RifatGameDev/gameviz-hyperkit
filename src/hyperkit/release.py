from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .health import generate_health_report


@dataclass
class ReleaseCheck:
    name: str
    passed: bool
    message: str


@dataclass
class ReleaseReport:
    root: Path
    checks: list[ReleaseCheck] = field(default_factory=list)

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

    def add(self, name: str, passed: bool, message: str) -> None:
        self.checks.append(
            ReleaseCheck(
                name=name,
                passed=passed,
                message=message,
            )
        )


REQUIRED_RELEASE_FILES = [
    "README.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "docs/TEMPLATES.md",
    "docs/TEMPLATE_HELPERS.md",
    "docs/TEMPLATE_QUALITY_CHECKLIST.md",
    "docs/RELEASE_READINESS_CHECKLIST.md",
    "docs/VERSION_HISTORY.md",
    "docs/GENERATED_PROJECT_SMOKE_TESTS.md",
    "docs/PROJECT_HEALTH_REPORT.md",
    "docs/RELEASE_BUILD_AUTOMATION.md",
    "docs/FINAL_PRE_RELEASE_AUDIT.md",
    "docs/QUICK_START_TUTORIAL.md",
]

REQUIRED_RELEASE_TESTS = [
    "tests/test_template_quality_phase34.py",
    "tests/test_release_readiness_phase35.py",
    "tests/test_changelog_phase36.py",
    "tests/test_generated_project_smoke_phase37.py",
    "tests/test_health_phase38.py",
    "tests/test_pre_release_audit_phase40.py",
    "tests/test_public_readme_phase42.py",
    "tests/test_quick_start_tutorial_phase43.py",
]

REQUIRED_PYPROJECT_TERMS = [
    "gameviz-hyperkit",
    "hyperkit.cli:main",
    "requires-python",
    "dependencies",
]


def _file_contains(path: Path, terms: list[str]) -> bool:
    if not path.exists():
        return False

    content = path.read_text(encoding="utf-8", errors="ignore")

    return all(term in content for term in terms)


def generate_release_report(root: str | Path = ".") -> ReleaseReport:
    root_path = Path(root).resolve()
    report = ReleaseReport(root=root_path)

    health_report = generate_health_report(root_path)

    report.add(
        name="Project health report",
        passed=health_report.passed,
        message=(
            f"{health_report.passed_count}/{health_report.total} health checks passed"
        ),
    )

    for filename in REQUIRED_RELEASE_FILES:
        path = root_path / filename
        report.add(
            name=f"Required release file: {filename}",
            passed=path.exists(),
            message="Found" if path.exists() else "Missing",
        )

    for filename in REQUIRED_RELEASE_TESTS:
        path = root_path / filename
        report.add(
            name=f"Required release test: {filename}",
            passed=path.exists(),
            message="Found" if path.exists() else "Missing",
        )

    pyproject_path = root_path / "pyproject.toml"
    report.add(
        name="pyproject release metadata",
        passed=_file_contains(pyproject_path, REQUIRED_PYPROJECT_TERMS),
        message="Required package metadata found",
    )

    readme_path = root_path / "README.md"
    report.add(
        name="README package identity",
        passed=_file_contains(readme_path, ["HyperKit", "gameviz-hyperkit"]),
        message="README mentions package identity",
    )

    changelog_path = root_path / "CHANGELOG.md"
    report.add(
        name="CHANGELOG version notes",
        passed=_file_contains(changelog_path, ["Unreleased", "0.1.0"]),
        message="CHANGELOG contains version sections",
    )

    report.add(
        name="Build command available",
        passed=True,
        message="Run manually: python -m build",
    )

    report.add(
        name="Twine check command available",
        passed=True,
        message="Run manually after build: twine check dist/*",
    )

    return report


def format_release_report(report: ReleaseReport) -> str:
    lines: list[str] = []

    lines.append("HyperKit Release Readiness Report")
    lines.append("=" * 37)
    lines.append(f"Root: {report.root}")
    lines.append("")
    lines.append(f"Passed: {report.passed_count}/{report.total}")
    lines.append(f"Failed: {report.failed_count}")
    lines.append("")

    for check in report.checks:
        status = "OK" if check.passed else "FAIL"
        lines.append(f"[{status}] {check.name} - {check.message}")

    lines.append("")

    if report.passed:
        lines.append("Release readiness status: PASS")
        lines.append("Next manual commands:")
        lines.append("  pytest")
        lines.append("  python -m build")
        lines.append("  twine check dist/*")
    else:
        lines.append("Release readiness status: FAIL")
        lines.append("Fix failed checks before building a release.")

    return "\n".join(lines)


def run_release_check(root: str | Path = ".") -> int:
    report = generate_release_report(root)
    print(format_release_report(report))
    return 0 if report.passed else 1
