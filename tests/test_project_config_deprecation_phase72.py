from pathlib import Path

import pytest

from hyperkit import (
    PROJECT_CONFIG_FILENAME,
    PROJECT_CONFIG_SCHEMA_VERSION,
    HyperKitConfigurationError,
    HyperKitDeprecationWarning,
    ProjectConfig,
    build_deprecation_message,
    deprecated,
    find_project_config,
    load_project_config,
    warn_deprecated,
)


def test_project_config_constants():
    assert (
        PROJECT_CONFIG_FILENAME
        == "hyperkit.toml"
    )

    assert (
        PROJECT_CONFIG_SCHEMA_VERSION
        == 1
    )


def test_load_basic_project_config(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "hyperkit.toml"
    )

    path.write_text(
        """
[project]
name = "demo-game"
""".strip(),
        encoding="utf-8",
    )

    config = load_project_config(path)

    assert isinstance(
        config,
        ProjectConfig,
    )

    assert config.path == path.resolve()

    assert config.schema_version == 1

    assert (
        config.get_section(
            "project"
        )["name"]
        == "demo-game"
    )


def test_directory_path_loads_hyperkit_toml(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "hyperkit.toml"
    )

    path.write_text(
        """
[project]
name = "directory-test"
""".strip(),
        encoding="utf-8",
    )

    config = load_project_config(
        tmp_path
    )

    assert config.path == path.resolve()


def test_explicit_schema_version(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "hyperkit.toml"
    )

    path.write_text(
        """
[hyperkit]
schema_version = 1
""".strip(),
        encoding="utf-8",
    )

    config = load_project_config(path)

    assert config.schema_version == 1


def test_unsupported_schema_version_rejected(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "hyperkit.toml"
    )

    path.write_text(
        """
[hyperkit]
schema_version = 999
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(
        HyperKitConfigurationError
    ):
        load_project_config(path)


def test_invalid_toml_is_rejected(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "hyperkit.toml"
    )

    path.write_text(
        "[broken",
        encoding="utf-8",
    )

    with pytest.raises(
        HyperKitConfigurationError
    ):
        load_project_config(path)


def test_missing_project_config_is_rejected(
    tmp_path: Path,
):
    with pytest.raises(
        HyperKitConfigurationError
    ):
        load_project_config(
            tmp_path
        )


def test_sdk_config_can_be_loaded_from_project(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "hyperkit.toml"
    )

    path.write_text(
        """
[sdk]
debug = true
strict = false
log_level = "DEBUG"
""".strip(),
        encoding="utf-8",
    )

    project = load_project_config(path)

    sdk = project.get_sdk_config()

    assert sdk.debug is True
    assert sdk.strict is False
    assert sdk.log_level == "DEBUG"


def test_find_project_config_searches_parents(
    tmp_path: Path,
):
    config_path = (
        tmp_path
        / "hyperkit.toml"
    )

    config_path.write_text(
        "[project]\nname = \"demo\"",
        encoding="utf-8",
    )

    nested = (
        tmp_path
        / "src"
        / "game"
    )

    nested.mkdir(
        parents=True,
    )

    result = find_project_config(
        nested
    )

    assert result == config_path.resolve()


def test_deprecation_warning_type():
    assert issubclass(
        HyperKitDeprecationWarning,
        DeprecationWarning,
    )


def test_build_deprecation_message():
    message = build_deprecation_message(
        "old_api",
        since="0.2",
    )

    assert "old_api is deprecated" in message
    assert "HyperKit 0.2" in message


def test_deprecation_message_supports_removal():
    message = build_deprecation_message(
        "old_api",
        since="0.2",
        removal="1.0",
    )

    assert "HyperKit 1.0" in message


def test_deprecation_message_supports_replacement():
    message = build_deprecation_message(
        "old_api",
        since="0.2",
        replacement="new_api",
    )

    assert "Use new_api instead." in message


def test_warn_deprecated_emits_hyperkit_warning():
    with pytest.warns(
        HyperKitDeprecationWarning
    ):
        warn_deprecated(
            "old_api",
            since="0.2",
        )


def test_deprecated_decorator_warns_and_preserves_behavior():
    @deprecated(
        since="0.2",
        replacement="new_function",
    )
    def old_function(
        value: int,
    ) -> int:
        return value * 2

    with pytest.warns(
        HyperKitDeprecationWarning
    ):
        result = old_function(5)

    assert result == 10
    assert old_function.__name__ == "old_function"
