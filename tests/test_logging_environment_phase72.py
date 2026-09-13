import logging

import pytest

from hyperkit.config import SDKConfig
from hyperkit.environment import (
    PlatformKind,
    RuntimeEnvironment,
    detect_platform,
    detect_runtime_environment,
)
from hyperkit.errors import (
    HyperKitConfigurationError,
)
from hyperkit.logging import (
    configure_logging,
    get_logger,
    log_event,
)


def test_get_logger_returns_hyperkit_root_logger():
    logger = get_logger()

    assert logger.name == "hyperkit"


def test_get_logger_creates_child_logger():
    logger = get_logger("runtime")

    assert logger.name == "hyperkit.runtime"


def test_existing_hyperkit_logger_name_is_preserved():
    logger = get_logger(
        "hyperkit.android"
    )

    assert logger.name == "hyperkit.android"


def test_invalid_logger_name_is_rejected():
    with pytest.raises(
        HyperKitConfigurationError
    ):
        get_logger("   ")


def test_configure_logging_respects_sdk_log_level():
    config = SDKConfig(
        log_level="DEBUG",
    )

    logger = configure_logging(config)

    assert logger.level == logging.DEBUG


def test_configure_logging_does_not_duplicate_handler():
    config = SDKConfig()

    logger = configure_logging(config)

    before = len(
        [
            handler
            for handler in logger.handlers
            if getattr(
                handler,
                "_hyperkit_stream_handler",
                False,
            )
        ]
    )

    configure_logging(config)

    after = len(
        [
            handler
            for handler in logger.handlers
            if getattr(
                handler,
                "_hyperkit_stream_handler",
                False,
            )
        ]
    )

    assert before == 1
    assert after == 1


def test_quiet_logging_uses_suppressed_handler_level():
    logger = configure_logging(
        SDKConfig(),
        quiet=True,
    )

    handlers = [
        handler
        for handler in logger.handlers
        if getattr(
            handler,
            "_hyperkit_stream_handler",
            False,
        )
    ]

    assert len(handlers) == 1

    assert handlers[0].level > logging.CRITICAL


def test_log_event_validates_level():
    configure_logging(
        SDKConfig(),
        quiet=True,
    )

    with pytest.raises(
        HyperKitConfigurationError
    ):
        log_event(
            "TRACE",
            "test_event",
        )


def test_windows_platform_detection():
    result = detect_platform(
        environ={},
        platform_name="win32",
        system_name="Windows",
    )

    assert result == PlatformKind.WINDOWS


def test_linux_platform_detection():
    result = detect_platform(
        environ={},
        platform_name="linux",
        system_name="Linux",
    )

    assert result == PlatformKind.LINUX


def test_android_environment_detection():
    result = detect_platform(
        environ={
            "ANDROID_ARGUMENT": "1",
        },
        platform_name="linux",
        system_name="Linux",
    )

    assert result == PlatformKind.ANDROID


def test_runtime_environment_contains_python_metadata():
    environment = (
        detect_runtime_environment()
    )

    assert isinstance(
        environment,
        RuntimeEnvironment,
    )

    assert environment.python_version
    assert environment.python_implementation
    assert environment.executable

    assert isinstance(
        environment.platform,
        PlatformKind,
    )
