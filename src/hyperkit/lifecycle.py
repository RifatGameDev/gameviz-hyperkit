"""Runtime lifecycle integration for GameViz HyperKit."""

from __future__ import annotations

from typing import Optional

from .environment import detect_runtime_environment
from .errors import HyperKitRuntimeError
from .logging import configure_logging
from .runtime import (
    SDKContext,
    get_default_context,
)


def start_runtime(
    context: Optional[SDKContext] = None,
) -> SDKContext:
    """Start a HyperKit runtime context.

    Logging and runtime environment metadata are initialized
    before the context enters the running state.
    """

    if context is None:
        context = get_default_context()

    if not isinstance(context, SDKContext):
        raise HyperKitRuntimeError(
            "context must be an SDKContext instance."
        )

    configure_logging(context.config)

    environment = detect_runtime_environment()

    context.set_metadata(
        "environment",
        environment.to_dict(),
    )

    context.start()

    return context


def stop_runtime(
    context: Optional[SDKContext] = None,
) -> SDKContext:
    """Stop a HyperKit runtime context."""

    if context is None:
        context = get_default_context()

    if not isinstance(context, SDKContext):
        raise HyperKitRuntimeError(
            "context must be an SDKContext instance."
        )

    context.stop()

    return context


def run_game(
    game: object,
    *,
    context: Optional[SDKContext] = None,
) -> object:
    """Run a HyperKit game inside an SDK runtime context.

    The runtime is always stopped when the game exits,
    including when the game raises an exception.
    """

    run_method = getattr(
        game,
        "run",
        None,
    )

    if not callable(run_method):
        raise HyperKitRuntimeError(
            "game must provide a callable run() method."
        )

    runtime = start_runtime(context)

    try:
        return run_method()
    finally:
        stop_runtime(runtime)
