"""Deprecation helpers for GameViz HyperKit."""

from __future__ import annotations

import warnings
from functools import wraps
from typing import Callable, Optional, TypeVar, cast


class HyperKitDeprecationWarning(
    DeprecationWarning
):
    """Warning emitted for deprecated HyperKit APIs."""


F = TypeVar(
    "F",
    bound=Callable[..., object],
)


def build_deprecation_message(
    name: str,
    *,
    since: str,
    removal: Optional[str] = None,
    replacement: Optional[str] = None,
) -> str:
    """Build a consistent HyperKit deprecation message."""

    if not isinstance(name, str):
        raise TypeError(
            "Deprecated API name must be a string."
        )

    normalized_name = name.strip()

    if not normalized_name:
        raise ValueError(
            "Deprecated API name cannot be empty."
        )

    if not isinstance(since, str):
        raise TypeError(
            "Deprecation version must be a string."
        )

    normalized_since = since.strip()

    if not normalized_since:
        raise ValueError(
            "Deprecation version cannot be empty."
        )

    message = (
        f"{normalized_name} is deprecated "
        f"since HyperKit {normalized_since}."
    )

    if removal is not None:
        normalized_removal = (
            str(removal).strip()
        )

        if normalized_removal:
            message += (
                f" It is planned for removal "
                f"in HyperKit {normalized_removal}."
            )

    if replacement is not None:
        normalized_replacement = (
            str(replacement).strip()
        )

        if normalized_replacement:
            message += (
                f" Use {normalized_replacement} instead."
            )

    return message


def warn_deprecated(
    name: str,
    *,
    since: str,
    removal: Optional[str] = None,
    replacement: Optional[str] = None,
    stacklevel: int = 2,
) -> None:
    """Emit a HyperKit deprecation warning."""

    message = build_deprecation_message(
        name,
        since=since,
        removal=removal,
        replacement=replacement,
    )

    warnings.warn(
        message,
        HyperKitDeprecationWarning,
        stacklevel=stacklevel,
    )


def deprecated(
    *,
    since: str,
    removal: Optional[str] = None,
    replacement: Optional[str] = None,
) -> Callable[[F], F]:
    """Mark a callable as deprecated.

    The warning is emitted when the callable is used.
    """

    def decorator(
        function: F,
    ) -> F:
        @wraps(function)
        def wrapper(
            *args: object,
            **kwargs: object,
        ) -> object:
            warn_deprecated(
                function.__qualname__,
                since=since,
                removal=removal,
                replacement=replacement,
                stacklevel=3,
            )

            return function(
                *args,
                **kwargs,
            )

        return cast(
            F,
            wrapper,
        )

    return decorator
