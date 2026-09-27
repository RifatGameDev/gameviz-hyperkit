import pytest

from hyperkit.ads import (
    AdStatus,
    AdType,
    AdsService,
    MockAdProvider,
    NoOpAdProvider,
)
from hyperkit.errors import HyperKitRuntimeError
from hyperkit.runtime import create_context


def test_ads_service_defaults_to_noop_provider():
    ads = AdsService()

    result = ads.show_interstitial(
        "game_over"
    )

    assert ads.initialized
    assert ads.provider_name == "noop"
    assert not result.success
    assert result.status == AdStatus.UNAVAILABLE


def test_ads_service_wraps_mock_provider():
    provider = MockAdProvider()
    ads = AdsService(provider)

    assert ads.is_available(
        "rewarded",
        "revive",
    )

    result = ads.show_interstitial(
        "game_over"
    )

    assert result.success
    assert result.completed


def test_ads_service_rewarded_flow_calls_reward_once():
    ads = AdsService(
        MockAdProvider()
    )

    rewards = []

    result = ads.show_rewarded(
        "double_coins",
        on_reward=lambda: rewards.append(100),
    )

    assert result.success
    assert result.reward_granted
    assert rewards == [100]


def test_ads_service_can_switch_provider():
    ads = AdsService(
        NoOpAdProvider()
    )

    ads.initialize()

    ads.set_provider(
        MockAdProvider(),
        initialize=True,
    )

    assert ads.provider_name == "mock"
    assert ads.initialized
    assert ads.is_available(
        AdType.INTERSTITIAL
    )


def test_ads_service_requires_explicit_initialize_when_disabled():
    ads = AdsService(
        MockAdProvider(),
        auto_initialize=False,
    )

    with pytest.raises(
        HyperKitRuntimeError,
        match="not initialized",
    ):
        ads.show_banner("menu")


def test_ads_service_attaches_to_context():
    context = create_context()
    ads = AdsService()

    ads.attach(context)

    assert context.get_service(
        "ads"
    ) is ads


def test_ads_service_rejects_unknown_ad_type():
    ads = AdsService(
        MockAdProvider()
    )

    with pytest.raises(
        ValueError,
        match="Unsupported ad type",
    ):
        ads.is_available(
            "popup"
        )
