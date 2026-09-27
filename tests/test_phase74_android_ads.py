import pytest

from hyperkit.ads import (
    AdConfig,
    AdStatus,
    AdType,
    AdsService,
)
from hyperkit.ads.android import (
    AndroidAdBuildRequirements,
    AndroidAdProvider,
    DEFAULT_ANDROID_AD_PERMISSIONS,
    MockAndroidAdBridge,
)


def test_android_ad_build_requirements_have_network_permissions():
    requirements = (
        AndroidAdBuildRequirements()
    )

    assert (
        requirements.permissions
        == DEFAULT_ANDROID_AD_PERMISSIONS
    )

    assert (
        requirements.permissions
        == (
            "INTERNET",
            "ACCESS_NETWORK_STATE",
        )
    )


def test_android_provider_initializes_bridge():
    bridge = MockAndroidAdBridge()
    provider = AndroidAdProvider(
        bridge
    )

    result = provider.initialize()

    assert result.success
    assert result.status == AdStatus.READY
    assert provider.initialized
    assert provider.bridge_name == "mock-android"


def test_android_provider_resolves_logical_placement_ids():
    bridge = MockAndroidAdBridge()

    provider = AndroidAdProvider(
        bridge,
        AdConfig(
            placements={
                "game_over": (
                    "provider-interstitial-1"
                ),
            }
        ),
    )

    provider.initialize()

    result = (
        provider
        .show_interstitial(
            "game_over"
        )
    )

    assert result.success
    assert (
        result.placement
        == "provider-interstitial-1"
    )

    assert (
        bridge.history[-1]
        == (
            "show_interstitial",
            AdType.INTERSTITIAL,
            "provider-interstitial-1",
        )
    )


def test_android_provider_can_require_mapped_placements():
    provider = AndroidAdProvider(
        MockAndroidAdBridge(),
        AdConfig(),
        require_mapped_placements=True,
    )

    provider.initialize()

    with pytest.raises(
        ValueError,
        match="is not mapped",
    ):
        provider.show_interstitial(
            "game_over"
        )


def test_android_rewarded_callback_only_runs_when_reward_granted():
    rewarded = []

    provider = AndroidAdProvider(
        MockAndroidAdBridge(
            grant_reward=True
        )
    )

    provider.initialize()

    result = provider.show_rewarded(
        "revive",
        on_reward=lambda: (
            rewarded.append("revive")
        ),
    )

    assert result.success
    assert result.reward_granted
    assert rewarded == [
        "revive"
    ]


def test_android_rewarded_callback_does_not_run_without_reward():
    rewarded = []

    provider = AndroidAdProvider(
        MockAndroidAdBridge(
            grant_reward=False
        )
    )

    provider.initialize()

    result = provider.show_rewarded(
        "revive",
        on_reward=lambda: (
            rewarded.append("revive")
        ),
    )

    assert result.success
    assert not result.reward_granted
    assert rewarded == []


def test_android_provider_is_safe_before_initialize():
    provider = AndroidAdProvider(
        MockAndroidAdBridge()
    )

    assert not provider.is_available(
        AdType.INTERSTITIAL,
        "game_over",
    )

    result = (
        provider
        .show_interstitial(
            "game_over"
        )
    )

    assert not result.success
    assert result.status == AdStatus.UNAVAILABLE


def test_ads_service_can_use_android_provider_without_android_sdk():
    bridge = MockAndroidAdBridge()

    ads = AdsService(
        AndroidAdProvider(
            bridge,
            AdConfig(
                placements={
                    "revive": (
                        "provider-rewarded-1"
                    ),
                }
            ),
        )
    )

    rewards = []

    result = ads.show_rewarded(
        "revive",
        on_reward=lambda: (
            rewards.append(1)
        ),
    )

    assert result.success
    assert result.reward_granted
    assert rewards == [1]

    assert (
        result.placement
        == "provider-rewarded-1"
    )


def test_android_provider_exposes_bridge_build_requirements():
    requirements = (
        AndroidAdBuildRequirements(
            permissions=(
                "INTERNET",
            ),
            python_requirements=(
                "provider-python-package",
            ),
            gradle_dependencies=(
                "com.example:ads:1.0.0",
            ),
            manifest_placeholders={
                "APP_ID": "demo",
            },
        )
    )

    provider = AndroidAdProvider(
        MockAndroidAdBridge(
            build_requirements=(
                requirements
            )
        )
    )

    assert (
        provider.build_requirements
        == requirements
    )
