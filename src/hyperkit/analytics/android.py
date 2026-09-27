"""Android analytics bridge architecture for GameViz HyperKit."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from . import (
    AnalyticsEvent,
    AnalyticsProvider,
    AnalyticsResult,
)


DEFAULT_ANDROID_ANALYTICS_PERMISSIONS = (
    "INTERNET",
    "ACCESS_NETWORK_STATE",
)


@dataclass(frozen=True)
class AndroidAnalyticsBuildRequirements:
    """Android build requirements declared by an analytics bridge."""

    permissions: tuple[str, ...] = (
        DEFAULT_ANDROID_ANALYTICS_PERMISSIONS
    )
    python_requirements: tuple[str, ...] = ()
    gradle_dependencies: tuple[str, ...] = ()
    java_source_dirs: tuple[str, ...] = ()
    enable_androidx: bool = False


class AndroidAnalyticsBridge(ABC):
    """Platform bridge used by Android analytics providers."""

    bridge_name = "android-analytics-base"

    @property
    def build_requirements(
        self,
    ) -> AndroidAnalyticsBuildRequirements:
        return AndroidAnalyticsBuildRequirements()

    @abstractmethod
    def initialize(
        self,
    ) -> AnalyticsResult:
        """Initialize the native analytics layer."""

    @abstractmethod
    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        """Send one event to the native analytics layer."""

    @abstractmethod
    def flush(
        self,
    ) -> AnalyticsResult:
        """Flush pending analytics events when supported."""


class AndroidAnalyticsProvider(
    AnalyticsProvider
):
    """Adapt an Android analytics bridge to the HyperKit provider API."""

    provider_name = "android-analytics"

    def __init__(
        self,
        bridge: AndroidAnalyticsBridge,
    ) -> None:
        if not isinstance(
            bridge,
            AndroidAnalyticsBridge,
        ):
            raise TypeError(
                "bridge must be an "
                "AndroidAnalyticsBridge instance."
            )

        super().__init__()

        self.bridge = bridge
        self.last_initialize_result: (
            AnalyticsResult | None
        ) = None

    @property
    def bridge_name(
        self,
    ) -> str:
        return self.bridge.bridge_name

    @property
    def build_requirements(
        self,
    ) -> AndroidAnalyticsBuildRequirements:
        return self.bridge.build_requirements

    def initialize(
        self,
    ) -> AnalyticsResult:
        result = (
            self.bridge
            .initialize()
        )

        self.last_initialize_result = result
        self.initialized = bool(
            result.success
        )

        return result

    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        if not self.initialized:
            return AnalyticsResult(
                success=False,
                message=(
                    "Android analytics provider "
                    "is not initialized."
                ),
            )

        return (
            self.bridge
            .track_event(
                event
            )
        )

    def flush(
        self,
    ) -> AnalyticsResult:
        if not self.initialized:
            return AnalyticsResult(
                success=False,
                message=(
                    "Android analytics provider "
                    "is not initialized."
                ),
            )

        return self.bridge.flush()


class MockAndroidAnalyticsBridge(
    AndroidAnalyticsBridge
):
    """Deterministic bridge for desktop development and tests."""

    bridge_name = "mock-android-analytics"

    def __init__(
        self,
        *,
        available: bool = True,
        build_requirements: (
            AndroidAnalyticsBuildRequirements
            | None
        ) = None,
    ) -> None:
        self.available = bool(
            available
        )
        self.initialized = False
        self.events: list[
            AnalyticsEvent
        ] = []
        self.flush_count = 0
        self._build_requirements = (
            build_requirements
            or AndroidAnalyticsBuildRequirements()
        )

    @property
    def build_requirements(
        self,
    ) -> AndroidAnalyticsBuildRequirements:
        return self._build_requirements

    def initialize(
        self,
    ) -> AnalyticsResult:
        self.initialized = True

        if not self.available:
            return AnalyticsResult(
                success=False,
                message=(
                    "Mock Android analytics "
                    "bridge is unavailable."
                ),
            )

        return AnalyticsResult(
            success=True,
            message=(
                "Mock Android analytics "
                "bridge initialized."
            ),
        )

    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        if (
            not self.initialized
            or not self.available
        ):
            return AnalyticsResult(
                success=False,
                message=(
                    "Mock Android analytics "
                    "bridge is unavailable."
                ),
            )

        self.events.append(
            event
        )

        return AnalyticsResult(
            success=True
        )

    def flush(
        self,
    ) -> AnalyticsResult:
        if (
            not self.initialized
            or not self.available
        ):
            return AnalyticsResult(
                success=False,
                message=(
                    "Mock Android analytics "
                    "bridge is unavailable."
                ),
            )

        self.flush_count += 1

        return AnalyticsResult(
            success=True
        )


__all__ = [
    "AndroidAnalyticsBridge",
    "AndroidAnalyticsBuildRequirements",
    "AndroidAnalyticsProvider",
    "DEFAULT_ANDROID_ANALYTICS_PERMISSIONS",
    "MockAndroidAnalyticsBridge",
]
