"""Public API contract for GameViz HyperKit."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Optional

from .errors import HyperKitCompatibilityError


REQUIRED_PUBLIC_API = frozenset(
    {
        # Existing core game API
        "Game",
        "GameObject",
        "Scene",
        "SaveManager",
        "ScoreManager",

        # Phase 70
        "API_VERSION",
        "SDKConfig",
        "HyperKitError",
        "HyperKitConfigurationError",
        "HyperKitCompatibilityError",
        "HyperKitRuntimeError",
        "HyperKitValidationError",
        "get_api_version",
        "is_api_compatible",
        "require_api_version",

        # Phase 71
        "RuntimeState",
        "SDKContext",
        "create_context",
        "get_default_context",
        "set_default_context",
        "reset_default_context",

        # Phase 72
        "PlatformKind",
        "RuntimeEnvironment",
        "detect_platform",
        "detect_runtime_environment",
        "configure_logging",
        "get_logger",
        "log_event",
        "PROJECT_CONFIG_FILENAME",
        "PROJECT_CONFIG_SCHEMA_VERSION",
        "ProjectConfig",
        "find_project_config",
        "load_project_config",
        "HyperKitDeprecationWarning",
        "build_deprecation_message",
        "deprecated",
        "warn_deprecated",
        "start_runtime",
        "stop_runtime",
        "run_game",
    }
)


def get_missing_public_api(
    namespace: Mapping[str, object],
) -> tuple[str, ...]:
    """Return required public API names missing from a namespace."""

    missing = (
        REQUIRED_PUBLIC_API
        - set(namespace)
    )

    return tuple(
        sorted(missing)
    )


def validate_public_api(
    namespace: Optional[
        Mapping[str, object]
    ] = None,
) -> None:
    """Validate the HyperKit public API contract."""

    if namespace is None:
        import hyperkit

        namespace = vars(hyperkit)

    missing = get_missing_public_api(
        namespace
    )

    if missing:
        names = ", ".join(missing)

        raise HyperKitCompatibilityError(
            "HyperKit public API contract "
            f"is missing: {names}."
        )
