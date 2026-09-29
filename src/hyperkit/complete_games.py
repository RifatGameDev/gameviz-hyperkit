"""Validation for HyperKit's complete built-in game templates."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


COMPLETE_GAME_TEMPLATES = (
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
)


@dataclass
class CompleteGameCheck:
    template: str
    name: str
    passed: bool
    message: str


@dataclass
class CompleteGameReport:
    root: Path
    checks: list[CompleteGameCheck] = field(
        default_factory=list
    )

    @property
    def passed(self) -> bool:
        return all(
            check.passed
            for check in self.checks
        )

    @property
    def total(self) -> int:
        return len(
            self.checks
        )

    @property
    def passed_count(self) -> int:
        return sum(
            1
            for check in self.checks
            if check.passed
        )

    @property
    def failed_count(self) -> int:
        return (
            self.total
            - self.passed_count
        )

    def add(
        self,
        template: str,
        name: str,
        passed: bool,
        message: str,
    ) -> None:
        self.checks.append(
            CompleteGameCheck(
                template=template,
                name=name,
                passed=passed,
                message=message,
            )
        )


def _read(
    path: Path,
) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def _check_template(
    report: CompleteGameReport,
    template: str,
    template_root: Path,
) -> None:
    main_file = (
        template_root
        / "main.py"
    )
    readme_file = (
        template_root
        / "README.md"
    )

    report.add(
        template,
        "main.py exists",
        main_file.is_file(),
        str(main_file),
    )
    report.add(
        template,
        "README.md exists",
        readme_file.is_file(),
        str(readme_file),
    )

    if not main_file.is_file():
        for name in (
            "main.py syntax is valid",
            "game entry exists",
            "player input exists",
            "score and high score exist",
            "progress feedback exists",
            "game-over state exists",
            "restart flow exists",
        ):
            report.add(
                template,
                name,
                False,
                "main.py missing",
            )
        return

    content = _read(
        main_file
    )

    try:
        ast.parse(
            content,
            filename=str(
                main_file
            ),
        )
        syntax_valid = True
    except SyntaxError:
        syntax_valid = False

    report.add(
        template,
        "main.py syntax is valid",
        syntax_valid,
        (
            "Valid Python syntax"
            if syntax_valid
            else "Invalid Python syntax"
        ),
    )

    has_entry = (
        "Game(" in content
        and ".set_scene(" in content
        and ".run()" in content
    )
    report.add(
        template,
        "game entry exists",
        has_entry,
        (
            "Runnable game entry found"
            if has_entry
            else "Runnable game entry missing"
        ),
    )

    has_input = (
        "def on_tap(" in content
        or "def on_swipe(" in content
    )
    report.add(
        template,
        "player input exists",
        has_input,
        (
            "Player input handler found"
            if has_input
            else "Player input handler missing"
        ),
    )

    has_score = (
        "ScoreManager" in content
        and "High Score" in content
    )
    report.add(
        template,
        "score and high score exist",
        has_score,
        (
            "Score and persistent high-score flow found"
            if has_score
            else "Score/high-score flow missing"
        ),
    )

    has_progress = (
        "ProgressBar" in content
        and ".set_value(" in content
    )
    report.add(
        template,
        "progress feedback exists",
        has_progress,
        (
            "Progress feedback found"
            if has_progress
            else "Progress feedback missing"
        ),
    )

    has_game_over = (
        "game_over" in content
    )
    report.add(
        template,
        "game-over state exists",
        has_game_over,
        (
            "Game-over state found"
            if has_game_over
            else "Game-over state missing"
        ),
    )

    has_restart = (
        "def _restart(" in content
        and "_restart()" in content
    )
    report.add(
        template,
        "restart flow exists",
        has_restart,
        (
            "Restart flow found"
            if has_restart
            else "Restart flow missing"
        ),
    )


def generate_complete_game_report(
    root: str | Path = ".",
) -> CompleteGameReport:
    root_path = Path(
        root
    ).resolve()
    report = CompleteGameReport(
        root=root_path
    )

    templates_root = (
        root_path
        / "src"
        / "hyperkit"
        / "templates"
    )

    for template in (
        COMPLETE_GAME_TEMPLATES
    ):
        _check_template(
            report,
            template,
            templates_root
            / template,
        )

    return report


def format_complete_game_report(
    report: CompleteGameReport,
) -> str:
    lines = [
        "HyperKit Complete Game Validation",
        "=" * 33,
        f"Root: {report.root}",
        "",
        (
            "Passed: "
            f"{report.passed_count}/"
            f"{report.total}"
        ),
        (
            "Failed: "
            f"{report.failed_count}"
        ),
        "",
    ]

    for check in report.checks:
        status = (
            "OK"
            if check.passed
            else "FAIL"
        )
        lines.append(
            f"[{status}] "
            f"{check.template} - "
            f"{check.name} - "
            f"{check.message}"
        )

    lines.append("")

    if report.passed:
        lines.append(
            "Complete game validation status: PASS"
        )
    else:
        lines.append(
            "Complete game validation status: FAIL"
        )

    return "\n".join(
        lines
    )


def run_complete_game_validation(
    root: str | Path = ".",
) -> int:
    report = generate_complete_game_report(
        root
    )
    print(
        format_complete_game_report(
            report
        )
    )
    return (
        0
        if report.passed
        else 1
    )
