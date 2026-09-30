"""Production Android release and signing readiness checks."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .android import (
    PRODUCTION_ANDROID_API,
    PRODUCTION_ANDROID_NDK,
    PRODUCTION_P4A_BRANCH,
    PRODUCTION_RELEASE_ARTIFACT,
)


P4A_RELEASE_SIGNING_VARIABLES = (
    "P4A_RELEASE_KEYSTORE",
    "P4A_RELEASE_KEYSTORE_PASSWD",
    "P4A_RELEASE_KEYALIAS",
    "P4A_RELEASE_KEYALIAS_PASSWD",
)


@dataclass(frozen=True)
class AndroidProductionCheck:
    """One production Android readiness check."""

    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class AndroidProductionReadinessReport:
    """Store-oriented Android build/signing readiness report."""

    root: Path
    checks: tuple[
        AndroidProductionCheck,
        ...,
    ]

    @property
    def passed(self) -> bool:
        return all(
            check.passed
            for check in self.checks
        )

    @property
    def failed_checks(self) -> tuple[
        AndroidProductionCheck,
        ...,
    ]:
        return tuple(
            check
            for check in self.checks
            if not check.passed
        )


def _contains_spec_value(
    content: str,
    key: str,
    expected: str,
) -> bool:
    expected_line = (
        f"{key} = {expected}"
    )

    return any(
        line.strip()
        == expected_line
        for line in content.splitlines()
    )


def generate_android_production_readiness_report(
    path: str | Path = ".",
    *,
    environment: Mapping[
        str,
        str,
    ] | None = None,
) -> AndroidProductionReadinessReport:
    """Validate production build configuration and signing inputs.

    Secret values are never included in the report.
    """

    root = Path(
        path
    ).resolve()
    env = (
        os.environ
        if environment is None
        else environment
    )

    main_file = (
        root
        / "main.py"
    )
    metadata_file = (
        root
        / "hyperkit.toml"
    )
    spec_file = (
        root
        / "buildozer.spec"
    )

    spec_content = (
        spec_file.read_text(
            encoding="utf-8",
            errors="ignore",
        )
        if spec_file.is_file()
        else ""
    )

    checks: list[
        AndroidProductionCheck
    ] = [
        AndroidProductionCheck(
            name="Project directory",
            passed=(
                root.is_dir()
            ),
            message=(
                "Project directory found"
                if root.is_dir()
                else "Project directory missing"
            ),
        ),
        AndroidProductionCheck(
            name="Main entry point",
            passed=(
                main_file.is_file()
            ),
            message=(
                "main.py found"
                if main_file.is_file()
                else "main.py missing"
            ),
        ),
        AndroidProductionCheck(
            name="HyperKit metadata",
            passed=(
                metadata_file.is_file()
            ),
            message=(
                "hyperkit.toml found"
                if metadata_file.is_file()
                else "hyperkit.toml missing"
            ),
        ),
        AndroidProductionCheck(
            name="Buildozer configuration",
            passed=(
                spec_file.is_file()
            ),
            message=(
                "buildozer.spec found"
                if spec_file.is_file()
                else "buildozer.spec missing"
            ),
        ),
        AndroidProductionCheck(
            name="Production target API",
            passed=_contains_spec_value(
                spec_content,
                "android.api",
                str(
                    PRODUCTION_ANDROID_API
                ),
            ),
            message=(
                "Expected Android API "
                f"{PRODUCTION_ANDROID_API}"
            ),
        ),
        AndroidProductionCheck(
            name="Production NDK",
            passed=_contains_spec_value(
                spec_content,
                "android.ndk",
                PRODUCTION_ANDROID_NDK,
            ),
            message=(
                "Expected Android NDK "
                f"{PRODUCTION_ANDROID_NDK}"
            ),
        ),
        AndroidProductionCheck(
            name="Release artifact format",
            passed=_contains_spec_value(
                spec_content,
                "android.release_artifact",
                PRODUCTION_RELEASE_ARTIFACT,
            ),
            message=(
                "Expected release artifact "
                f"{PRODUCTION_RELEASE_ARTIFACT}"
            ),
        ),
        AndroidProductionCheck(
            name="python-for-android branch",
            passed=_contains_spec_value(
                spec_content,
                "p4a.branch",
                PRODUCTION_P4A_BRANCH,
            ),
            message=(
                "Expected p4a branch "
                f"{PRODUCTION_P4A_BRANCH}"
            ),
        ),
    ]

    missing_variables = [
        name
        for name in P4A_RELEASE_SIGNING_VARIABLES
        if not str(
            env.get(
                name,
                "",
            )
        ).strip()
    ]

    checks.append(
        AndroidProductionCheck(
            name="Release signing variables",
            passed=(
                not missing_variables
            ),
            message=(
                "All required signing variables are present"
                if not missing_variables
                else (
                    "Missing: "
                    + ", ".join(
                        missing_variables
                    )
                )
            ),
        )
    )

    keystore_value = str(
        env.get(
            "P4A_RELEASE_KEYSTORE",
            "",
        )
    ).strip()

    keystore_exists = (
        bool(
            keystore_value
        )
        and Path(
            keystore_value
        ).expanduser().is_file()
    )

    checks.append(
        AndroidProductionCheck(
            name="Release keystore file",
            passed=keystore_exists,
            message=(
                "Configured keystore file exists"
                if keystore_exists
                else (
                    "P4A_RELEASE_KEYSTORE must point "
                    "to an existing keystore file"
                )
            ),
        )
    )

    return AndroidProductionReadinessReport(
        root=root,
        checks=tuple(
            checks
        ),
    )


def format_android_production_readiness_report(
    report: AndroidProductionReadinessReport,
) -> str:
    """Format production Android readiness without exposing secrets."""

    lines = [
        "HyperKit Android Production Readiness",
        "=====================================",
        f"Project: {report.root}",
        "",
    ]

    for check in report.checks:
        lines.append(
            (
                "[PASS] "
                if check.passed
                else "[FAIL] "
            )
            + check.name
            + ": "
            + check.message
        )

    lines.extend(
        [
            "",
            (
                "Android production readiness: "
                f"{'PASS' if report.passed else 'FAIL'}"
            ),
        ]
    )

    return "\n".join(
        lines
    )
