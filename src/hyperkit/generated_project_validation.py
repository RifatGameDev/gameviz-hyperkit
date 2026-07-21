from __future__ import annotations

import ast
import io
import shutil
import tempfile
import tomllib
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path


POLISHED_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


FORBIDDEN_GENERATED_PROJECT_TERMS = [
    "D:" + "\\AI\\HyperKit\\gameviz-hyperkit",
    "/" + "mnt/data",
    "gameviz-hyperkit" + "\\src",
]


FOLLOWUP_CHECK_NAMES = [
    "Project directory exists",
    "main.py exists",
    "hyperkit.toml exists",
    "assets directory exists",
    "main.py syntax is valid",
    "main.py imports HyperKit",
    "main.py has game entry",
    "hyperkit.toml is valid",
    "No forbidden local paths",
]


@dataclass
class GeneratedProjectValidationCheck:
    template: str
    name: str
    passed: bool
    message: str


@dataclass
class GeneratedProjectValidationReport:
    work_root: Path
    checks: list[GeneratedProjectValidationCheck] = field(default_factory=list)

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

    def add(
        self,
        template: str,
        name: str,
        passed: bool,
        message: str,
    ) -> None:
        self.checks.append(
            GeneratedProjectValidationCheck(
                template=template,
                name=name,
                passed=passed,
                message=message,
            )
        )


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _resolve_generated_project_path(
    created_path,
    destination: Path,
    project_name: str,
) -> Path:
    candidates: list[Path] = []

    if created_path is not None:
        candidates.append(Path(created_path).resolve())

    candidates.extend(
        [
            destination.resolve(),
            (destination / project_name).resolve(),
        ]
    )

    for candidate in candidates:
        if (candidate / "main.py").exists():
            return candidate

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return destination.resolve()


def _add_failed_followup_checks(
    report: GeneratedProjectValidationReport,
    template_name: str,
    message: str,
) -> None:
    for check_name in FOLLOWUP_CHECK_NAMES:
        report.add(
            template=template_name,
            name=check_name,
            passed=False,
            message=message,
        )


def _validate_required_paths(
    report: GeneratedProjectValidationReport,
    template_name: str,
    project_path: Path,
) -> None:
    required_paths = {
        "Project directory exists": project_path,
        "main.py exists": project_path / "main.py",
        "hyperkit.toml exists": project_path / "hyperkit.toml",
        "assets directory exists": project_path / "assets",
    }

    for check_name, required_path in required_paths.items():
        report.add(
            template=template_name,
            name=check_name,
            passed=required_path.exists(),
            message=str(required_path),
        )


def _validate_main_syntax(
    report: GeneratedProjectValidationReport,
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
    report: GeneratedProjectValidationReport,
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
    imports_hyperkit = (
        "from hyperkit import" in content
        or "import hyperkit" in content
    )

    report.add(
        template=template_name,
        name="main.py imports HyperKit",
        passed=imports_hyperkit,
        message=(
            "HyperKit import found"
            if imports_hyperkit
            else "HyperKit import missing"
        ),
    )


def _validate_game_entry(
    report: GeneratedProjectValidationReport,
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
    has_game_entry = (
        "Game(" in content
        and ".set_scene(" in content
        and ".run()" in content
    )

    report.add(
        template=template_name,
        name="main.py has game entry",
        passed=has_game_entry,
        message=(
            "Game entry found"
            if has_game_entry
            else "Game entry missing"
        ),
    )


def _validate_project_metadata(
    report: GeneratedProjectValidationReport,
    template_name: str,
    metadata_file: Path,
) -> None:
    if not metadata_file.exists():
        report.add(
            template=template_name,
            name="hyperkit.toml is valid",
            passed=False,
            message="hyperkit.toml missing",
        )
        return

    try:
        metadata = tomllib.loads(_read_text(metadata_file))
        is_valid = isinstance(metadata, dict) and len(metadata) > 0

        report.add(
            template=template_name,
            name="hyperkit.toml is valid",
            passed=is_valid,
            message=(
                "Valid TOML metadata"
                if is_valid
                else "TOML metadata is empty"
            ),
        )
    except tomllib.TOMLDecodeError as exc:
        report.add(
            template=template_name,
            name="hyperkit.toml is valid",
            passed=False,
            message=f"Invalid TOML: {exc}",
        )


def _validate_no_forbidden_paths(
    report: GeneratedProjectValidationReport,
    template_name: str,
    project_path: Path,
) -> None:
    if not project_path.exists():
        report.add(
            template=template_name,
            name="No forbidden local paths",
            passed=False,
            message="Project directory missing",
        )
        return

    findings: list[str] = []
    allowed_suffixes = {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".toml",
        ".yaml",
        ".yml",
    }

    for file_path in project_path.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in allowed_suffixes:
            continue

        content = _read_text(file_path)

        for term in FORBIDDEN_GENERATED_PROJECT_TERMS:
            if term in content:
                findings.append(f"{file_path.name}: {term}")

    report.add(
        template=template_name,
        name="No forbidden local paths",
        passed=len(findings) == 0,
        message=(
            "No forbidden paths found"
            if not findings
            else "; ".join(findings[:5])
        ),
    )


def _validate_generated_project(
    report: GeneratedProjectValidationReport,
    template_name: str,
    project_path: Path,
) -> None:
    main_file = project_path / "main.py"
    metadata_file = project_path / "hyperkit.toml"

    _validate_required_paths(
        report=report,
        template_name=template_name,
        project_path=project_path,
    )

    _validate_main_syntax(
        report=report,
        template_name=template_name,
        main_file=main_file,
    )

    _validate_hyperkit_import(
        report=report,
        template_name=template_name,
        main_file=main_file,
    )

    _validate_game_entry(
        report=report,
        template_name=template_name,
        main_file=main_file,
    )

    _validate_project_metadata(
        report=report,
        template_name=template_name,
        metadata_file=metadata_file,
    )

    _validate_no_forbidden_paths(
        report=report,
        template_name=template_name,
        project_path=project_path,
    )


def _generate_and_validate_templates(
    work_root: Path,
) -> GeneratedProjectValidationReport:
    from .cli import create_project

    work_root.mkdir(parents=True, exist_ok=True)

    report = GeneratedProjectValidationReport(work_root=work_root)

    for template_name in POLISHED_TEMPLATES:
        project_name = f"phase55_{template_name}"
        destination = work_root / project_name

        if destination.exists():
            shutil.rmtree(destination)

        try:
            captured_output = io.StringIO()

            with redirect_stdout(captured_output):
                created_path = create_project(
                    project_name,
                    template_name,
                    destination,
                )

            project_path = _resolve_generated_project_path(
                created_path=created_path,
                destination=destination,
                project_name=project_name,
            )

            report.add(
                template=template_name,
                name="Project generation",
                passed=True,
                message=str(project_path),
            )

            _validate_generated_project(
                report=report,
                template_name=template_name,
                project_path=project_path,
            )
        except Exception as exc:
            report.add(
                template=template_name,
                name="Project generation",
                passed=False,
                message=f"{type(exc).__name__}: {exc}",
            )

            _add_failed_followup_checks(
                report=report,
                template_name=template_name,
                message="Project generation failed",
            )

    return report


def generate_generated_project_validation_report(
    work_root: str | Path | None = None,
) -> GeneratedProjectValidationReport:
    if work_root is not None:
        return _generate_and_validate_templates(
            Path(work_root).resolve()
        )

    with tempfile.TemporaryDirectory(
        prefix="hyperkit-generated-validation-"
    ) as temporary_directory:
        return _generate_and_validate_templates(
            Path(temporary_directory).resolve()
        )


def format_generated_project_validation_report(
    report: GeneratedProjectValidationReport,
) -> str:
    lines: list[str] = []

    lines.append("HyperKit Generated Project Validation")
    lines.append("=" * 37)
    lines.append(f"Work root: {report.work_root}")
    lines.append("")
    lines.append(f"Passed: {report.passed_count}/{report.total}")
    lines.append(f"Failed: {report.failed_count}")
    lines.append("")

    for check in report.checks:
        status = "OK" if check.passed else "FAIL"
        lines.append(
            f"[{status}] {check.template} - "
            f"{check.name} - {check.message}"
        )

    lines.append("")

    if report.passed:
        lines.append("Generated project validation status: PASS")
    else:
        lines.append("Generated project validation status: FAIL")
        lines.append(
            "Fix failed generated project checks before release."
        )

    return "\n".join(lines)


def run_generated_project_validation(
    work_root: str | Path | None = None,
) -> int:
    report = generate_generated_project_validation_report(work_root)
    print(format_generated_project_validation_report(report))
    return 0 if report.passed else 1
