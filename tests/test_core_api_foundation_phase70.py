from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import hyperkit
from hyperkit import (
    API_VERSION,
    SDKConfig,
    HyperKitCompatibilityError,
    HyperKitConfigurationError,
    HyperKitError,
    HyperKitRuntimeError,
    HyperKitValidationError,
    get_api_version,
    is_api_compatible,
    require_api_version,
)


PYPROJECT = Path("pyproject.toml")


def test_phase70_version_is_synchronized():
    with PYPROJECT.open("rb") as file:
        project = tomllib.load(file)["project"]

    assert project["version"] == hyperkit.__version__


def test_core_error_types_inherit_from_hyperkit_error():
    assert issubclass(
        HyperKitConfigurationError,
        HyperKitError,
    )

    assert issubclass(
        HyperKitCompatibilityError,
        HyperKitError,
    )

    assert issubclass(
        HyperKitRuntimeError,
        HyperKitError,
    )

    assert issubclass(
        HyperKitValidationError,
        HyperKitError,
    )


def test_sdk_config_defaults_are_stable():
    config = SDKConfig()

    assert config.debug is False
    assert config.strict is True
    assert config.log_level == "INFO"

    assert config.to_dict() == {
        "debug": False,
        "strict": True,
        "log_level": "INFO",
    }


def test_sdk_config_normalizes_log_level():
    config = SDKConfig(
        log_level="debug"
    )

    assert config.log_level == "DEBUG"


def test_sdk_config_rejects_invalid_log_level():
    with pytest.raises(
        HyperKitConfigurationError
    ):
        SDKConfig(
            log_level="trace"
        )


def test_current_api_version_is_exposed():
    assert API_VERSION == "1.0"
    assert get_api_version() == "1.0"


def test_api_compatibility_rules():
    assert is_api_compatible("1.0") is True
    assert is_api_compatible("1.1") is False
    assert is_api_compatible("0.9") is False
    assert is_api_compatible("2.0") is False


def test_require_api_version_rejects_incompatible_api():
    require_api_version("1.0")

    with pytest.raises(
        HyperKitCompatibilityError
    ):
        require_api_version("1.1")

