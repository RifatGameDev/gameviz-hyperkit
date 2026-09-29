from importlib.metadata import PackageNotFoundError
from pathlib import Path

import pytest

import hyperkit
import hyperkit.cli as cli


def test_cli_version_falls_back_to_package_version(
    monkeypatch,
):
    def missing_package(_name):
        raise PackageNotFoundError

    monkeypatch.setattr(
        cli,
        "version",
        missing_package,
    )

    assert (
        cli.get_hyperkit_version()
        == hyperkit.__version__
    )


def test_cli_exposes_global_version_option(
    capsys,
):
    with pytest.raises(
        SystemExit
    ) as exc:
        cli.main(
            ["--version"]
        )

    assert exc.value.code == 0

    output = (
        capsys.readouterr()
        .out
        .strip()
    )

    assert output.startswith(
        "gameviz-hyperkit "
    )


def test_cli_description_matches_current_scope():
    help_text = (
        cli.build_parser()
        .format_help()
    )

    assert (
        "building complete small "
        "2D mobile games"
        in help_text
    )


def test_python_module_entry_point_exists():
    path = Path(
        "src/hyperkit/__main__.py"
    )

    assert path.exists()

    content = path.read_text(
        encoding="utf-8"
    )

    assert "from .cli import main" in content
    assert "raise SystemExit" in content
