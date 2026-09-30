from pathlib import Path
from types import SimpleNamespace

import hyperkit.cli as cli

from hyperkit.cli import main
from hyperkit.release_build import (
    CleanInstallResult,
)


VERSION = "0.8.0.dev0"


def create_dist_project(
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
        b"wheel"
    )
    (
        dist
        / f"gameviz_hyperkit-{VERSION}.tar.gz"
    ).write_bytes(
        b"sdist"
    )

    return root


def test_verify_dist_cli(
    tmp_path: Path,
    capsys,
):
    project = create_dist_project(
        tmp_path
        / "package"
    )

    result = main(
        [
            "verify-dist",
            "--path",
            str(
                project
            ),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert (
        "Distribution verification: PASS"
        in output
    )


def test_release_manifest_cli_writes_metadata(
    tmp_path: Path,
    capsys,
):
    project = create_dist_project(
        tmp_path
        / "package"
    )

    result = main(
        [
            "release-manifest",
            "--path",
            str(
                project
            ),
            "--source-commit",
            "abc123",
        ]
    )

    capsys.readouterr()

    assert result == 0
    assert (
        project
        / "dist"
        / "SHA256SUMS"
    ).is_file()
    assert (
        project
        / "dist"
        / "release-manifest.json"
    ).is_file()


def test_verify_clean_install_cli(
    tmp_path: Path,
    capsys,
    monkeypatch,
):
    project = create_dist_project(
        tmp_path
        / "package"
    )

    monkeypatch.setattr(
        cli,
        "run_clean_install_verification",
        lambda wheel, expected_version: (
            CleanInstallResult(
                passed=True,
                wheel=Path(
                    wheel
                ),
                expected_version=(
                    expected_version
                ),
                installed_version=(
                    expected_version
                ),
                cli_output=(
                    "gameviz-hyperkit "
                    + expected_version
                ),
                message="passed",
            )
        ),
    )

    result = main(
        [
            "verify-clean-install",
            "--path",
            str(
                project
            ),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert (
        "Clean-install verification: PASS"
        in output
    )


def test_init_android_production_cli(
    tmp_path: Path,
    capsys,
):
    project = (
        tmp_path
        / "game"
    )
    project.mkdir()

    result = main(
        [
            "init-android",
            "--path",
            str(
                project
            ),
            "--production",
            "--overwrite",
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert "Profile: production" in output

    spec = (
        project
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8"
    )

    assert "android.api = 36" in spec
    assert "android.release_artifact = aab" in spec
    assert "p4a.branch = develop" in spec


def test_android_release_doctor_cli_fails_without_signing(
    tmp_path: Path,
    capsys,
):
    project = (
        tmp_path
        / "game"
    )
    project.mkdir()
    (
        project
        / "main.py"
    ).write_text(
        "print('game')\n",
        encoding="utf-8",
    )
    (
        project
        / "hyperkit.toml"
    ).write_text(
        (
            "[project]\n"
            'name = "game"\n'
        ),
        encoding="utf-8",
    )

    main(
        [
            "init-android",
            "--path",
            str(
                project
            ),
            "--production",
            "--overwrite",
        ]
    )
    capsys.readouterr()

    result = main(
        [
            "android-release-doctor",
            "--path",
            str(
                project
            ),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 1
    assert (
        "Android production readiness: FAIL"
        in output
    )
