"""Structured logging helpers for GameViz HyperKit.

HyperKit uses a dedicated logger so SDK systems can produce consistent
diagnostic output without scattering direct print() calls throughout
the package.

Applications remain free to use Python's standard logging system
alongside HyperKit.
"""

from __future__ import annotations

import logging
from typing import Optional

from .config import SDKConfig
from .errors import HyperKitConfigurationError


LOGGER_NAME = "hyperkit"

_HANDLER_MARKER = "_hyperkit_stream_handler"


def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """Return the HyperKit logger or one of its child loggers."""

    if name is None:
        return logging.getLogger(LOGGER_NAME)

    if not isinstance(name, str):
        raise HyperKitConfigurationError(
            "Logger name must be a string."
        )

    normalized_name = name.strip()

    if not normalized_name:
        raise HyperKitConfigurationError(
            "Logger name cannot be empty."
        )

    if normalized_name == LOGGER_NAME:
        return logging.getLogger(LOGGER_NAME)

    if normalized_name.startswith(
        f"{LOGGER_NAME}."
    ):
        return logging.getLogger(normalized_name)

    return logging.getLogger(
        f"{LOGGER_NAME}.{normalized_name}"
    )


def configure_logging(
    config: Optional[SDKConfig] = None,
    *,
    quiet: bool = False,
) -> logging.Logger:
    """Configure HyperKit's root SDK logger.

    Args:
        config:
            SDK configuration controlling the log level.

        quiet:
            Suppress console output while keeping the logging
            infrastructure available.

    Returns:
        The configured HyperKit logger.
    """

    if config is None:
        config = SDKConfig()

    if not isinstance(config, SDKConfig):
        raise HyperKitConfigurationError(
            "config must be an SDKConfig instance."
        )

    if type(quiet) is not bool:
        raise HyperKitConfigurationError(
            "quiet must be a boolean value."
        )

    logger = get_logger()

    level = getattr(
        logging,
        config.log_level,
        logging.INFO,
    )

    logger.setLevel(level)
    logger.propagate = False

    handler = _get_hyperkit_handler(logger)

    if handler is None:
        handler = logging.StreamHandler()

        setattr(
            handler,
            _HANDLER_MARKER,
            True,
        )

        formatter = logging.Formatter(
            "%(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    if quiet:
        handler.setLevel(
            logging.CRITICAL + 1
        )
    else:
        handler.setLevel(level)

    return logger


def _get_hyperkit_handler(
    logger: logging.Logger,
) -> Optional[logging.Handler]:
    """Return the console handler owned by HyperKit."""

    for handler in logger.handlers:
        if getattr(
            handler,
            _HANDLER_MARKER,
            False,
        ):
            return handler

    return None


def debug(
    message: str,
    *args: object,
) -> None:
    """Write a HyperKit debug message."""

    get_logger().debug(
        message,
        *args,
    )


def info(
    message: str,
    *args: object,
) -> None:
    """Write a HyperKit informational message."""

    get_logger().info(
        message,
        *args,
    )


def warning(
    message: str,
    *args: object,
) -> None:
    """Write a HyperKit warning message."""

    get_logger().warning(
        message,
        *args,
    )


def error(
    message: str,
    *args: object,
) -> None:
    """Write a HyperKit error message."""

    get_logger().error(
        message,
        *args,
    )


def critical(
    message: str,
    *args: object,
) -> None:
    """Write a HyperKit critical message."""

    get_logger().critical(
        message,
        *args,
    )


def log_event(
    level: str,
    event: str,
    **fields: object,
) -> None:
    """Write a small structured event message.

    Example:

        log_event(
            "INFO",
            "runtime_started",
            platform="windows",
        )

    produces a message similar to:

        event=runtime_started platform='windows'
    """

    if not isinstance(level, str):
        raise HyperKitConfigurationError(
            "Event log level must be a string."
        )

    normalized_level = level.strip().upper()

    valid_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    if normalized_level not in valid_levels:
        raise HyperKitConfigurationError(
            f"Unsupported event log level '{level}'."
        )

    if not isinstance(event, str):
        raise HyperKitConfigurationError(
            "Event name must be a string."
        )

    normalized_event = event.strip()

    if not normalized_event:
        raise HyperKitConfigurationError(
            "Event name cannot be empty."
        )

    message_parts = [
        f"event={normalized_event}",
    ]

    for key in sorted(fields):
        message_parts.append(
            f"{key}={fields[key]!r}"
        )

    get_logger().log(
        valid_levels[normalized_level],
        " ".join(message_parts),
    )
