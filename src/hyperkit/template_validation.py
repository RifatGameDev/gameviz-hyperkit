from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TemplateValidationCheck:
    template: str
    name: str
    passed: bool
    message: str


@dataclass
class TemplateValidationReport:
    root: Path
    checks: list[TemplateValidationCheck] = field(default_factory=list)

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

    def add(self, template: str, name: str, passed: bool, message: str) -> None:
        self.checks.append(
            TemplateValidationCheck(
                template=template,
                name=name,
                passed=passed,
                message=message,
            )
        )


EXPECTED_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


FORBIDDEN_TEMPLATE_TERMS = [
    "D:" + "\\AI\\HyperKit\\gameviz-hyperkit",
    "/" + "mnt/data",
    "gameviz-hyperkit" + "\\src",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _template_root(root_path: Path) -> Path:
    return root_path / "src" / "hyperkit" / "templates"


def _validate_template_folder(
    report: TemplateValidationReport,
    template_name: str,
    template_folder: Path,
) -> None:
    report.add(
        template=template_name,
        name="Template folder exists",
        passed=template_folder.exists(),
        message=str(template_folder),
    )


def _validate_required_files(
    report: TemplateValidationReport,
    template_name: str,
    template_folder: Path,
) -> None:
    main_file = template_folder / "main.py"
    readme_file = template_folder / "README.md"

    report.add(
        template=template_name,
        name="main.py exists",
        passed=main_file.exists(),
        message=str(main_file),
    )

    report.add(
        template=template_name,
        name="README.md exists",
        passed=readme_file.exists(),
        message=str(readme_file),
    )


def _validate_python_syntax(
    report: TemplateValidationReport,
    template_name: str,
    main_file: Path,
) -> None:
    if not main_file.exists():
        report.add(
            template=template_name,
            name="main.py syntax is valid",
            passed=False,
            message="main.py missing",
        )
        return

    try:
        ast.parse(_read_text(main_file), filename=str(main_file))
        report.add(
            template=template_name,
            name="main.py syntax is valid",
            passed=True,
            message="Valid Python syntax",
        )
    except SyntaxError as exc:
        report.add(
            template=template_name,
            name="main.py syntax is valid",
            passed=False,
            message=f"Syntax error: {exc}",
        )


def _validate_hyperkit_import(
    report: TemplateValidationReport,
    template_name: str,
    main_file: Path,
) -> None:
    if not main_file.exists():
        report.add(
            template=template_name,
            name="main.py imports HyperKit",
            passed=False,
            message="main.py missing",
        )
        return

    content = _read_text(main_file)

    report.add(
        template=template_name,
        name="main.py imports HyperKit",
        passed="from hyperkit import" in content or "import hyperkit" in content,
        message="HyperKit import found"
        if "from hyperkit import" in content or "import hyperkit" in content
        else "HyperKit import missing",
    )


def _validate_template_has_game_entry(
    report: TemplateValidationReport,
    template_name: str,
    main_file: Path,
) -> None:
    if not main_file.exists():
        report.add(
            template=template_name,
            name="main.py has game entry",
            passed=False,
            message="main.py missing",
        )
        return

    content = _read_text(main_file)
    has_game_entry = "Game(" in content and ".set_scene(" in content and ".run()" in content

    report.add(
        template=template_name,
        name="main.py has game entry",
        passed=has_game_entry,
        message="Game entry found" if has_game_entry else "Game entry missing",
    )


def _validate_no_forbidden_paths(
    report: TemplateValidationReport,
    template_name: str,
    template_folder: Path,
) -> None:
    findings: list[str] = []

    if template_folder.exists():
        for file_path in template_folder.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in {".py", ".md", ".txt", ".json", ".toml"}:
                continue

            content = _read_text(file_path)

            for term in FORBIDDEN_TEMPLATE_TERMS:
                if term in content:
                    findings.append(f"{file_path.name}: {term}")

    report.add(
        template=template_name,
        name="No forbidden local paths",
        passed=len(findings) == 0,
        message="No forbidden paths found" if not findings else "; ".join(
            findings[:5]),
    )


def generate_template_validation_report(root: str | Path = ".") -> TemplateValidationReport:
    root_path = Path(root).resolve()
    report = TemplateValidationReport(root=root_path)
    templates_root = _template_root(root_path)

    for template_name in EXPECTED_TEMPLATES:
        template_folder = templates_root / template_name
        main_file = template_folder / "main.py"

        _validate_template_folder(report, template_name, template_folder)
        _validate_required_files(report, template_name, template_folder)
        _validate_python_syntax(report, template_name, main_file)
        _validate_hyperkit_import(report, template_name, main_file)
        _validate_template_has_game_entry(report, template_name, main_file)
        _validate_no_forbidden_paths(report, template_name, template_folder)

    return report


def format_template_validation_report(report: TemplateValidationReport) -> str:
    lines: list[str] = []

    lines.append("HyperKit Template Validation Report")
    lines.append("=" * 36)
    lines.append(f"Root: {report.root}")
    lines.append("")
    lines.append(f"Passed: {report.passed_count}/{report.total}")
    lines.append(f"Failed: {report.failed_count}")
    lines.append("")

    for check in report.checks:
        status = "OK" if check.passed else "FAIL"
        lines.append(
            f"[{status}] {check.template} - {check.name} - {check.message}")

    lines.append("")

    if report.passed:
        lines.append("Template validation status: PASS")
    else:
        lines.append("Template validation status: FAIL")
        lines.append("Fix failed template checks before release.")

    return "\n".join(lines)


def run_template_validation(root: str | Path = ".") -> int:
    report = generate_template_validation_report(root)
    print(format_template_validation_report(report))
    return 0 if report.passed else 1
