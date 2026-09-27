import pytest

from hyperkit.analytics import (
    AnalyticsService,
    MockAnalyticsProvider,
    NoOpAnalyticsProvider,
)
from hyperkit.errors import HyperKitRuntimeError
from hyperkit.runtime import create_context


def test_analytics_service_defaults_to_noop_provider():
    analytics = AnalyticsService()

    result = analytics.game_start(
        mode="endless"
    )

    assert analytics.initialized
    assert analytics.provider_name == "noop"
    assert result.success


def test_analytics_service_tracks_common_game_events():
    provider = MockAnalyticsProvider()
    analytics = AnalyticsService(
        provider
    )

    analytics.game_start(
        mode="runner"
    )

    analytics.level_start(
        2
    )

    analytics.level_complete(
        2,
        score=150,
        duration=12.5,
    )

    analytics.game_over(
        score=150,
        high_score=200,
        reason="obstacle",
    )

    names = [
        event.name
        for event in provider.events
    ]

    assert names == [
        "game_start",
        "level_start",
        "level_complete",
        "game_over",
    ]

    assert (
        provider.events[2]
        .properties
    ) == {
        "level": 2,
        "score": 150,
        "duration": 12.5,
    }


def test_analytics_service_score_and_progression_helpers():
    provider = MockAnalyticsProvider()
    analytics = AnalyticsService(
        provider
    )

    analytics.score(
        90,
        high_score=100,
    )

    analytics.progression(
        level=3,
        xp=450,
        coins=25,
    )

    assert (
        provider.events[0]
        .properties
    ) == {
        "score": 90,
        "high_score": 100,
    }

    assert (
        provider.events[1]
        .properties
    ) == {
        "level": 3,
        "xp": 450,
        "coins": 25,
    }


def test_analytics_service_can_switch_provider():
    analytics = AnalyticsService(
        NoOpAnalyticsProvider()
    )

    analytics.initialize()

    provider = MockAnalyticsProvider()

    analytics.set_provider(
        provider,
        initialize=True,
    )

    analytics.track(
        "custom_event",
        value=7,
    )

    assert analytics.provider_name == "mock"
    assert len(provider.events) == 1


def test_analytics_service_requires_explicit_initialize_when_disabled():
    analytics = AnalyticsService(
        MockAnalyticsProvider(),
        auto_initialize=False,
    )

    with pytest.raises(
        HyperKitRuntimeError,
        match="not initialized",
    ):
        analytics.track(
            "game_start"
        )


def test_analytics_service_attaches_to_context():
    context = create_context()
    analytics = AnalyticsService()

    analytics.attach(context)

    assert context.get_service(
        "analytics"
    ) is analytics
