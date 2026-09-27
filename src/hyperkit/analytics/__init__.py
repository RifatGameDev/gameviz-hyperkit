"""Provider-independent analytics foundation for GameViz HyperKit."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from time import time
from typing import Any


@dataclass(frozen=True)
class AnalyticsEvent:
    """Portable analytics event."""

    name: str
    properties: Mapping[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)

    def __post_init__(self) -> None:
        normalized = self.name.strip()
        if not normalized:
            raise ValueError("analytics event name cannot be empty.")
        object.__setattr__(self, "name", normalized)


@dataclass(frozen=True)
class AnalyticsResult:
    """Result from an analytics provider operation."""

    success: bool
    message: str = ""


class AnalyticsProvider(ABC):
    """Interface implemented by concrete analytics providers."""

    provider_name = "base"

    def __init__(self) -> None:
        self.initialized = False

    @abstractmethod
    def initialize(self) -> AnalyticsResult:
        """Initialize the provider."""

    @abstractmethod
    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        """Track one event."""

    @abstractmethod
    def flush(self) -> AnalyticsResult:
        """Flush pending events if the provider buffers them."""


class NoOpAnalyticsProvider(AnalyticsProvider):
    """Safe provider used when analytics is disabled."""

    provider_name = "noop"

    def initialize(self) -> AnalyticsResult:
        self.initialized = True
        return AnalyticsResult(success=True)

    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        return AnalyticsResult(success=True)

    def flush(self) -> AnalyticsResult:
        return AnalyticsResult(success=True)


class MockAnalyticsProvider(AnalyticsProvider):
    """In-memory analytics provider for tests and desktop development."""

    provider_name = "mock"

    def __init__(self) -> None:
        super().__init__()
        self.events: list[AnalyticsEvent] = []
        self.flush_count = 0

    def initialize(self) -> AnalyticsResult:
        self.initialized = True
        return AnalyticsResult(success=True)

    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        if not self.initialized:
            return AnalyticsResult(
                success=False,
                message="Analytics provider is not initialized.",
            )

        self.events.append(event)
        return AnalyticsResult(success=True)

    def track(
        self,
        name: str,
        **properties: Any,
    ) -> AnalyticsResult:
        return self.track_event(
            AnalyticsEvent(
                name=name,
                properties=properties,
            )
        )

    def flush(self) -> AnalyticsResult:
        if not self.initialized:
            return AnalyticsResult(
                success=False,
                message="Analytics provider is not initialized.",
            )

        self.flush_count += 1
        return AnalyticsResult(success=True)


from .service import AnalyticsService
from .android import (
    AndroidAnalyticsBridge,
    AndroidAnalyticsBuildRequirements,
    AndroidAnalyticsProvider,
    DEFAULT_ANDROID_ANALYTICS_PERMISSIONS,
    MockAndroidAnalyticsBridge,
)
from .firebase import (
    FIREBASE_ANALYTICS_DEPENDENCY,
    FIREBASE_ANALYTICS_JAVA_SOURCE,
    FirebaseAnalyticsAndroidBridge,
    FirebaseAnalyticsAndroidProvider,
    FirebaseAnalyticsConfig,
    configure_firebase_analytics_android_project,
    load_firebase_analytics_config,
)


__all__ = [
    "AnalyticsEvent",
    "AnalyticsProvider",
    "AnalyticsResult",
    "AnalyticsService",
    "AndroidAnalyticsBridge",
    "AndroidAnalyticsBuildRequirements",
    "AndroidAnalyticsProvider",
    "DEFAULT_ANDROID_ANALYTICS_PERMISSIONS",
    "MockAndroidAnalyticsBridge",
    "FIREBASE_ANALYTICS_DEPENDENCY",
    "FIREBASE_ANALYTICS_JAVA_SOURCE",
    "FirebaseAnalyticsAndroidBridge",
    "FirebaseAnalyticsAndroidProvider",
    "FirebaseAnalyticsConfig",
    "configure_firebase_analytics_android_project",
    "load_firebase_analytics_config",
    "MockAnalyticsProvider",
    "NoOpAnalyticsProvider",
]
