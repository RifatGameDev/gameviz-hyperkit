import pytest

from hyperkit.analytics import (
    AnalyticsEvent,
    MockAnalyticsProvider,
    NoOpAnalyticsProvider,
)


def test_analytics_event_requires_name():
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        AnalyticsEvent("   ")


def test_noop_analytics_is_safe_without_provider_dependencies():
    provider = NoOpAnalyticsProvider()

    assert provider.initialize().success
    assert provider.track_event(
        AnalyticsEvent("game_start")
    ).success
    assert provider.flush().success


def test_mock_analytics_collects_events():
    provider = MockAnalyticsProvider()

    assert provider.initialize().success

    result = provider.track(
        "level_complete",
        level=3,
        score=120,
    )

    assert result.success
    assert len(provider.events) == 1

    event = provider.events[0]

    assert event.name == "level_complete"
    assert event.properties == {
        "level": 3,
        "score": 120,
    }


def test_mock_analytics_requires_initialization():
    provider = MockAnalyticsProvider()

    result = provider.track_event(
        AnalyticsEvent("game_start")
    )

    assert not result.success
    assert provider.events == []


def test_mock_analytics_flush_tracks_calls():
    provider = MockAnalyticsProvider()
    provider.initialize()

    assert provider.flush().success
    assert provider.flush_count == 1
