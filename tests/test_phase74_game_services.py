from hyperkit.ads import (
    AdType,
    MockAdProvider,
)
from hyperkit.analytics import (
    MockAnalyticsProvider,
)
from hyperkit.game_systems import (
    GameSystems,
)
from hyperkit.lifecycle import (
    start_runtime,
    stop_runtime,
)
from hyperkit.runtime import (
    create_context,
)


def test_game_systems_registers_all_phase74_services():
    context = create_context()
    systems = GameSystems()

    systems.attach(context)

    assert context.get_service(
        "game_systems"
    ) is systems

    assert context.get_service(
        "ads"
    ) is systems.ads

    assert context.get_service(
        "analytics"
    ) is systems.analytics


def test_game_systems_supports_mock_ads_without_real_network_sdk():
    systems = GameSystems(
        ads=MockAdProvider()
    )

    systems.initialize()

    assert systems.ads_available(
        AdType.REWARDED,
        "revive",
    )

    rewards = []

    result = systems.show_rewarded(
        "revive",
        on_reward=lambda: rewards.append(
            "revived"
        ),
    )

    assert result.success
    assert result.reward_granted
    assert rewards == [
        "revived"
    ]


def test_game_systems_progression_helpers_emit_analytics():
    provider = MockAnalyticsProvider()

    systems = GameSystems(
        analytics=provider
    )

    systems.add_coins(10)
    systems.add_xp(50)
    systems.advance_level()

    assert systems.progression.as_dict() == {
        "level": 2,
        "xp": 50,
        "coins": 10,
    }

    assert [
        event.name
        for event in provider.events
    ] == [
        "progression_updated",
        "progression_updated",
        "progression_updated",
    ]


def test_game_systems_game_event_helpers_emit_analytics():
    provider = MockAnalyticsProvider()
    systems = GameSystems(
        analytics=provider
    )

    systems.game_start(
        mode="endless"
    )

    systems.level_start()

    systems.record_score(
        75,
        high_score=100,
    )

    systems.level_complete(
        score=75,
        duration=8.0,
    )

    systems.game_over(
        score=75,
        high_score=100,
        reason="collision",
    )

    assert [
        event.name
        for event in provider.events
    ] == [
        "game_start",
        "level_start",
        "score_recorded",
        "level_complete",
        "game_over",
    ]


def test_runtime_initializes_services_and_closes_session():
    context = create_context()
    analytics = MockAnalyticsProvider()
    ads = MockAdProvider()

    systems = GameSystems(
        analytics=analytics,
        ads=ads,
    )

    systems.attach(context)

    start_runtime(context)

    assert systems.analytics.initialized
    assert systems.ads.initialized
    assert systems.session.current is not None

    stop_runtime(context)

    assert systems.session.current.ended
    assert analytics.flush_count == 1
