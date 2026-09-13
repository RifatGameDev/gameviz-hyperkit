"""Public API compatibility helpers for GameViz HyperKit."""

from __future__ import annotations

from .errors import HyperKitCompatibilityError


API_VERSION = "0.2"


def _parse_api_version(version: str) -> tuple[int, int]:
    """Parse a HyperKit API version in MAJOR.MINOR format."""

    if not isinstance(version, str):
        raise HyperKitCompatibilityError(
            "HyperKit API version must be a string in MAJOR.MINOR format."
        )

    parts = version.strip().split(".")

    if len(parts) != 2:
        raise HyperKitCompatibilityError(
            f"Invalid HyperKit API version '{version}'. "
            "Expected MAJOR.MINOR format, for example '0.2'."
        )

    try:
        major = int(parts[0])
        minor = int(parts[1])
    except ValueError as exc:
        raise HyperKitCompatibilityError(
            f"Invalid HyperKit API version '{version}'. "
            "Major and minor versions must be integers."
        ) from exc

    if major < 0 or minor < 0:
        raise HyperKitCompatibilityError(
            "HyperKit API version values cannot be negative."
        )

    return major, minor


def get_api_version() -> str:
    """Return the current public HyperKit API version."""

    return API_VERSION


def is_api_compatible(required_version: str) -> bool:
    """Return whether the current API satisfies a requested API version.

    HyperKit uses major-version compatibility.

    Within the same major version, a newer minor API is considered
    compatible with an older requested minor API.

    Examples for API version 0.2:

        0.1 -> compatible
        0.2 -> compatible
        0.3 -> incompatible
        1.0 -> incompatible
    """

    current_major, current_minor = _parse_api_version(API_VERSION)
    required_major, required_minor = _parse_api_version(required_version)

    return (
        current_major == required_major
        and current_minor >= required_minor
    )


def require_api_version(required_version: str) -> None:
    """Require a compatible HyperKit API version.

    Raises:
        HyperKitCompatibilityError:
            If the requested API is not compatible with this SDK.
    """

    if is_api_compatible(required_version):
        return

    raise HyperKitCompatibilityError(
        f"HyperKit API {required_version} is required, "
        f"but this SDK provides API {API_VERSION}."
    )
