"""Android advertising bridge architecture for GameViz HyperKit.

This module intentionally contains no dependency on AdMob, Unity, Java,
PyJNIus, or another network SDK. Concrete Android integrations implement
AndroidAdBridge and can be injected into AndroidAdProvider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field

from . import (
    AdConfig,
    AdProvider,
    AdResult,
    AdStatus,
    AdType,
)


DEFAULT_ANDROID_AD_PERMISSIONS = (
    "INTERNET",
    "ACCESS_NETWORK_STATE",
)


@dataclass(frozen=True)
class AndroidAdBuildRequirements:
    """Android build requirements declared by an ad bridge."""

    permissions: tuple[str, ...] = (
        DEFAULT_ANDROID_AD_PERMISSIONS
    )
    python_requirements: tuple[str, ...] = ()
    gradle_dependencies: tuple[str, ...] = ()
    manifest_placeholders: Mapping[
        str,
        str,
    ] = field(
        default_factory=dict
    )


class AndroidAdBridge(ABC):
    """Platform bridge used by Android advertising providers."""

    bridge_name = "android-base"

    @property
    def build_requirements(
        self,
    ) -> AndroidAdBuildRequirements:
        return AndroidAdBuildRequirements()

    @abstractmethod
    def initialize(
        self,
        config: AdConfig,
    ) -> AdResult:
        """Initialize the Android/native advertising layer."""

    @abstractmethod
    def is_available(
        self,
        ad_type: AdType,
        placement_id: str | None,
    ) -> bool:
        """Return whether an Android ad can currently be shown."""

    @abstractmethod
    def show_banner(
        self,
        placement_id: str | None,
    ) -> AdResult:
        """Show a banner through the native bridge."""

    @abstractmethod
    def hide_banner(
        self,
        placement_id: str | None,
    ) -> AdResult:
        """Hide a banner through the native bridge."""

    @abstractmethod
    def show_interstitial(
        self,
        placement_id: str | None,
    ) -> AdResult:
        """Show an interstitial through the native bridge."""

    @abstractmethod
    def show_rewarded(
        self,
        placement_id: str | None,
    ) -> AdResult:
        """Show a rewarded ad through the native bridge."""


class AndroidAdProvider(AdProvider):
    """Provider that adapts an AndroidAdBridge to HyperKit ads."""

    provider_name = "android"

    def __init__(
        self,
        bridge: AndroidAdBridge,
        config: AdConfig | None = None,
        *,
        require_mapped_placements: bool = False,
    ) -> None:
        if not isinstance(
            bridge,
            AndroidAdBridge,
        ):
            raise TypeError(
                "bridge must be an "
                "AndroidAdBridge instance."
            )

        super().__init__(
            config
        )

        self.bridge = bridge
        self.require_mapped_placements = bool(
            require_mapped_placements
        )
        self.last_initialize_result: (
            AdResult | None
        ) = None

    @property
    def bridge_name(
        self,
    ) -> str:
        return self.bridge.bridge_name

    @property
    def build_requirements(
        self,
    ) -> AndroidAdBuildRequirements:
        return self.bridge.build_requirements

    def _resolve_placement(
        self,
        placement: str | None,
    ) -> str | None:
        if placement is None:
            return None

        logical_name = str(
            placement
        ).strip()

        if not logical_name:
            return None

        mapped = self.config.placement_id(
            logical_name
        )

        if mapped is not None:
            return mapped

        if self.require_mapped_placements:
            raise ValueError(
                "Android ad placement "
                f"'{logical_name}' is not mapped "
                "in AdConfig.placements."
            )

        return logical_name

    @staticmethod
    def _not_initialized(
        ad_type: AdType | None = None,
        placement: str | None = None,
    ) -> AdResult:
        return AdResult(
            success=False,
            status=AdStatus.UNAVAILABLE,
            ad_type=ad_type,
            placement=placement,
            message=(
                "Android advertising provider "
                "is not initialized."
            ),
        )

    def initialize(
        self,
    ) -> AdResult:
        result = self.bridge.initialize(
            self.config
        )

        self.last_initialize_result = result
        self.initialized = bool(
            result.success
        )

        return result

    def is_available(
        self,
        ad_type: AdType,
        placement: str | None = None,
    ) -> bool:
        if not self.initialized:
            return False

        return self.bridge.is_available(
            ad_type,
            self._resolve_placement(
                placement
            ),
        )

    def show_banner(
        self,
        placement: str | None = None,
    ) -> AdResult:
        resolved = self._resolve_placement(
            placement
        )

        if not self.initialized:
            return self._not_initialized(
                AdType.BANNER,
                resolved,
            )

        return self.bridge.show_banner(
            resolved
        )

    def hide_banner(
        self,
        placement: str | None = None,
    ) -> AdResult:
        resolved = self._resolve_placement(
            placement
        )

        if not self.initialized:
            return self._not_initialized(
                AdType.BANNER,
                resolved,
            )

        return self.bridge.hide_banner(
            resolved
        )

    def show_interstitial(
        self,
        placement: str | None = None,
    ) -> AdResult:
        resolved = self._resolve_placement(
            placement
        )

        if not self.initialized:
            return self._not_initialized(
                AdType.INTERSTITIAL,
                resolved,
            )

        return (
            self.bridge
            .show_interstitial(
                resolved
            )
        )

    def show_rewarded(
        self,
        placement: str | None = None,
        *,
        on_reward=None,
    ) -> AdResult:
        resolved = self._resolve_placement(
            placement
        )

        if not self.initialized:
            return self._not_initialized(
                AdType.REWARDED,
                resolved,
            )

        result = (
            self.bridge
            .show_rewarded(
                resolved
            )
        )

        if (
            result.success
            and result.reward_granted
            and on_reward is not None
        ):
            on_reward()

        return result


class MockAndroidAdBridge(
    AndroidAdBridge
):
    """Deterministic Android bridge for desktop tests and development."""

    bridge_name = "mock-android"

    def __init__(
        self,
        *,
        available: bool = True,
        grant_reward: bool = True,
        build_requirements: (
            AndroidAdBuildRequirements
            | None
        ) = None,
    ) -> None:
        self.available = bool(
            available
        )
        self.grant_reward = bool(
            grant_reward
        )
        self.initialized = False
        self.history: list[
            tuple[
                str,
                AdType | None,
                str | None,
            ]
        ] = []
        self._build_requirements = (
            build_requirements
            or AndroidAdBuildRequirements()
        )

    @property
    def build_requirements(
        self,
    ) -> AndroidAdBuildRequirements:
        return self._build_requirements

    def initialize(
        self,
        config: AdConfig,
    ) -> AdResult:
        self.initialized = True

        status = (
            AdStatus.READY
            if config.enabled
            and self.available
            else AdStatus.UNAVAILABLE
        )

        self.history.append(
            (
                "initialize",
                None,
                None,
            )
        )

        return AdResult(
            success=True,
            status=status,
            message=(
                "Mock Android advertising "
                "bridge initialized."
            ),
        )

    def is_available(
        self,
        ad_type: AdType,
        placement_id: str | None,
    ) -> bool:
        self.history.append(
            (
                "is_available",
                ad_type,
                placement_id,
            )
        )

        return (
            self.initialized
            and self.available
        )

    def _show(
        self,
        operation: str,
        ad_type: AdType,
        placement_id: str | None,
        *,
        reward_granted: bool = False,
        status: AdStatus = AdStatus.COMPLETED,
    ) -> AdResult:
        self.history.append(
            (
                operation,
                ad_type,
                placement_id,
            )
        )

        if (
            not self.initialized
            or not self.available
        ):
            return AdResult(
                success=False,
                status=AdStatus.UNAVAILABLE,
                ad_type=ad_type,
                placement=placement_id,
                message=(
                    "Mock Android ad "
                    "is not available."
                ),
            )

        return AdResult(
            success=True,
            status=status,
            ad_type=ad_type,
            placement=placement_id,
            reward_granted=(
                reward_granted
            ),
        )

    def show_banner(
        self,
        placement_id: str | None,
    ) -> AdResult:
        return self._show(
            "show_banner",
            AdType.BANNER,
            placement_id,
            status=AdStatus.SHOWING,
        )

    def hide_banner(
        self,
        placement_id: str | None,
    ) -> AdResult:
        return self._show(
            "hide_banner",
            AdType.BANNER,
            placement_id,
        )

    def show_interstitial(
        self,
        placement_id: str | None,
    ) -> AdResult:
        return self._show(
            "show_interstitial",
            AdType.INTERSTITIAL,
            placement_id,
        )

    def show_rewarded(
        self,
        placement_id: str | None,
    ) -> AdResult:
        return self._show(
            "show_rewarded",
            AdType.REWARDED,
            placement_id,
            reward_granted=(
                self.grant_reward
            ),
        )


__all__ = [
    "AndroidAdBridge",
    "AndroidAdBuildRequirements",
    "AndroidAdProvider",
    "DEFAULT_ANDROID_AD_PERMISSIONS",
    "MockAndroidAdBridge",
]
