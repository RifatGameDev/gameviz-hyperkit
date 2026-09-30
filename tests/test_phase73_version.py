from __future__ import annotations

from pathlib import Path

import hyperkit

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def test_phase73_development_version():
    assert (
        hyperkit.__version__
        == "1.0.0"
    )


def test_package_metadata_matches_module():
    root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    data = tomllib.loads(
        (
            root
            / "pyproject.toml"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert (
        data["project"]["version"]
        == hyperkit.__version__
    )


def test_core_api_contract_remains_02():
    assert (
        hyperkit.API_VERSION
        == "1.0"
    )

