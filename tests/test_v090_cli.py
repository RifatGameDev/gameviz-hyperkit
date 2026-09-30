import hyperkit

from hyperkit.cli import main


def test_v090_api_freeze_cli_passes(
    capsys,
):
    result = main(
        [
            "api-freeze-check",
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert (
        "HyperKit API Freeze Check"
        in output
    )
    assert (
        "API contract: 1.0"
        in output
    )
    assert (
        "Frozen exports: 256"
        in output
    )
    assert (
        hyperkit.get_api_fingerprint()
        in output
    )
    assert (
        "API freeze status: PASS"
        in output
    )


def test_v090_cli_version_reports_beta():
    assert (
        hyperkit.__version__
        == "0.9.0b1"
    )
