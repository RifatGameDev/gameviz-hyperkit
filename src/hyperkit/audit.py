from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .release import generate_release_report


@dataclass
class PreReleaseAuditCheck:
    name: str
    passed: bool
    message: str


@dataclass
class PreReleaseAuditReport:
    root: Path
    checks: list[PreReleaseAuditCheck] = field(default_factory=list)

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
            PreReleaseAuditCheck(
                name=name,
                passed=passed,
                message=message,
            )
        )


TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".toml",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
}

SCAN_FOLDERS = [
    "src",
    "tests",
    "docs",
    "examples",
]

FORBIDDEN_SCAN_IGNORE_FILES = {
    "tests/test_generated_project_smoke_phase37.py",
    "tests/test_tap_counter_polish_phase48.py",
    "tests/test_flappy_mini_polish_phase49.py",
    "tests/test_swipe_runner_polish_phase50.py",
    "tests/test_puzzle_game_polish_phase51.py",
}

REQUIRED_README_LINKS = [
    "docs/VERSION_HISTORY.md",
    "CHANGELOG.md",
    "docs/TEMPLATE_HELPERS.md",
    "docs/TEMPLATES.md",
    "docs/TEMPLATE_QUALITY_CHECKLIST.md",
    "docs/RELEASE_READINESS_CHECKLIST.md",
    "docs/GENERATED_PROJECT_SMOKE_TESTS.md",
    "docs/PROJECT_HEALTH_REPORT.md",
    "docs/RELEASE_BUILD_AUTOMATION.md",
    "docs/FINAL_PRE_RELEASE_AUDIT.md",
    "docs/QUICK_START_TUTORIAL.md",
    "docs/TEMPLATE_MEDIA_GUIDE.md",
    "docs/TEMPLATE_SCREENSHOTS.md",
    "docs/CLI_ERROR_MESSAGES.md",
    "docs/TEMPLATE_VALIDATION.md",
    "docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md",
    "docs/TAP_COUNTER_POLISH_PHASE48.md",
    "docs/FLAPPY_MINI_POLISH_PHASE49.md",
    "docs/SWIPE_RUNNER_POLISH_PHASE50.md",
    "docs/PUZZLE_GAME_POLISH_PHASE51.md",
]


def _forbidden_terms() -> list[str]:
    return [
        "D:" + "\\AI\\HyperKit\\gameviz-hyperkit",
        "/" + "mnt/data",
        "gameviz-hyperkit" + "\\src",
        "\\n\\n" + "## Documentation",
    ]


def _is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _markdown_fences_are_balanced(content: str) -> bool:
    return content.count("```") % 2 == 0


def _find_temp_scripts(root_path: Path) -> list[str]:
    temp_scripts: list[str] = []

    for path in root_path.glob("*.py"):
        name = path.name.lower()

        if name.startswith("create_phase"):
            temp_scripts.append(path.name)
        elif name.startswith("fix_phase"):
            temp_scripts.append(path.name)
        elif name.startswith("fix_"):
            temp_scripts.append(path.name)

    return sorted(temp_scripts)


def _iter_project_text_files(root_path: Path):
    root_files = [
        root_path / "README.md",
        root_path / "CHANGELOG.md",
        root_path / "pyproject.toml",
    ]

    for file_path in root_files:
        if file_path.exists() and file_path.is_file():
            yield file_path

    for folder_name in SCAN_FOLDERS:
        folder = root_path / folder_name

        if not folder.exists():
            continue

        for file_path in folder.rglob("*"):
            if file_path.is_file() and _is_text_file(file_path):
                yield file_path


def _find_forbidden_terms(root_path: Path) -> list[str]:
    findings: list[str] = []
    forbidden_terms = _forbidden_terms()

    for file_path in _iter_project_text_files(root_path):
        relative_path = file_path.relative_to(root_path).as_posix()

        if relative_path in FORBIDDEN_SCAN_IGNORE_FILES:
            continue

        content = _read_text(file_path)

        for term in forbidden_terms:
            if term in content:
                findings.append(f"{relative_path}: {term}")

    return findings


def _find_unbalanced_markdown(root_path: Path) -> list[str]:
    findings: list[str] = []

    markdown_files = [root_path / "README.md"]
    docs_dir = root_path / "docs"

    if docs_dir.exists():
        markdown_files.extend(docs_dir.glob("*.md"))

    for file_path in markdown_files:
        if not file_path.exists():
            continue

        content = _read_text(file_path)

        if not _markdown_fences_are_balanced(content):
            findings.append(file_path.relative_to(root_path).as_posix())

    return findings


def generate_pre_release_audit_report(root: str | Path = ".") -> PreReleaseAuditReport:
    root_path = Path(root).resolve()
    report = PreReleaseAuditReport(root=root_path)

    release_report = generate_release_report(root_path)

    report.add(
        name="Release readiness report",
        passed=release_report.passed,
        message=f"{release_report.passed_count}/{release_report.total} release checks passed",
    )

    report.add(
        name="Project root has pyproject.toml",
        passed=(root_path / "pyproject.toml").exists(),
        message="Found pyproject.toml",
    )

    report.add(
        name="Project root has README.md",
        passed=(root_path / "README.md").exists(),
        message="Found README.md",
    )

    temp_scripts = _find_temp_scripts(root_path)
    report.add(
        name="No temporary cleanup scripts",
        passed=len(temp_scripts) == 0,
        message="No temporary scripts found"
        if not temp_scripts
        else ", ".join(temp_scripts),
    )

    forbidden_findings = _find_forbidden_terms(root_path)
    report.add(
        name="No local machine paths leaked",
        passed=len(forbidden_findings) == 0,
        message="No forbidden local paths found"
        if not forbidden_findings
        else "; ".join(forbidden_findings[:5]),
    )

    unbalanced_markdown = _find_unbalanced_markdown(root_path)
    report.add(
        name="Markdown code fences are balanced",
        passed=len(unbalanced_markdown) == 0,
        message="All markdown fences balanced"
        if not unbalanced_markdown
        else ", ".join(unbalanced_markdown),
    )

    readme_path = root_path / "README.md"
    readme_content = _read_text(readme_path) if readme_path.exists() else ""

    report.add(
        name="README has no escaped newline artifacts",
        passed="\\n" not in readme_content,
        message="README has no literal escaped newline artifacts",
    )

    missing_readme_links = [
        link for link in REQUIRED_README_LINKS if link not in readme_content
    ]

    report.add(
        name="README links important docs",
        passed=len(missing_readme_links) == 0,
        message="All required docs linked"
        if not missing_readme_links
        else ", ".join(missing_readme_links),
    )

    final_doc = root_path / "docs" / "FINAL_PRE_RELEASE_AUDIT.md"
    report.add(
        name="Final audit documentation",
        passed=final_doc.exists(),
        message="Found docs/FINAL_PRE_RELEASE_AUDIT.md",
    )

    final_test = root_path / "tests" / "test_pre_release_audit_phase40.py"
    report.add(
        name="Final audit tests",
        passed=final_test.exists(),
        message="Found tests/test_pre_release_audit_phase40.py",
    )

    return report


def format_pre_release_audit_report(report: PreReleaseAuditReport) -> str:
    lines: list[str] = []

    lines.append("HyperKit Final Pre-release Audit")
    lines.append("=" * 35)
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
        lines.append("Final pre-release audit status: PASS")
        lines.append("Safe next commands:")
        lines.append("  pytest")
        lines.append("  hyperkit health")
        lines.append("  hyperkit release-check")
        lines.append("  python -m build")
        lines.append("  twine check dist/*")
    else:
        lines.append("Final pre-release audit status: FAIL")
        lines.append("Fix failed checks before preparing a release.")

    return "\n".join(lines)


def run_pre_release_audit(root: str | Path = ".") -> int:
    report = generate_pre_release_audit_report(root)
    print(format_pre_release_audit_report(report))
    return 0 if report.passed else 1
