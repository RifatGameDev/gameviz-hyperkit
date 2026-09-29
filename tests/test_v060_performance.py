import math

import pytest

from hyperkit import (
    FixedStepClock,
    FrameTimeController,
    PerformanceMode,
    PerformanceProfile,
)
from hyperkit.app import Game


def test_performance_profiles_cover_mobile_modes():
    battery = PerformanceProfile.from_mode(
        PerformanceMode.BATTERY
    )
    balanced = PerformanceProfile.from_mode(
        "balanced"
    )
    performance = PerformanceProfile.from_mode(
        "performance"
    )

    assert battery.target_fps == 30
    assert balanced.target_fps == 60
    assert performance.target_fps == 60
    assert (
        performance.max_frame_delta
        < balanced.max_frame_delta
    )


def test_performance_profile_rejects_invalid_values():
    with pytest.raises(
        ValueError
    ):
        PerformanceProfile(
            target_fps=0
        )

    with pytest.raises(
        ValueError
    ):
        PerformanceProfile(
            max_frame_delta=0
        )

    with pytest.raises(
        ValueError
    ):
        PerformanceProfile.from_mode(
            "ultra"
        )


def test_frame_time_controller_clamps_hitches():
    profile = PerformanceProfile(
        target_fps=60,
        max_frame_delta=0.1,
    )
    controller = FrameTimeController(
        profile
    )

    assert math.isclose(
        controller.normalize(
            1 / 60
        ),
        1 / 60,
    )

    assert controller.normalize(
        0.5
    ) == 0.1
    assert controller.frame_count == 2
    assert controller.hitch_count == 1
    assert math.isclose(
        controller.clamped_time,
        0.4,
    )


def test_fixed_step_clock_limits_spiral_of_death():
    clock = FixedStepClock(
        step=0.02,
        max_substeps=4,
    )

    steps = clock.advance(
        1.0
    )

    assert steps == 4
    assert clock.dropped_time > 0.8
    assert clock.accumulator < clock.step
    assert 0 <= clock.alpha < 1


def test_fixed_step_clock_accumulates_small_frames():
    clock = FixedStepClock(
        step=0.02,
        max_substeps=4,
    )

    assert clock.advance(
        0.01
    ) == 0
    assert clock.advance(
        0.01
    ) == 1


def test_game_uses_supplied_performance_profile():
    profile = PerformanceProfile.from_mode(
        "battery"
    )

    game = Game(
        performance_profile=profile
    )

    assert game.fps == 30
    assert (
        game.performance_profile
        is profile
    )
    assert (
        game.performance_stats()[
            "target_fps"
        ]
        == 30
    )


def test_game_rejects_negative_touch_move_filter():
    with pytest.raises(
        ValueError
    ):
        Game(
            touch_move_min_distance=-1
        )
