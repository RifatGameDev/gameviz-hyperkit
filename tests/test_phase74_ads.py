from hyperkit.ads import (
    AdConfig,
    AdStatus,
    AdType,
    MockAdProvider,
    NoOpAdProvider,
)


def test_ad_config_resolves_placement():
    config = AdConfig(
        placements={
            "game_over": "provider-slot-1",
        }
    )

    assert (
        config.placement_id("game_over")
        == "provider-slot-1"
    )

    assert config.placement_id("missing") is None


def test_noop_ads_never_require_mobile_dependencies():
    provider = NoOpAdProvider()

    initialized = provider.initialize()

    assert initialized.success
    assert initialized.status == AdStatus.UNAVAILABLE

    result = provider.show_interstitial("game_over")

    assert not result.success
    assert result.status == AdStatus.UNAVAILABLE
    assert result.ad_type == AdType.INTERSTITIAL


def test_mock_ads_initialize_and_show_interstitial():
    provider = MockAdProvider()

    init_result = provider.initialize()

    assert init_result.success
    assert init_result.status == AdStatus.READY

    result = provider.show_interstitial("game_over")

    assert result.success
    assert result.completed
    assert result.ad_type == AdType.INTERSTITIAL
    assert result.placement == "game_over"


def test_mock_rewarded_ad_grants_reward_callback():
    provider = MockAdProvider()
    provider.initialize()

    rewards = []

    result = provider.show_rewarded(
        "double_coins",
        on_reward=lambda: rewards.append(100),
    )

    assert result.success
    assert result.reward_granted
    assert rewards == [100]


def test_disabled_mock_provider_is_unavailable():
    provider = MockAdProvider(
        AdConfig(enabled=False)
    )

    result = provider.initialize()

    assert result.status == AdStatus.UNAVAILABLE
    assert not provider.is_available(AdType.REWARDED)

    rewarded = provider.show_rewarded("revive")

    assert not rewarded.success
    assert not rewarded.reward_granted
