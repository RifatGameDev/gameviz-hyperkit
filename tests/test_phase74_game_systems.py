from hyperkit.analytics import MockAnalyticsProvider
from hyperkit.game_systems import (
    GameSystems,
    ProgressionTracker,
    SessionState,
    SessionTracker,
)
from hyperkit.lifecycle import (
    background_runtime,
    pause_runtime,
    resume_runtime,
    start_runtime,
    stop_runtime,
)
from hyperkit.runtime import create_context


def test_session_tracker_lifecycle():
    times = iter(
        [
            10.0,
            15.0,
        ]
    )

    tracker = SessionTracker(
        time_fn=lambda: next(times),
        id_factory=lambda: "session-1",
    )

    session = tracker.start()

    assert session.session_id == "session-1"
    assert session.state == SessionState.RUNNING

    tracker.pause()
    assert session.state == SessionState.PAUSED

    tracker.resume()
    assert session.state == SessionState.RUNNING

    tracker.end()

    assert session.ended
    assert tracker.duration == 5.0


def test_progression_tracker_updates_common_values():
    progression = ProgressionTracker()

    assert progression.add_xp(25) == 25
    assert progression.add_coins(10) == 10
    assert progression.spend_coins(4)
    assert progression.coins == 6
    assert not progression.spend_coins(100)
    assert progression.advance_level() == 2

    assert progression.as_dict() == {
        "level": 2,
        "xp": 25,
        "coins": 6,
    }


def test_game_systems_can_attach_to_runtime_context():
    context = create_context()
    systems = GameSystems()

    systems.attach(context)

    assert (
        context.get_service("game_systems")
        is systems
    )


def test_runtime_lifecycle_notifies_game_systems():
    context = create_context()
    analytics = MockAnalyticsProvider()

    systems = GameSystems(
        analytics=analytics
    )

    systems.attach(context)

    start_runtime(context)

    assert systems.session.current is not None
    assert (
        systems.session.current.state
        == SessionState.RUNNING
    )

    pause_runtime(context)

    assert (
        systems.session.current.state
        == SessionState.PAUSED
    )

    background_runtime(context)

    assert (
        systems.session.current.state
        == SessionState.BACKGROUND
    )

    resume_runtime(context)

    assert (
        systems.session.current.state
        == SessionState.RUNNING
    )

    stop_runtime(context)

    assert systems.session.current.ended

    names = [
        event.name
        for event in analytics.events
    ]

    assert names == [
        "session_start",
        "session_pause",
        "session_background",
        "session_resume",
        "session_end",
    ]

    assert analytics.flush_count == 1


def test_score_and_progression_hooks_emit_analytics():
    analytics = MockAnalyticsProvider()
    systems = GameSystems(
        analytics=analytics
    )

    systems.record_score(
        80,
        high_score=100,
    )

    systems.progression.add_coins(15)
    systems.progression.add_xp(30)
    systems.record_progression()

    assert [
        event.name
        for event in analytics.events
    ] == [
        "score_recorded",
        "progression_updated",
    ]

    assert analytics.events[0].properties == {
        "score": 80,
        "high_score": 100,
    }

    assert analytics.events[1].properties == {
        "level": 1,
        "xp": 30,
        "coins": 15,
    }



def test_session_tracker_reports_active_state_and_session_id():
    tracker = SessionTracker(
        id_factory=lambda: "session-42",
    )

    assert not tracker.active
    assert tracker.session_id is None

    tracker.start()

    assert tracker.active
    assert tracker.session_id == "session-42"

    tracker.end()

    assert not tracker.active


def test_session_tracker_rejects_empty_session_id():
    tracker = SessionTracker(
        id_factory=lambda: " ",
    )

    try:
        tracker.start()
    except ValueError as exc:
        assert "session_id" in str(exc)
    else:
        raise AssertionError(
            "Expected empty session_id to be rejected."
        )


def test_progression_tracker_reset_is_chainable():
    progression = ProgressionTracker(
        level=3,
        xp=50,
        coins=20,
    )

    result = progression.reset(
        level=2,
        xp=10,
        coins=5,
    )

    assert result is progression
    assert progression.as_dict() == {
        "level": 2,
        "xp": 10,
        "coins": 5,
    }


def test_game_systems_reports_initialization_state():
    systems = GameSystems()

    assert not systems.initialized

    assert systems.initialize() is systems

    assert systems.initialized


def test_game_systems_spend_coins_tracks_only_success():
    analytics = MockAnalyticsProvider()
    systems = GameSystems(
        analytics=analytics
    )

    systems.add_coins(
        10,
        track=False,
    )

    assert systems.spend_coins(4) is True
    assert systems.progression.coins == 6

    assert systems.spend_coins(100) is False
    assert systems.progression.coins == 6

    names = [
        event.name
        for event in analytics.events
    ]

    assert names == [
        "progression_updated",
    ]


def test_game_systems_rejects_invalid_explicit_level():
    systems = GameSystems()

    try:
        systems.level_start(0)
    except ValueError as exc:
        assert "level" in str(exc)
    else:
        raise AssertionError(
            "Expected invalid level_start level."
        )

    try:
        systems.level_complete(-1)
    except ValueError as exc:
        assert "level" in str(exc)
    else:
        raise AssertionError(
            "Expected invalid level_complete level."
        )


def test_record_progression_keeps_tracker_values_authoritative():
    analytics = MockAnalyticsProvider()
    systems = GameSystems(
        analytics=analytics
    )

    systems.progression.reset(
        level=3,
        xp=25,
        coins=7,
    )

    systems.record_progression(
        level=999,
        xp=999,
        coins=999,
        source="test",
    )

    event = analytics.events[-1]

    assert event.properties == {
        "level": 3,
        "xp": 25,
        "coins": 7,
        "source": "test",
    }
