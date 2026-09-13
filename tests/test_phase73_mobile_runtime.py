from __future__ import annotations

import pytest

from hyperkit.app import Game
from hyperkit.environment import (
    PlatformKind,
    RuntimeEnvironment,
    detect_wsl,
)
from hyperkit.errors import (
    HyperKitRuntimeError,
)
from hyperkit.input import (
    TouchTracker,
)
from hyperkit.mobile import (
    DisplayOrientation,
    MobileDisplayProfile,
    SafeAreaInsets,
)
from hyperkit.runtime import (
    RuntimeState,
    create_context,
)


def test_safe_area_rejects_negative_values():
    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        SafeAreaInsets(
            top=-1
        )


def test_safe_area_resolves_mobile_viewport():
    profile = MobileDisplayProfile(
        safe_area=SafeAreaInsets(
            left=10,
            right=20,
            top=30,
            bottom=40,
        )
    )

    viewport = profile.resolve_viewport(
        1000,
        2000,
    )

    assert viewport.x == 10
    assert viewport.y == 40
    assert viewport.width == 970
    assert viewport.height == 1930


def test_landscape_swaps_portrait_virtual_size():
    profile = MobileDisplayProfile(
        virtual_width=720,
        virtual_height=1280,
        orientation=(
            DisplayOrientation.LANDSCAPE
        ),
    )

    assert profile.virtual_size == (
        1280,
        720,
    )


def test_portrait_swaps_landscape_virtual_size():
    profile = MobileDisplayProfile(
        virtual_width=1280,
        virtual_height=720,
        orientation=(
            DisplayOrientation.PORTRAIT
        ),
    )

    assert profile.virtual_size == (
        720,
        1280,
    )


def test_fullscreen_defaults_to_mobile():
    profile = MobileDisplayProfile()

    assert profile.resolve_fullscreen(
        is_mobile=True
    )

    assert not profile.resolve_fullscreen(
        is_mobile=False
    )


def test_zero_timestamp_is_preserved():
    tracker = TouchTracker(
        tap_max_duration=1.0
    )

    tracker.touch_down(
        10,
        20,
        timestamp=0.0,
    )

    gesture = tracker.touch_up(
        10,
        20,
        timestamp=0.5,
    )

    assert gesture is not None
    assert gesture.kind == "tap"
    assert gesture.duration == 0.5


def test_multi_touch_pointer_tracking():
    tracker = TouchTracker()

    tracker.touch_down(
        0,
        0,
        timestamp=1.0,
        pointer_id="finger-1",
    )

    tracker.touch_down(
        100,
        100,
        timestamp=1.0,
        pointer_id="finger-2",
    )

    assert tracker.active_touch_count == 2

    first = tracker.touch_up(
        100,
        0,
        timestamp=1.1,
        pointer_id="finger-1",
    )

    assert first is not None
    assert first.kind == "swipe"
    assert first.direction == "right"
    assert first.pointer_id == "finger-1"

    assert tracker.active_touch_count == 1

    second = tracker.touch_up(
        100,
        100,
        timestamp=1.1,
        pointer_id="finger-2",
    )

    assert second is not None
    assert second.kind == "tap"

    assert tracker.active_touch_count == 0


def test_touch_move_position():
    tracker = TouchTracker()

    tracker.touch_down(
        1,
        2,
        timestamp=1.0,
    )

    tracker.touch_move(
        10,
        20,
        timestamp=1.1,
    )

    assert tracker.get_touch_position() == (
        10.0,
        20.0,
    )


def test_mobile_runtime_lifecycle():
    context = create_context()

    assert (
        context.state
        == RuntimeState.CREATED
    )

    context.start()

    assert context.is_running

    context.pause()

    assert context.is_paused
    assert context.is_suspended

    context.background()

    assert context.is_background
    assert context.is_suspended

    context.resume()

    assert context.is_running

    context.stop()

    assert context.is_stopped


def test_runtime_cannot_pause_before_start():
    context = create_context()

    with pytest.raises(
        HyperKitRuntimeError,
        match="only be paused",
    ):
        context.pause()


def test_detect_wsl_from_environment():
    assert detect_wsl(
        environ={
            "WSL_DISTRO_NAME": "Ubuntu",
        },
        release_name="linux",
    )


def test_detect_wsl_from_kernel_release():
    assert detect_wsl(
        environ={},
        release_name=(
            "5.15.153.1-microsoft-standard-WSL2"
        ),
    )


def test_extended_environment_preserves_base_contract():
    environment = RuntimeEnvironment(
        platform=PlatformKind.ANDROID,
        python_version="3.11.0",
        python_implementation="CPython",
        executable="/python",
        machine="arm64",
        system="Linux",
        release="android",
        is_wsl=False,
    )

    stable = environment.to_dict()

    extended = (
        environment.to_extended_dict()
    )

    assert stable == {
        "platform": "android",
        "python_version": "3.11.0",
        "python_implementation": "CPython",
        "executable": "/python",
        "is_android": True,
        "is_mobile": True,
        "is_desktop": False,
    }

    assert extended[
        "machine"
    ] == "arm64"

    assert extended[
        "device_family"
    ] == "mobile"


class DummyScene:
    def __init__(self):
        self.started = False
        self.pause_calls = 0
        self.resume_calls = 0
        self.background_calls = 0
        self.game = None

    def bind_game(
        self,
        game,
    ):
        self.game = game

    def start(
        self,
    ):
        self.started = True

    def on_pause(
        self,
    ):
        self.pause_calls += 1

    def on_resume(
        self,
    ):
        self.resume_calls += 1

    def on_background(
        self,
    ):
        self.background_calls += 1


def test_game_mobile_profile_and_lifecycle():
    game = Game(
        width=720,
        height=1280,
        orientation="landscape",
    )

    scene = DummyScene()

    game.set_scene(
        scene
    )

    assert (
        game.width,
        game.height,
    ) == (
        1280,
        720,
    )

    game.pause()

    assert game.is_paused
    assert scene.pause_calls == 1

    game.background()

    assert game.is_backgrounded
    assert (
        scene.background_calls
        == 1
    )

    game.resume()

    assert not game.is_paused
    assert not game.is_backgrounded
    assert scene.resume_calls == 1
