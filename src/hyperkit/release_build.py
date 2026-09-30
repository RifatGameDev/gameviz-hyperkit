"""Release artifact validation and clean-install verification for HyperKit."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class ReleaseBuildError(RuntimeError):
    """Raised when release build verification cannot continue."""


@dataclass(frozen=True)
class DistributionArtifact:
    """One built Python distribution artifact."""

    path: Path
    kind: str
    size_bytes: int
    sha256: str

    @property
    def name(self) -> str:
        return self.path.name


@dataclass(frozen=True)
class DistributionCheck:
    """One distribution validation check."""

    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class DistributionReport:
    """Validation report for wheel and source distribution artifacts."""

    root: Path
    expected_version: str
    artifacts: tuple[DistributionArtifact, ...]
    checks: tuple[DistributionCheck, ...]

    @property
    def passed(self) -> bool:
        return all(
            check.passed
            for check in self.checks
        )

    @property
    def failed_checks(self) -> tuple[DistributionCheck, ...]:
        return tuple(
            check
            for check in self.checks
            if not check.passed
        )

    @property
    def wheel(self) -> DistributionArtifact | None:
        for artifact in self.artifacts:
            if artifact.kind == "wheel":
                return artifact
        return None

    @property
    def sdist(self) -> DistributionArtifact | None:
        for artifact in self.artifacts:
            if artifact.kind == "sdist":
                return artifact
        return None


@dataclass(frozen=True)
class CleanInstallResult:
    """Result of isolated wheel installation verification."""

    passed: bool
    wheel: Path
    expected_version: str
    installed_version: str | None
    cli_output: str
    message: str


def read_project_version(
    root: str | Path = ".",
) -> str:
    """Read the package version from pyproject.toml."""

    root_path = Path(
        root
    ).resolve()
    pyproject = (
        root_path
        / "pyproject.toml"
    )

    if not pyproject.is_file():
        raise ReleaseBuildError(
            f"Missing pyproject.toml: {pyproject}"
        )

    data = tomllib.loads(
        pyproject.read_text(
            encoding="utf-8"
        )
    )

    try:
        version = str(
            data[
                "project"
            ][
                "version"
            ]
        ).strip()
    except (
        KeyError,
        TypeError,
    ) as exc:
        raise ReleaseBuildError(
            "pyproject.toml is missing project.version."
        ) from exc

    if not version:
        raise ReleaseBuildError(
            "project.version must not be empty."
        )

    return version


def sha256_file(
    path: str | Path,
) -> str:
    """Return the SHA-256 digest for a file."""

    file_path = Path(
        path
    )

    digest = hashlib.sha256()

    with file_path.open(
        "rb"
    ) as handle:
        for chunk in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(
                chunk
            )

    return digest.hexdigest()


def _artifact_kind(
    path: Path,
) -> str | None:
    name = path.name.lower()

    if name.endswith(
        ".whl"
    ):
        return "wheel"

    if name.endswith(
        ".tar.gz"
    ):
        return "sdist"

    return None


def discover_distribution_artifacts(
    root: str | Path = ".",
    *,
    dist_dir: str | Path = "dist",
) -> tuple[DistributionArtifact, ...]:
    """Discover built wheel and source distribution artifacts."""

    root_path = Path(
        root
    ).resolve()
    dist_path = (
        root_path
        / dist_dir
    ).resolve()

    if not dist_path.is_dir():
        return ()

    artifacts: list[
        DistributionArtifact
    ] = []

    for path in sorted(
        dist_path.iterdir()
    ):
        if not path.is_file():
            continue

        kind = _artifact_kind(
            path
        )

        if kind is None:
            continue

        stat = path.stat()

        artifacts.append(
            DistributionArtifact(
                path=path.resolve(),
                kind=kind,
                size_bytes=stat.st_size,
                sha256=sha256_file(
                    path
                ),
            )
        )

    return tuple(
        artifacts
    )


def generate_distribution_report(
    root: str | Path = ".",
    *,
    expected_version: str | None = None,
    dist_dir: str | Path = "dist",
) -> DistributionReport:
    """Validate built distribution artifacts for the current package version."""

    root_path = Path(
        root
    ).resolve()
    version = (
        str(
            expected_version
        ).strip()
        if expected_version
        is not None
        else read_project_version(
            root_path
        )
    )

    artifacts = (
        discover_distribution_artifacts(
            root_path,
            dist_dir=dist_dir,
        )
    )

    wheels = tuple(
        artifact
        for artifact in artifacts
        if artifact.kind
        == "wheel"
    )

    sdists = tuple(
        artifact
        for artifact in artifacts
        if artifact.kind
        == "sdist"
    )

    normalized_version = (
        version.replace(
            "-",
            "_",
        )
    )

    checks: list[
        DistributionCheck
    ] = []

    checks.append(
        DistributionCheck(
            name="Wheel count",
            passed=(
                len(
                    wheels
                )
                == 1
            ),
            message=(
                f"Found {len(wheels)} wheel artifact(s)"
            ),
        )
    )

    checks.append(
        DistributionCheck(
            name="Source distribution count",
            passed=(
                len(
                    sdists
                )
                == 1
            ),
            message=(
                f"Found {len(sdists)} source distribution artifact(s)"
            ),
        )
    )

    for artifact in artifacts:
        checks.append(
            DistributionCheck(
                name=(
                    "Non-empty artifact: "
                    f"{artifact.name}"
                ),
                passed=(
                    artifact.size_bytes
                    > 0
                ),
                message=(
                    f"{artifact.size_bytes} bytes"
                ),
            )
        )

        checks.append(
            DistributionCheck(
                name=(
                    "Artifact version: "
                    f"{artifact.name}"
                ),
                passed=(
                    version
                    in artifact.name
                    or normalized_version
                    in artifact.name
                ),
                message=(
                    "Expected version "
                    f"{version}"
                ),
            )
        )

        checks.append(
            DistributionCheck(
                name=(
                    "Artifact SHA-256: "
                    f"{artifact.name}"
                ),
                passed=(
                    len(
                        artifact.sha256
                    )
                    == 64
                ),
                message=artifact.sha256,
            )
        )

    if not artifacts:
        checks.append(
            DistributionCheck(
                name="Distribution artifacts",
                passed=False,
                message=(
                    "No wheel or source distribution "
                    "artifacts found."
                ),
            )
        )

    return DistributionReport(
        root=root_path,
        expected_version=version,
        artifacts=artifacts,
        checks=tuple(
            checks
        ),
    )


def format_distribution_report(
    report: DistributionReport,
) -> str:
    """Format a distribution report for the CLI."""

    lines = [
        "HyperKit Distribution Verification",
        "==================================",
        f"Root: {report.root}",
        f"Version: {report.expected_version}",
        "",
    ]

    for check in report.checks:
        lines.append(
            "[PASS] "
            f"{check.name}: "
            f"{check.message}"
            if check.passed
            else (
                "[FAIL] "
                f"{check.name}: "
                f"{check.message}"
            )
        )

    lines.extend(
        [
            "",
            (
                "Distribution verification: "
                f"{'PASS' if report.passed else 'FAIL'}"
            ),
        ]
    )

    return "\n".join(
        lines
    )


def write_checksum_manifest(
    report: DistributionReport,
    *,
    filename: str = "SHA256SUMS",
) -> Path:
    """Write deterministic SHA-256 checksums for verified artifacts."""

    if not report.passed:
        raise ReleaseBuildError(
            "Cannot write checksums for an invalid distribution report."
        )

    dist_path = (
        report.artifacts[
            0
        ].path.parent
    )

    output = (
        dist_path
        / filename
    )

    lines = [
        (
            f"{artifact.sha256}  "
            f"{artifact.name}"
        )
        for artifact in sorted(
            report.artifacts,
            key=lambda item: item.name,
        )
    ]

    output.write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    return output


def write_release_manifest(
    report: DistributionReport,
    *,
    filename: str = "release-manifest.json",
    source_commit: str | None = None,
) -> Path:
    """Write machine-readable release artifact metadata."""

    if not report.passed:
        raise ReleaseBuildError(
            "Cannot write a release manifest for invalid artifacts."
        )

    dist_path = (
        report.artifacts[
            0
        ].path.parent
    )

    output = (
        dist_path
        / filename
    )

    payload = {
        "package": (
            "gameviz-hyperkit"
        ),
        "version": (
            report.expected_version
        ),
        "source_commit": (
            source_commit
            or os.environ.get(
                "GITHUB_SHA"
            )
        ),
        "artifacts": [
            {
                "filename": artifact.name,
                "kind": artifact.kind,
                "size_bytes": artifact.size_bytes,
                "sha256": artifact.sha256,
            }
            for artifact in sorted(
                report.artifacts,
                key=lambda item: item.name,
            )
        ],
    }

    output.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    return output


def _venv_python(
    environment: Path,
) -> Path:
    if os.name == "nt":
        return (
            environment
            / "Scripts"
            / "python.exe"
        )

    return (
        environment
        / "bin"
        / "python"
    )


def _run_command(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(
            command
        ),
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def run_clean_install_verification(
    wheel: str | Path,
    *,
    expected_version: str,
    python_executable: str | Path = sys.executable,
) -> CleanInstallResult:
    """Install a built wheel into a fresh venv and verify import/CLI version."""

    wheel_path = Path(
        wheel
    ).resolve()

    if not wheel_path.is_file():
        raise ReleaseBuildError(
            f"Wheel does not exist: {wheel_path}"
        )

    if wheel_path.suffix.lower() != ".whl":
        raise ReleaseBuildError(
            "Clean-install verification requires a wheel artifact."
        )

    version = str(
        expected_version
    ).strip()

    if not version:
        raise ReleaseBuildError(
            "expected_version must not be empty."
        )

    with tempfile.TemporaryDirectory(
        prefix="hyperkit-clean-install-"
    ) as temp_dir:
        environment = (
            Path(
                temp_dir
            )
            / "venv"
        )

        create_result = _run_command(
            [
                str(
                    python_executable
                ),
                "-m",
                "venv",
                str(
                    environment
                ),
            ]
        )

        if create_result.returncode != 0:
            return CleanInstallResult(
                passed=False,
                wheel=wheel_path,
                expected_version=version,
                installed_version=None,
                cli_output="",
                message=(
                    "Virtual environment creation failed: "
                    f"{create_result.stderr.strip()}"
                ),
            )

        env_python = (
            _venv_python(
                environment
            )
        )

        install_result = _run_command(
            [
                str(
                    env_python
                ),
                "-m",
                "pip",
                "install",
                str(
                    wheel_path
                ),
            ]
        )

        if install_result.returncode != 0:
            return CleanInstallResult(
                passed=False,
                wheel=wheel_path,
                expected_version=version,
                installed_version=None,
                cli_output="",
                message=(
                    "Wheel installation failed: "
                    f"{install_result.stderr.strip()}"
                ),
            )

        import_result = _run_command(
            [
                str(
                    env_python
                ),
                "-c",
                (
                    "import hyperkit; "
                    "print(hyperkit.__version__)"
                ),
            ]
        )

        installed_version = (
            import_result.stdout.strip()
            if import_result.returncode
            == 0
            else None
        )

        cli_result = _run_command(
            [
                str(
                    env_python
                ),
                "-m",
                "hyperkit",
                "--version",
            ]
        )

        cli_output = (
            cli_result.stdout.strip()
        )

        passed = (
            import_result.returncode
            == 0
            and cli_result.returncode
            == 0
            and installed_version
            == version
            and version
            in cli_output
        )

        if passed:
            message = (
                "Fresh virtual environment import and CLI checks passed."
            )
        else:
            details = [
                (
                    "import return code="
                    f"{import_result.returncode}"
                ),
                (
                    "cli return code="
                    f"{cli_result.returncode}"
                ),
                (
                    "installed version="
                    f"{installed_version!r}"
                ),
                (
                    "cli output="
                    f"{cli_output!r}"
                ),
            ]
            message = "; ".join(
                details
            )

        return CleanInstallResult(
            passed=passed,
            wheel=wheel_path,
            expected_version=version,
            installed_version=installed_version,
            cli_output=cli_output,
            message=message,
        )


def format_clean_install_result(
    result: CleanInstallResult,
) -> str:
    """Format isolated install verification for CLI output."""

    lines = [
        "HyperKit Clean Install Verification",
        "===================================",
        f"Wheel: {result.wheel}",
        f"Expected version: {result.expected_version}",
        (
            "Installed version: "
            f"{result.installed_version or 'unknown'}"
        ),
        (
            "CLI: "
            f"{result.cli_output or 'no output'}"
        ),
        "",
        (
            "Clean-install verification: "
            f"{'PASS' if result.passed else 'FAIL'}"
        ),
        result.message,
    ]

    return "\n".join(
        lines
    )
