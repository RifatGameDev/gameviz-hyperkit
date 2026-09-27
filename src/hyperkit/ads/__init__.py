"""Provider-independent advertising foundation for GameViz HyperKit.

The core SDK never depends on a concrete ad network. Games can develop
against this small interface and swap providers later.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AdType(str, Enum):
    """Supported advertising formats."""

    BANNER = "banner"
    INTERSTITIAL = "interstitial"
    REWARDED = "rewarded"


class AdStatus(str, Enum):
    """Portable result states shared by all ad providers."""

    UNAVAILABLE = "unavailable"
    READY = "ready"
    SHOWING = "showing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class AdConfig:
    """Provider-neutral advertising configuration."""

    enabled: bool = True
    test_mode: bool = True
    placements: Mapping[str, str] = field(default_factory=dict)
    provider_options: Mapping[str, Any] = field(default_factory=dict)

    def placement_id(self, name: str) -> str | None:
        """Return a configured provider placement identifier."""

        normalized = str(name).strip()
        if not normalized:
            raise ValueError("placement name cannot be empty.")

        value = self.placements.get(normalized)
        if value is None:
            return None

        resolved = str(value).strip()
        return resolved or None


@dataclass(frozen=True)
class AdResult:
    """Result returned by provider operations."""

    success: bool
    status: AdStatus
    ad_type: AdType | None = None
    placement: str | None = None
    reward_granted: bool = False
    message: str = ""

    @property
    def completed(self) -> bool:
        return self.status == AdStatus.COMPLETED


class AdProvider(ABC):
    """Interface implemented by concrete advertising providers."""

    provider_name = "base"

    def __init__(self, config: AdConfig | None = None) -> None:
        self.config = config or AdConfig()
        self.initialized = False

    @abstractmethod
    def initialize(self) -> AdResult:
        """Initialize the provider."""

    @abstractmethod
    def is_available(
        self,
        ad_type: AdType,
        placement: str | None = None,
    ) -> bool:
        """Return whether an ad can currently be shown."""

    @abstractmethod
    def show_banner(self, placement: str | None = None) -> AdResult:
        """Show a banner ad."""

    @abstractmethod
    def hide_banner(self, placement: str | None = None) -> AdResult:
        """Hide a banner ad."""

    @abstractmethod
    def show_interstitial(self, placement: str | None = None) -> AdResult:
        """Show an interstitial ad."""

    @abstractmethod
    def show_rewarded(
        self,
        placement: str | None = None,
        *,
        on_reward: Callable[[], None] | None = None,
    ) -> AdResult:
        """Show a rewarded ad and invoke the reward callback on success."""


class NoOpAdProvider(AdProvider):
    """Safe provider used when advertising is not configured."""

    provider_name = "noop"

    def initialize(self) -> AdResult:
        self.initialized = True
        return AdResult(
            success=True,
            status=AdStatus.UNAVAILABLE,
            message="Advertising is disabled or no provider is configured.",
        )

    def is_available(
        self,
        ad_type: AdType,
        placement: str | None = None,
    ) -> bool:
        return False

    def _unavailable(
        self,
        ad_type: AdType,
        placement: str | None,
    ) -> AdResult:
        return AdResult(
            success=False,
            status=AdStatus.UNAVAILABLE,
            ad_type=ad_type,
            placement=placement,
            message="No advertising provider is configured.",
        )

    def show_banner(self, placement: str | None = None) -> AdResult:
        return self._unavailable(AdType.BANNER, placement)

    def hide_banner(self, placement: str | None = None) -> AdResult:
        return self._unavailable(AdType.BANNER, placement)

    def show_interstitial(self, placement: str | None = None) -> AdResult:
        return self._unavailable(AdType.INTERSTITIAL, placement)

    def show_rewarded(
        self,
        placement: str | None = None,
        *,
        on_reward: Callable[[], None] | None = None,
    ) -> AdResult:
        return self._unavailable(AdType.REWARDED, placement)


class MockAdProvider(AdProvider):
    """Deterministic provider for desktop development and tests."""

    provider_name = "mock"

    def __init__(
        self,
        config: AdConfig | None = None,
        *,
        available: bool = True,
    ) -> None:
        super().__init__(config)
        self.available = bool(available)
        self.history: list[AdResult] = []

    def _record(self, result: AdResult) -> AdResult:
        self.history.append(result)
        return result

    def initialize(self) -> AdResult:
        self.initialized = True

        status = (
            AdStatus.READY
            if self.config.enabled and self.available
            else AdStatus.UNAVAILABLE
        )

        return self._record(
            AdResult(
                success=True,
                status=status,
                message="Mock advertising provider initialized.",
            )
        )

    def is_available(
        self,
        ad_type: AdType,
        placement: str | None = None,
    ) -> bool:
        return (
            self.initialized
            and self.config.enabled
            and self.available
        )

    def _show(
        self,
        ad_type: AdType,
        placement: str | None,
        *,
        reward_granted: bool = False,
    ) -> AdResult:
        if not self.is_available(ad_type, placement):
            return self._record(
                AdResult(
                    success=False,
                    status=AdStatus.UNAVAILABLE,
                    ad_type=ad_type,
                    placement=placement,
                    message="Mock ad is not available.",
                )
            )

        return self._record(
            AdResult(
                success=True,
                status=AdStatus.COMPLETED,
                ad_type=ad_type,
                placement=placement,
                reward_granted=reward_granted,
            )
        )

    def show_banner(self, placement: str | None = None) -> AdResult:
        if not self.is_available(AdType.BANNER, placement):
            return self._show(AdType.BANNER, placement)

        return self._record(
            AdResult(
                success=True,
                status=AdStatus.SHOWING,
                ad_type=AdType.BANNER,
                placement=placement,
            )
        )

    def hide_banner(self, placement: str | None = None) -> AdResult:
        if not self.initialized:
            return self._record(
                AdResult(
                    success=False,
                    status=AdStatus.UNAVAILABLE,
                    ad_type=AdType.BANNER,
                    placement=placement,
                    message="Mock advertising provider is not initialized.",
                )
            )

        return self._record(
            AdResult(
                success=True,
                status=AdStatus.COMPLETED,
                ad_type=AdType.BANNER,
                placement=placement,
            )
        )

    def show_interstitial(self, placement: str | None = None) -> AdResult:
        return self._show(AdType.INTERSTITIAL, placement)

    def show_rewarded(
        self,
        placement: str | None = None,
        *,
        on_reward: Callable[[], None] | None = None,
    ) -> AdResult:
        result = self._show(
            AdType.REWARDED,
            placement,
            reward_granted=True,
        )

        if result.success and result.reward_granted and on_reward is not None:
            on_reward()

        return result


from .service import AdsService
from .android import (
    AndroidAdBridge,
    AndroidAdBuildRequirements,
    AndroidAdProvider,
    DEFAULT_ANDROID_AD_PERMISSIONS,
    MockAndroidAdBridge,
)


__all__ = [
    "AdConfig",
    "AdProvider",
    "AdResult",
    "AdStatus",
    "AdType",
    "AdsService",
    "AndroidAdBridge",
    "AndroidAdBuildRequirements",
    "AndroidAdProvider",
    "DEFAULT_ANDROID_AD_PERMISSIONS",
    "MockAndroidAdBridge",
    "MockAdProvider",
    "NoOpAdProvider",
]
