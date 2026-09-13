"""Runtime lifecycle and SDK context for GameViz HyperKit.

The runtime context provides a stable foundation for systems that need
to share configuration, services, lifecycle state, and runtime metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from .config import SDKConfig
from .errors import HyperKitRuntimeError


class RuntimeState(str, Enum):
    """Lifecycle states for a HyperKit SDK context."""

    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    BACKGROUND = "background"
    STOPPED = "stopped"


@dataclass
class SDKContext:
    """Shared runtime context for HyperKit systems."""

    config: SDKConfig = field(
        default_factory=SDKConfig
    )

    state: RuntimeState = field(
        default=RuntimeState.CREATED,
        init=False,
    )

    services: Dict[
        str,
        object,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    metadata: Dict[
        str,
        object,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    @property
    def is_running(
        self,
    ) -> bool:
        return (
            self.state
            == RuntimeState.RUNNING
        )

    @property
    def is_paused(
        self,
    ) -> bool:
        return (
            self.state
            == RuntimeState.PAUSED
        )

    @property
    def is_background(
        self,
    ) -> bool:
        return (
            self.state
            == RuntimeState.BACKGROUND
        )

    @property
    def is_stopped(
        self,
    ) -> bool:
        return (
            self.state
            == RuntimeState.STOPPED
        )

    @property
    def is_suspended(
        self,
    ) -> bool:
        return self.state in {
            RuntimeState.PAUSED,
            RuntimeState.BACKGROUND,
        }

    def start(
        self,
    ) -> "SDKContext":
        self.state = (
            RuntimeState.RUNNING
        )

        return self

    def pause(
        self,
    ) -> "SDKContext":
        if (
            self.state
            == RuntimeState.PAUSED
        ):
            return self

        if (
            self.state
            != RuntimeState.RUNNING
        ):
            raise HyperKitRuntimeError(
                "HyperKit runtime can only "
                "be paused while running."
            )

        self.state = (
            RuntimeState.PAUSED
        )

        return self

    def background(
        self,
    ) -> "SDKContext":
        if (
            self.state
            == RuntimeState.BACKGROUND
        ):
            return self

        if self.state not in {
            RuntimeState.RUNNING,
            RuntimeState.PAUSED,
        }:
            raise HyperKitRuntimeError(
                "HyperKit runtime can only enter "
                "the background after it has started."
            )

        self.state = (
            RuntimeState.BACKGROUND
        )

        return self

    def resume(
        self,
    ) -> "SDKContext":
        if (
            self.state
            == RuntimeState.RUNNING
        ):
            return self

        if self.state not in {
            RuntimeState.PAUSED,
            RuntimeState.BACKGROUND,
        }:
            raise HyperKitRuntimeError(
                "HyperKit runtime can only resume "
                "from paused or background state."
            )

        self.state = (
            RuntimeState.RUNNING
        )

        return self

    def stop(
        self,
    ) -> "SDKContext":
        self.state = (
            RuntimeState.STOPPED
        )

        return self

    def reset(
        self,
    ) -> "SDKContext":
        self.state = (
            RuntimeState.CREATED
        )

        self.services.clear()
        self.metadata.clear()

        return self

    def require_running(
        self,
    ) -> None:
        if not self.is_running:
            raise HyperKitRuntimeError(
                "HyperKit runtime is not running. "
                "Call context.start() before "
                "using this operation."
            )

    def register_service(
        self,
        name: str,
        service: object,
        *,
        replace: bool = False,
    ) -> object:
        normalized_name = (
            self._normalize_name(
                name
            )
        )

        if (
            normalized_name
            in self.services
            and not replace
        ):
            raise HyperKitRuntimeError(
                f"HyperKit service "
                f"'{normalized_name}' "
                "is already registered."
            )

        self.services[
            normalized_name
        ] = service

        return service

    def get_service(
        self,
        name: str,
        default: Optional[
            object
        ] = None,
    ) -> Optional[object]:
        normalized_name = (
            self._normalize_name(
                name
            )
        )

        return self.services.get(
            normalized_name,
            default,
        )

    def has_service(
        self,
        name: str,
    ) -> bool:
        normalized_name = (
            self._normalize_name(
                name
            )
        )

        return (
            normalized_name
            in self.services
        )

    def unregister_service(
        self,
        name: str,
    ) -> Optional[object]:
        normalized_name = (
            self._normalize_name(
                name
            )
        )

        return self.services.pop(
            normalized_name,
            None,
        )

    def set_metadata(
        self,
        key: str,
        value: object,
    ) -> object:
        normalized_key = (
            self._normalize_name(
                key
            )
        )

        self.metadata[
            normalized_key
        ] = value

        return value

    def get_metadata(
        self,
        key: str,
        default: Optional[
            object
        ] = None,
    ) -> Optional[object]:
        normalized_key = (
            self._normalize_name(
                key
            )
        )

        return self.metadata.get(
            normalized_key,
            default,
        )

    def remove_metadata(
        self,
        key: str,
    ) -> Optional[object]:
        normalized_key = (
            self._normalize_name(
                key
            )
        )

        return self.metadata.pop(
            normalized_key,
            None,
        )

    @staticmethod
    def _normalize_name(
        name: str,
    ) -> str:
        if not isinstance(
            name,
            str,
        ):
            raise HyperKitRuntimeError(
                "Runtime names must be strings."
            )

        normalized = (
            name.strip()
        )

        if not normalized:
            raise HyperKitRuntimeError(
                "Runtime names cannot be empty."
            )

        return normalized


_default_context: Optional[
    SDKContext
] = None


def create_context(
    config: Optional[
        SDKConfig
    ] = None,
) -> SDKContext:
    if config is None:
        config = SDKConfig()

    if not isinstance(
        config,
        SDKConfig,
    ):
        raise HyperKitRuntimeError(
            "config must be an "
            "SDKConfig instance."
        )

    return SDKContext(
        config=config
    )


def get_default_context(
) -> SDKContext:
    global _default_context

    if _default_context is None:
        _default_context = (
            create_context()
        )

    return _default_context


def set_default_context(
    context: SDKContext,
) -> SDKContext:
    global _default_context

    if not isinstance(
        context,
        SDKContext,
    ):
        raise HyperKitRuntimeError(
            "Default context must be "
            "an SDKContext instance."
        )

    _default_context = context

    return context


def reset_default_context(
) -> None:
    global _default_context

    _default_context = None
