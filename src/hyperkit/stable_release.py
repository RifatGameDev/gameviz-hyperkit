"""Stable-release certification helpers for GameViz HyperKit 1.0."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .api_contract import (
    FROZEN_API_EXPORT_COUNT,
    FROZEN_API_FINGERPRINT,
    FROZEN_API_VERSION,
    validate_frozen_public_api,
)
from .audit import generate_pre_release_audit_report
from .compatibility import API_VERSION
from .release import generate_release_report
from .release_build import (
    read_project_version,
    validate_publish_target,
)


STABLE_PACKAGE_VERSION = "1.0.1"


@dataclass(frozen=True)
class StableReleaseCheck:
    """One stable-release certification check."""

    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class StableReleaseReport:
    """Final source-tree certification report for HyperKit 1.0."""

    root: Path
    package_version: str
    checks: tuple[StableReleaseCheck, ...]

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

    @property
    def failed_checks(self) -> tuple[StableReleaseCheck, ...]:
        return tuple(
            check
            for check in self.checks
            if not check.passed
        )


def _read_module_version(
    root: Path,
) -> Optional[str]:
    init_path = (
        root
        / "src"
        / "hyperkit"
        / "__init__.py"
    )

    if not init_path.is_file():
        return None

    match = re.search(
        r'^__version__\s*=\s*["\']([^"\']+)["\']',
        init_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ),
        flags=re.MULTILINE,
    )

    if match is None:
        return None

    return match.group(
        1
    )


def _contains(
    path: Path,
    *terms: str,
) -> bool:
    if not path.is_file():
        return False

    content = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    return all(
        term in content
        for term in terms
    )


def generate_stable_release_report(
    root: str | Path = ".",
) -> StableReleaseReport:
    """Generate final stable-release source-tree certification."""

    root_path = Path(
        root
    ).resolve()

    version = read_project_version(
        root_path
    )

    module_version = (
        _read_module_version(
            root_path
        )
    )

    release_report = (
        generate_release_report(
            root_path
        )
    )

    audit_report = (
        generate_pre_release_audit_report(
            root_path
        )
    )

    try:
        validate_frozen_public_api()
    except Exception as exc:
        api_freeze_passed = False
        api_freeze_message = str(
            exc
        )
    else:
        api_freeze_passed = True
        api_freeze_message = (
            "Exact frozen public API matches "
            "the HyperKit 1.0 contract"
        )

    publish_allowed, publish_message = (
        validate_publish_target(
            version,
            "pypi",
        )
    )

    pyproject = (
        root_path
        / "pyproject.toml"
    )
    readme = (
        root_path
        / "README.md"
    )
    roadmap = (
        root_path
        / "ROADMAP.md"
    )
    changelog = (
        root_path
        / "CHANGELOG.md"
    )
    version_history = (
        root_path
        / "docs"
        / "VERSION_HISTORY.md"
    )
    stable_docs = (
        root_path
        / "docs"
        / "V100_STABLE_RELEASE.md"
    )
    stable_workflow = (
        root_path
        / ".github"
        / "workflows"
        / "stable-release.yml"
    )

    checks = (
        StableReleaseCheck(
            name="Stable package version",
            passed=(
                version
                == STABLE_PACKAGE_VERSION
            ),
            message=(
                f"Expected {STABLE_PACKAGE_VERSION}; "
                f"found {version}"
            ),
        ),
        StableReleaseCheck(
            name="Package/module version synchronization",
            passed=(
                module_version
                == version
            ),
            message=(
                f"pyproject={version}; "
                f"hyperkit.__version__={module_version}"
            ),
        ),
        StableReleaseCheck(
            name="Stable package classifier",
            passed=_contains(
                pyproject,
                "Development Status :: 5 - Production/Stable",
            ),
            message=(
                "Production/Stable package classifier present"
            ),
        ),
        StableReleaseCheck(
            name="Frozen compatibility contract",
            passed=(
                API_VERSION
                == FROZEN_API_VERSION
                == "1.0"
            ),
            message=(
                f"API contract={API_VERSION}"
            ),
        ),
        StableReleaseCheck(
            name="Frozen API exact match",
            passed=api_freeze_passed,
            message=api_freeze_message,
        ),
        StableReleaseCheck(
            name="Frozen API export count",
            passed=(
                FROZEN_API_EXPORT_COUNT
                == 256
            ),
            message=(
                "Frozen exports="
                f"{FROZEN_API_EXPORT_COUNT}"
            ),
        ),
        StableReleaseCheck(
            name="Frozen API fingerprint",
            passed=(
                len(
                    FROZEN_API_FINGERPRINT
                )
                == 64
            ),
            message=(
                FROZEN_API_FINGERPRINT
            ),
        ),
        StableReleaseCheck(
            name="Release readiness report",
            passed=release_report.passed,
            message=(
                f"{release_report.passed_count}/"
                f"{release_report.total} checks passed"
            ),
        ),
        StableReleaseCheck(
            name="Pre-release audit",
            passed=audit_report.passed,
            message=(
                f"{audit_report.passed_count}/"
                f"{audit_report.total} checks passed"
            ),
        ),
        StableReleaseCheck(
            name="Stable PyPI target eligibility",
            passed=publish_allowed,
            message=publish_message,
        ),
        StableReleaseCheck(
            name="Stable README status",
            passed=_contains(
                readme,
                "Package maturity: Production / Stable",
                "Public compatibility contract: API `1.0`",
                "Stable package version: `1.0.1`",
            ),
            message=(
                "README identifies HyperKit 1.0 as stable"
            ),
        ),
        StableReleaseCheck(
            name="Stable roadmap state",
            passed=_contains(
                roadmap,
                "v1.0.1  Stable Patch Release",
                "CURRENT STABLE RELEASE",
                "Active package version: `1.0.1`",
            ),
            message=(
                "Roadmap tracks v1.0.1 stable patch release"
            ),
        ),
        StableReleaseCheck(
            name="Stable changelog entry",
            passed=_contains(
                changelog,
                "## 1.0.1",
                "Stable Release",
            ),
            message=(
                "CHANGELOG contains the 1.0.1 stable patch release"
            ),
        ),
        StableReleaseCheck(
            name="Stable version history",
            passed=_contains(
                version_history,
                "1.0.1",
                "Stable Patch Release",
                "API `1.0`",
            ),
            message=(
                "Version history documents stable 1.0"
            ),
        ),
        StableReleaseCheck(
            name="Stable release documentation",
            passed=_contains(
                stable_docs,
                "HyperKit v1.0.1",
                "Stable Release",
                "256",
                FROZEN_API_FINGERPRINT,
            ),
            message=(
                "Stable release certification documentation present"
            ),
        ),
        StableReleaseCheck(
            name="Stable release workflow",
            passed=_contains(
                stable_workflow,
                "workflow_dispatch:",
                "stable-release-check",
                "api-freeze-check",
                "publish-check --target pypi",
                "verify-clean-install",
                "pypa/gh-action-pypi-publish@release/v1",
                "refs/tags/v1.0.1",
            ),
            message=(
                "Protected stable-release workflow present"
            ),
        ),
    )

    return StableReleaseReport(
        root=root_path,
        package_version=version,
        checks=checks,
    )


def format_stable_release_report(
    report: StableReleaseReport,
) -> str:
    """Format the final stable-release certification report."""

    lines = [
        "HyperKit 1.0 Stable Release Certification",
        "=========================================",
        f"Root: {report.root}",
        f"Package version: {report.package_version}",
        f"API contract: {FROZEN_API_VERSION}",
        f"Frozen exports: {FROZEN_API_EXPORT_COUNT}",
        f"API fingerprint: {FROZEN_API_FINGERPRINT}",
        "",
        (
            f"Passed: {report.passed_count}/"
            f"{report.total}"
        ),
        (
            f"Failed: {report.failed_count}"
        ),
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
                "Stable release certification: "
                f"{'PASS' if report.passed else 'FAIL'}"
            ),
        ]
    )

    return "\n".join(
        lines
    )


def write_stable_release_certificate(
    report: StableReleaseReport,
    output: str | Path,
    *,
    source_commit: Optional[str] = None,
) -> Path:
    """Write machine-readable stable-release certification evidence."""

    if not report.passed:
        raise RuntimeError(
            "Cannot write a stable release certificate "
            "while certification checks are failing."
        )

    output_path = Path(
        output
    ).resolve()
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "package": "gameviz-hyperkit",
        "version": report.package_version,
        "api_version": FROZEN_API_VERSION,
        "frozen_api_export_count": FROZEN_API_EXPORT_COUNT,
        "frozen_api_fingerprint": FROZEN_API_FINGERPRINT,
        "source_commit": source_commit,
        "status": "pass",
        "checks": {
            check.name: check.passed
            for check in report.checks
        },
    }

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        handle.write(
            json.dumps(
                payload,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    return output_path
