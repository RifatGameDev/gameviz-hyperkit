"""Runtime lifecycle integration for GameViz HyperKit."""

from __future__ import annotations

from typing import Optional

from .environment import (
    detect_runtime_environment,
)
from .errors import HyperKitRuntimeError
from .logging import configure_logging
from .runtime import (
    SDKContext,
    get_default_context,
)


def _resolve_context(
    context: Optional[
        SDKContext
    ],
) -> SDKContext:
    if context is None:
        context = (
            get_default_context()
        )

    if not isinstance(
        context,
        SDKContext,
    ):
        raise HyperKitRuntimeError(
            "context must be an "
            "SDKContext instance."
        )

    return context


def _record_lifecycle_state(
    context: SDKContext,
) -> None:
    context.set_metadata(
        "lifecycle_state",
        context.state.value,
    )


def _notify_runtime_services(
    context: SDKContext,
    method_name: str,
) -> None:
    """Notify registered services that opt into runtime lifecycle hooks."""

    seen: set[int] = set()

    for service in list(
        context.services.values()
    ):
        identity = id(
            service
        )

        if identity in seen:
            continue

        seen.add(
            identity
        )

        callback = getattr(
            service,
            method_name,
            None,
        )

        if callable(
            callback
        ):
            callback()


def start_runtime(
    context: Optional[
        SDKContext
    ] = None,
) -> SDKContext:
    runtime = _resolve_context(
        context
    )

    configure_logging(
        runtime.config
    )

    environment = (
        detect_runtime_environment()
    )

    runtime.set_metadata(
        "environment",
        environment.to_dict(),
    )

    runtime.set_metadata(
        "mobile_environment",
        environment.to_extended_dict(),
    )

    runtime.set_metadata(
        "device_family",
        environment.device_family,
    )

    runtime.start()

    _record_lifecycle_state(
        runtime
    )

    _notify_runtime_services(
        runtime,
        "on_runtime_start",
    )

    return runtime


def pause_runtime(
    context: Optional[
        SDKContext
    ] = None,
) -> SDKContext:
    runtime = _resolve_context(
        context
    )

    runtime.pause()

    _record_lifecycle_state(
        runtime
    )

    _notify_runtime_services(
        runtime,
        "on_runtime_pause",
    )

    return runtime


def background_runtime(
    context: Optional[
        SDKContext
    ] = None,
) -> SDKContext:
    runtime = _resolve_context(
        context
    )

    runtime.background()

    _record_lifecycle_state(
        runtime
    )

    _notify_runtime_services(
        runtime,
        "on_runtime_background",
    )

    return runtime


def resume_runtime(
    context: Optional[
        SDKContext
    ] = None,
) -> SDKContext:
    runtime = _resolve_context(
        context
    )

    runtime.resume()

    _record_lifecycle_state(
        runtime
    )

    _notify_runtime_services(
        runtime,
        "on_runtime_resume",
    )

    return runtime


def stop_runtime(
    context: Optional[
        SDKContext
    ] = None,
) -> SDKContext:
    runtime = _resolve_context(
        context
    )

    runtime.stop()

    _record_lifecycle_state(
        runtime
    )

    _notify_runtime_services(
        runtime,
        "on_runtime_stop",
    )

    return runtime


def run_game(
    game: object,
    *,
    context: Optional[
        SDKContext
    ] = None,
) -> object:
    run_method = getattr(
        game,
        "run",
        None,
    )

    if not callable(
        run_method
    ):
        raise HyperKitRuntimeError(
            "game must provide a "
            "callable run() method."
        )

    runtime = start_runtime(
        context
    )

    try:
        return run_method()

    finally:
        stop_runtime(
            runtime
        )
