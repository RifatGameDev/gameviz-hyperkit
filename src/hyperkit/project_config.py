"""Project configuration support for GameViz HyperKit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .config import SDKConfig
from .errors import HyperKitConfigurationError


PROJECT_CONFIG_FILENAME = "hyperkit.toml"

PROJECT_CONFIG_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ProjectConfig:
    """Loaded HyperKit project configuration."""

    path: Path
    data: Dict[str, object]
    schema_version: int = PROJECT_CONFIG_SCHEMA_VERSION

    def get_section(
        self,
        name: str,
    ) -> Dict[str, object]:
        """Return a configuration section.

        Missing sections return an empty dictionary.
        """

        if not isinstance(name, str):
            raise HyperKitConfigurationError(
                "Configuration section name must be a string."
            )

        normalized_name = name.strip()

        if not normalized_name:
            raise HyperKitConfigurationError(
                "Configuration section name cannot be empty."
            )

        value = self.data.get(
            normalized_name,
            {},
        )

        if value is None:
            return {}

        if not isinstance(value, dict):
            raise HyperKitConfigurationError(
                f"Configuration section "
                f"'{normalized_name}' must be a TOML table."
            )

        return dict(value)

    def get(
        self,
        key: str,
        default: object = None,
    ) -> object:
        """Return a top-level configuration value."""

        if not isinstance(key, str):
            raise HyperKitConfigurationError(
                "Configuration key must be a string."
            )

        normalized_key = key.strip()

        if not normalized_key:
            raise HyperKitConfigurationError(
                "Configuration key cannot be empty."
            )

        return self.data.get(
            normalized_key,
            default,
        )

    def get_sdk_config(self) -> SDKConfig:
        """Create SDKConfig from the optional [sdk] section."""

        section = self.get_section("sdk")

        return SDKConfig(
            debug=section.get(
                "debug",
                False,
            ),
            strict=section.get(
                "strict",
                True,
            ),
            log_level=section.get(
                "log_level",
                "INFO",
            ),
        )


def find_project_config(
    start: Optional[Path | str] = None,
) -> Optional[Path]:
    """Search for hyperkit.toml from a path upward.

    The search continues through parent directories until
    the filesystem root is reached.
    """

    if start is None:
        current = Path.cwd()
    else:
        current = Path(start)

    current = current.expanduser().resolve()

    if current.is_file():
        current = current.parent

    while True:
        candidate = (
            current
            / PROJECT_CONFIG_FILENAME
        )

        if candidate.is_file():
            return candidate

        parent = current.parent

        if parent == current:
            break

        current = parent

    return None


def load_project_config(
    path: Optional[Path | str] = None,
) -> ProjectConfig:
    """Load and validate a HyperKit project configuration.

    Args:
        path:
            Path to hyperkit.toml or to a project directory.
            When omitted, HyperKit searches upward from the
            current working directory.

    Raises:
        HyperKitConfigurationError:
            If the file cannot be found, parsed, or validated.
    """

    config_path = _resolve_config_path(path)

    try:
        with config_path.open("rb") as file:
            data = tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise HyperKitConfigurationError(
            f"Unable to load HyperKit project configuration "
            f"from '{config_path}': {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise HyperKitConfigurationError(
            "HyperKit project configuration "
            "must contain a TOML table."
        )

    schema_version = _read_schema_version(
        data
    )

    return ProjectConfig(
        path=config_path,
        data=dict(data),
        schema_version=schema_version,
    )


def _resolve_config_path(
    path: Optional[Path | str],
) -> Path:
    """Resolve a configuration file path."""

    if path is None:
        discovered = find_project_config()

        if discovered is None:
            raise HyperKitConfigurationError(
                f"Could not find "
                f"'{PROJECT_CONFIG_FILENAME}' "
                "in the current directory or its parents."
            )

        return discovered

    candidate = (
        Path(path)
        .expanduser()
        .resolve()
    )

    if candidate.is_dir():
        candidate = (
            candidate
            / PROJECT_CONFIG_FILENAME
        )

    if not candidate.is_file():
        raise HyperKitConfigurationError(
            f"HyperKit project configuration "
            f"does not exist: '{candidate}'."
        )

    return candidate


def _read_schema_version(
    data: Dict[str, object],
) -> int:
    """Read and validate the configuration schema version."""

    hyperkit_section = data.get(
        "hyperkit",
        {},
    )

    if hyperkit_section is None:
        hyperkit_section = {}

    if not isinstance(
        hyperkit_section,
        dict,
    ):
        raise HyperKitConfigurationError(
            "The [hyperkit] configuration section "
            "must be a TOML table."
        )

    version = hyperkit_section.get(
        "schema_version",
        PROJECT_CONFIG_SCHEMA_VERSION,
    )

    if type(version) is not int:
        raise HyperKitConfigurationError(
            "hyperkit.schema_version "
            "must be an integer."
        )

    if version != PROJECT_CONFIG_SCHEMA_VERSION:
        raise HyperKitConfigurationError(
            f"Unsupported HyperKit project "
            f"configuration schema version "
            f"'{version}'. "
            f"Supported version: "
            f"{PROJECT_CONFIG_SCHEMA_VERSION}."
        )

    return version
