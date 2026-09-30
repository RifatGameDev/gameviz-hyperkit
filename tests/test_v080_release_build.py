import json
from pathlib import Path
from types import SimpleNamespace

import hyperkit.release_build as release_build

from hyperkit import (
    generate_distribution_report,
    write_checksum_manifest,
    write_release_manifest,
)


VERSION = "0.8.0.dev0"


def create_project(
    root: Path,
) -> Path:
    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    (
        root
        / "pyproject.toml"
    ).write_text(
        (
            "[project]\n"
            'name = "gameviz-hyperkit"\n'
            f'version = "{VERSION}"\n'
        ),
        encoding="utf-8",
    )

    dist = (
        root
        / "dist"
    )
    dist.mkdir()

    (
        dist
        / f"gameviz_hyperkit-{VERSION}-py3-none-any.whl"
    ).write_bytes(
        b"wheel-artifact"
    )

    (
        dist
        / f"gameviz_hyperkit-{VERSION}.tar.gz"
    ).write_bytes(
        b"sdist-artifact"
    )

    return root


def test_distribution_report_validates_expected_artifacts(
    tmp_path: Path,
):
    create_project(
        tmp_path
    )

    report = generate_distribution_report(
        tmp_path
    )

    assert report.passed
    assert report.expected_version == VERSION
    assert report.wheel is not None
    assert report.sdist is not None
    assert len(
        report.artifacts
    ) == 2

    for artifact in report.artifacts:
        assert artifact.size_bytes > 0
        assert len(
            artifact.sha256
        ) == 64


def test_distribution_report_fails_when_sdist_is_missing(
    tmp_path: Path,
):
    create_project(
        tmp_path
    )

    (
        tmp_path
        / "dist"
        / f"gameviz_hyperkit-{VERSION}.tar.gz"
    ).unlink()

    report = generate_distribution_report(
        tmp_path
    )

    assert not report.passed
    assert any(
        check.name
        == "Source distribution count"
        and not check.passed
        for check in report.checks
    )


def test_release_manifests_include_checksums_and_source_commit(
    tmp_path: Path,
):
    create_project(
        tmp_path
    )
    report = generate_distribution_report(
        tmp_path
    )

    checksum_path = write_checksum_manifest(
        report
    )
    manifest_path = write_release_manifest(
        report,
        source_commit="abc123",
    )

    checksum_text = (
        checksum_path
        .read_text(
            encoding="utf-8"
        )
    )

    assert "gameviz_hyperkit" in checksum_text

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    assert manifest[
        "version"
    ] == VERSION
    assert manifest[
        "source_commit"
    ] == "abc123"
    assert len(
        manifest[
            "artifacts"
        ]
    ) == 2

    for artifact in manifest[
        "artifacts"
    ]:
        assert len(
            artifact[
                "sha256"
            ]
        ) == 64


def test_clean_install_verification_checks_import_and_cli(
    tmp_path: Path,
    monkeypatch,
):
    wheel = (
        tmp_path
        / f"gameviz_hyperkit-{VERSION}-py3-none-any.whl"
    )
    wheel.write_bytes(
        b"wheel"
    )

    responses = iter(
        [
            SimpleNamespace(
                returncode=0,
                stdout="",
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout="installed",
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout=VERSION + "\n",
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout=(
                    "gameviz-hyperkit "
                    + VERSION
                    + "\n"
                ),
                stderr="",
            ),
        ]
    )

    monkeypatch.setattr(
        release_build,
        "_run_command",
        lambda *args, **kwargs: (
            next(
                responses
            )
        ),
    )

    result = (
        release_build
        .run_clean_install_verification(
            wheel,
            expected_version=VERSION,
        )
    )

    assert result.passed
    assert (
        result.installed_version
        == VERSION
    )
    assert VERSION in result.cli_output


def test_clean_install_verification_reports_install_failure(
    tmp_path: Path,
    monkeypatch,
):
    wheel = (
        tmp_path
        / f"gameviz_hyperkit-{VERSION}-py3-none-any.whl"
    )
    wheel.write_bytes(
        b"wheel"
    )

    responses = iter(
        [
            SimpleNamespace(
                returncode=0,
                stdout="",
                stderr="",
            ),
            SimpleNamespace(
                returncode=1,
                stdout="",
                stderr="install failed",
            ),
        ]
    )

    monkeypatch.setattr(
        release_build,
        "_run_command",
        lambda *args, **kwargs: (
            next(
                responses
            )
        ),
    )

    result = (
        release_build
        .run_clean_install_verification(
            wheel,
            expected_version=VERSION,
        )
    )

    assert not result.passed
    assert "installation failed" in result.message
