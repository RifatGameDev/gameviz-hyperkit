import json
from pathlib import Path

from hyperkit.cli import main


def test_v100_stable_release_cli_passes(
    capsys,
):
    result = main(
        [
            "stable-release-check",
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert (
        "HyperKit 1.0 Stable Release Certification"
        in output
    )
    assert "Package version: 1.0.0" in output
    assert "API contract: 1.0" in output
    assert "Frozen exports: 256" in output
    assert (
        "Stable release certification: PASS"
        in output
    )


def test_v100_stable_release_cli_writes_certificate(
    tmp_path: Path,
    capsys,
):
    output = (
        tmp_path
        / "certificate.json"
    )

    result = main(
        [
            "stable-release-check",
            "--certificate",
            str(
                output
            ),
            "--source-commit",
            "abc123",
        ]
    )

    text = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert output.is_file()
    assert "Certificate:" in text

    data = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )

    assert data[
        "version"
    ] == "1.0.0"
    assert data[
        "source_commit"
    ] == "abc123"


def test_v100_publish_check_allows_stable_pypi(
    capsys,
):
    result = main(
        [
            "publish-check",
            "--target",
            "pypi",
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert "Version: 1.0.0" in output
    assert "Publishing check: PASS" in output
