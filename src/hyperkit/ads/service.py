"""Developer-facing advertising service for GameViz HyperKit."""

from __future__ import annotations

from collections.abc import Callable

from ..errors import HyperKitRuntimeError
from ..runtime import SDKContext
from . import (
    AdProvider,
    AdResult,
    AdType,
    NoOpAdProvider,
)


class AdsService:
    """High-level, provider-independent advertising API.

    The service keeps game code independent from AdMob, Unity, or any
    future network integration. A safe no-op provider is used by default.
    """

    SERVICE_NAME = "ads"

    def __init__(
        self,
        provider: AdProvider | None = None,
        *,
        auto_initialize: bool = True,
    ) -> None:
        self.provider = (
            provider
            if provider is not None
            else NoOpAdProvider()
        )
        self.auto_initialize = bool(
            auto_initialize
        )
        self._initialized = False
        self._last_initialize_result: (
            AdResult | None
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
    ) -> AdResult | None:
        return self._last_initialize_result

    def initialize(
        self,
    ) -> AdResult:
        result = self.provider.initialize()

        self._initialized = True
        self._last_initialize_result = result

        return result

    def set_provider(
        self,
        provider: AdProvider,
        *,
        initialize: bool = False,
    ) -> "AdsService":
        if not isinstance(
            provider,
            AdProvider,
        ):
            raise TypeError(
                "provider must be an "
                "AdProvider instance."
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
    ) -> "AdsService":
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
                "AdsService is not initialized. "
                "Call initialize() first."
            )

        self.initialize()

    @staticmethod
    def _normalize_ad_type(
        ad_type: AdType | str,
    ) -> AdType:
        if isinstance(
            ad_type,
            AdType,
        ):
            return ad_type

        try:
            return AdType(
                str(ad_type).strip().lower()
            )
        except ValueError as exc:
            allowed = ", ".join(
                item.value
                for item in AdType
            )

            raise ValueError(
                f"Unsupported ad type "
                f"'{ad_type}'. "
                f"Expected one of: "
                f"{allowed}."
            ) from exc

    def is_available(
        self,
        ad_type: AdType | str,
        placement: str | None = None,
    ) -> bool:
        self._ensure_initialized()

        return self.provider.is_available(
            self._normalize_ad_type(
                ad_type
            ),
            placement,
        )

    def show_banner(
        self,
        placement: str | None = None,
    ) -> AdResult:
        self._ensure_initialized()

        return self.provider.show_banner(
            placement
        )

    def hide_banner(
        self,
        placement: str | None = None,
    ) -> AdResult:
        self._ensure_initialized()

        return self.provider.hide_banner(
            placement
        )

    def show_interstitial(
        self,
        placement: str | None = None,
    ) -> AdResult:
        self._ensure_initialized()

        return (
            self.provider
            .show_interstitial(
                placement
            )
        )

    def show_rewarded(
        self,
        placement: str | None = None,
        *,
        on_reward: (
            Callable[[], None]
            | None
        ) = None,
    ) -> AdResult:
        self._ensure_initialized()

        return self.provider.show_rewarded(
            placement,
            on_reward=on_reward,
        )


__all__ = [
    "AdsService",
]
