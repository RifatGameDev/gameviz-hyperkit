import pytest

from hyperkit import (
    SDKConfig,
    SDKContext,
    RuntimeState,
    HyperKitRuntimeError,
    create_context,
    get_default_context,
    reset_default_context,
    set_default_context,
)


def setup_function():
    reset_default_context()


def teardown_function():
    reset_default_context()


def test_new_context_starts_in_created_state():
    context = SDKContext()

    assert context.state == RuntimeState.CREATED
    assert context.is_running is False
    assert context.is_stopped is False


def test_context_can_start_and_stop():
    context = SDKContext()

    result = context.start()

    assert result is context
    assert context.state == RuntimeState.RUNNING
    assert context.is_running is True

    result = context.stop()

    assert result is context
    assert context.state == RuntimeState.STOPPED
    assert context.is_stopped is True


def test_start_and_stop_are_idempotent():
    context = SDKContext()

    context.start()
    context.start()

    assert context.state == RuntimeState.RUNNING

    context.stop()
    context.stop()

    assert context.state == RuntimeState.STOPPED


def test_require_running_rejects_inactive_context():
    context = SDKContext()

    with pytest.raises(HyperKitRuntimeError):
        context.require_running()

    context.start()
    context.require_running()

    context.stop()

    with pytest.raises(HyperKitRuntimeError):
        context.require_running()


def test_context_reset_preserves_config_and_clears_runtime_data():
    config = SDKConfig(
        debug=True,
        log_level="DEBUG",
    )

    context = SDKContext(config=config)

    context.start()
    context.register_service(
        "analytics",
        object(),
    )
    context.set_metadata(
        "platform",
        "desktop",
    )

    result = context.reset()

    assert result is context

    assert context.state == RuntimeState.CREATED
    assert context.config is config
    assert context.services == {}
    assert context.metadata == {}


def test_context_service_registry():
    context = SDKContext()

    service = object()

    assert context.register_service(
        "audio",
        service,
    ) is service

    assert context.has_service("audio") is True
    assert context.get_service("audio") is service

    assert context.unregister_service("audio") is service
    assert context.has_service("audio") is False
    assert context.get_service("audio") is None


def test_duplicate_service_requires_replace_flag():
    context = SDKContext()

    first = object()
    second = object()

    context.register_service(
        "analytics",
        first,
    )

    with pytest.raises(HyperKitRuntimeError):
        context.register_service(
            "analytics",
            second,
        )

    context.register_service(
        "analytics",
        second,
        replace=True,
    )

    assert context.get_service("analytics") is second


def test_context_metadata():
    context = SDKContext()

    context.set_metadata(
        "platform",
        "windows",
    )

    assert context.get_metadata("platform") == "windows"

    assert context.remove_metadata("platform") == "windows"

    assert context.get_metadata("platform") is None


def test_create_context_accepts_sdk_config():
    config = SDKConfig(
        debug=True,
        strict=False,
        log_level="WARNING",
    )

    context = create_context(config)

    assert isinstance(context, SDKContext)
    assert context.config is config


def test_default_context_is_lazy_singleton():
    first = get_default_context()
    second = get_default_context()

    assert isinstance(first, SDKContext)
    assert first is second


def test_default_context_can_be_replaced():
    context = SDKContext()

    result = set_default_context(context)

    assert result is context
    assert get_default_context() is context


def test_reset_default_context_creates_fresh_context():
    first = get_default_context()

    reset_default_context()

    second = get_default_context()

    assert first is not second


def test_invalid_context_names_raise_runtime_error():
    context = SDKContext()

    with pytest.raises(HyperKitRuntimeError):
        context.register_service(
            "",
            object(),
        )

    with pytest.raises(HyperKitRuntimeError):
        context.set_metadata(
            "   ",
            "value",
        )


def test_invalid_default_context_is_rejected():
    with pytest.raises(HyperKitRuntimeError):
        set_default_context("invalid")  # type: ignore
