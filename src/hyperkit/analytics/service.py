"""Developer-facing analytics service for GameViz HyperKit."""

from __future__ import annotations

from typing import Any

from ..errors import HyperKitRuntimeError
from ..runtime import SDKContext
from . import (
    AnalyticsEvent,
    AnalyticsProvider,
    AnalyticsResult,
    NoOpAnalyticsProvider,
)


class AnalyticsService:
    """High-level, provider-independent analytics API."""

    SERVICE_NAME = "analytics"

    def __init__(
        self,
        provider: (
            AnalyticsProvider
            | None
        ) = None,
        *,
        auto_initialize: bool = True,
    ) -> None:
        self.provider = (
            provider
            if provider is not None
            else NoOpAnalyticsProvider()
        )
        self.auto_initialize = bool(
            auto_initialize
        )
        self._initialized = False
        self._last_initialize_result: (
            AnalyticsResult | None
        ) = None

    @property
    def provider_name(
        self,
    ) -> str:
        return self.provider.provider_name

    @property
    def initialized(
        self,
    ) -> bool:
        return self._initialized

    @property
    def last_initialize_result(
        self,
    ) -> AnalyticsResult | None:
        return self._last_initialize_result

    def initialize(
        self,
    ) -> AnalyticsResult:
        result = self.provider.initialize()

        self._initialized = True
        self._last_initialize_result = result

        return result

    def set_provider(
        self,
        provider: AnalyticsProvider,
        *,
        initialize: bool = False,
    ) -> "AnalyticsService":
        if not isinstance(
            provider,
            AnalyticsProvider,
        ):
            raise TypeError(
                "provider must be an "
                "AnalyticsProvider instance."
            )

        self.provider = provider
        self._initialized = False
        self._last_initialize_result = None

        if initialize:
            self.initialize()

        return self

    def attach(
        self,
        context: SDKContext,
        *,
        replace: bool = False,
    ) -> "AnalyticsService":
        if not isinstance(
            context,
            SDKContext,
        ):
            raise HyperKitRuntimeError(
                "context must be an "
                "SDKContext instance."
            )

        context.register_service(
            self.SERVICE_NAME,
            self,
            replace=replace,
        )

        return self

    def _ensure_initialized(
        self,
    ) -> None:
        if self._initialized:
            return

        if not self.auto_initialize:
            raise HyperKitRuntimeError(
                "AnalyticsService is not "
                "initialized. Call "
                "initialize() first."
            )

        self.initialize()

    def track(
        self,
        name: str,
        **properties: Any,
    ) -> AnalyticsResult:
        self._ensure_initialized()

        return self.provider.track_event(
            AnalyticsEvent(
                name=name,
                properties=properties,
            )
        )

    def flush(
        self,
    ) -> AnalyticsResult:
        self._ensure_initialized()

        return self.provider.flush()

    def game_start(
        self,
        **properties: Any,
    ) -> AnalyticsResult:
        return self.track(
            "game_start",
            **properties,
        )

    def game_over(
        self,
        *,
        score: int | None = None,
        high_score: int | None = None,
        reason: str | None = None,
        **properties: Any,
    ) -> AnalyticsResult:
        payload = dict(properties)

        if score is not None:
            payload["score"] = int(score)

        if high_score is not None:
            payload[
                "high_score"
            ] = int(high_score)

        if reason is not None:
            payload["reason"] = str(
                reason
            )

        return self.track(
            "game_over",
            **payload,
        )

    def level_start(
        self,
        level: int,
        **properties: Any,
    ) -> AnalyticsResult:
        return self.track(
            "level_start",
            level=int(level),
            **properties,
        )

    def level_complete(
        self,
        level: int,
        *,
        score: int | None = None,
        duration: float | None = None,
        **properties: Any,
    ) -> AnalyticsResult:
        payload = dict(properties)
        payload["level"] = int(level)

        if score is not None:
            payload["score"] = int(score)

        if duration is not None:
            payload[
                "duration"
            ] = float(duration)

        return self.track(
            "level_complete",
            **payload,
        )

    def score(
        self,
        score: int,
        *,
        high_score: int | None = None,
        **properties: Any,
    ) -> AnalyticsResult:
        payload = dict(properties)
        payload["score"] = int(score)

        if high_score is not None:
            payload[
                "high_score"
            ] = int(high_score)

        return self.track(
            "score_recorded",
            **payload,
        )

    def progression(
        self,
        *,
        level: int,
        xp: int,
        coins: int,
        **properties: Any,
    ) -> AnalyticsResult:
        return self.track(
            "progression_updated",
            level=int(level),
            xp=int(xp),
            coins=int(coins),
            **properties,
        )


__all__ = [
    "AnalyticsService",
]
