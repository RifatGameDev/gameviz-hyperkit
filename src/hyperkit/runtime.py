"""Runtime lifecycle and SDK context for GameViz HyperKit.

The runtime context provides a small, stable foundation for systems that
need to share configuration, services, and runtime metadata.

Future HyperKit systems such as Android integration, advertising,
analytics, plugins, platform services, and developer tooling can build
on this context without relying on unrelated module-level globals.
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
    STOPPED = "stopped"


@dataclass
class SDKContext:
    """Shared runtime context for HyperKit systems.

    A context owns:

    - SDK configuration
    - runtime lifecycle state
    - registered runtime services
    - lightweight runtime metadata

    Contexts are intentionally independent so tests, tools, generated
    projects, and future plugin systems can create isolated runtimes.
    """

    config: SDKConfig = field(default_factory=SDKConfig)

    state: RuntimeState = field(
        default=RuntimeState.CREATED,
        init=False,
    )

    services: Dict[str, object] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    metadata: Dict[str, object] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    @property
    def is_running(self) -> bool:
        """Return whether the runtime is currently running."""

        return self.state == RuntimeState.RUNNING

    @property
    def is_stopped(self) -> bool:
        """Return whether the runtime has been stopped."""

        return self.state == RuntimeState.STOPPED

    def start(self) -> "SDKContext":
        """Start or restart the runtime.

        Calling start repeatedly is safe and idempotent.
        """

        self.state = RuntimeState.RUNNING
        return self

    def stop(self) -> "SDKContext":
        """Stop the runtime.

        Calling stop repeatedly is safe and idempotent.
        """

        self.state = RuntimeState.STOPPED
        return self

    def reset(self) -> "SDKContext":
        """Reset the context to its initial runtime state.

        Configuration is preserved while runtime services and metadata
        are cleared.
        """

        self.state = RuntimeState.CREATED
        self.services.clear()
        self.metadata.clear()

        return self

    def require_running(self) -> None:
        """Require this context to be running.

        Raises:
            HyperKitRuntimeError:
                If the runtime has not been started or has been stopped.
        """

        if not self.is_running:
            raise HyperKitRuntimeError(
                "HyperKit runtime is not running. "
                "Call context.start() before using this operation."
            )

    def register_service(
        self,
        name: str,
        service: object,
        *,
        replace: bool = False,
    ) -> object:
        """Register a runtime service.

        Args:
            name:
                Unique service name.

            service:
                Service instance.

            replace:
                Allow replacement of an existing service.

        Returns:
            The registered service.

        Raises:
            HyperKitRuntimeError:
                If the name is invalid or already registered.
        """

        normalized_name = self._normalize_name(name)

        if normalized_name in self.services and not replace:
            raise HyperKitRuntimeError(
                f"HyperKit service '{normalized_name}' "
                "is already registered."
            )

        self.services[normalized_name] = service

        return service

    def get_service(
        self,
        name: str,
        default: Optional[object] = None,
    ) -> Optional[object]:
        """Return a registered runtime service."""

        normalized_name = self._normalize_name(name)

        return self.services.get(
            normalized_name,
            default,
        )

    def has_service(self, name: str) -> bool:
        """Return whether a runtime service is registered."""

        normalized_name = self._normalize_name(name)

        return normalized_name in self.services

    def unregister_service(
        self,
        name: str,
    ) -> Optional[object]:
        """Remove and return a registered service."""

        normalized_name = self._normalize_name(name)

        return self.services.pop(
            normalized_name,
            None,
        )

    def set_metadata(
        self,
        key: str,
        value: object,
    ) -> object:
        """Set a runtime metadata value."""

        normalized_key = self._normalize_name(key)

        self.metadata[normalized_key] = value

        return value

    def get_metadata(
        self,
        key: str,
        default: Optional[object] = None,
    ) -> Optional[object]:
        """Return a runtime metadata value."""

        normalized_key = self._normalize_name(key)

        return self.metadata.get(
            normalized_key,
            default,
        )

    def remove_metadata(
        self,
        key: str,
    ) -> Optional[object]:
        """Remove and return a metadata value."""

        normalized_key = self._normalize_name(key)

        return self.metadata.pop(
            normalized_key,
            None,
        )

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Validate and normalize service or metadata names."""

        if not isinstance(name, str):
            raise HyperKitRuntimeError(
                "Runtime names must be strings."
            )

        normalized = name.strip()

        if not normalized:
            raise HyperKitRuntimeError(
                "Runtime names cannot be empty."
            )

        return normalized


_default_context: Optional[SDKContext] = None


def create_context(
    config: Optional[SDKConfig] = None,
) -> SDKContext:
    """Create an independent HyperKit SDK context."""

    if config is None:
        config = SDKConfig()

    if not isinstance(config, SDKConfig):
        raise HyperKitRuntimeError(
            "config must be an SDKConfig instance."
        )

    return SDKContext(config=config)


def get_default_context() -> SDKContext:
    """Return the process-wide default HyperKit context.

    The context is created lazily on first access.
    """

    global _default_context

    if _default_context is None:
        _default_context = create_context()

    return _default_context


def set_default_context(
    context: SDKContext,
) -> SDKContext:
    """Replace the process-wide default context."""

    global _default_context

    if not isinstance(context, SDKContext):
        raise HyperKitRuntimeError(
            "Default context must be an SDKContext instance."
        )

    _default_context = context

    return context


def reset_default_context() -> None:
    """Discard the current process-wide default context."""

    global _default_context

    _default_context = None
