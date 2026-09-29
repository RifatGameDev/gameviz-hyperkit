from hyperkit import (
    GameObject,
    Scene,
    TouchTracker,
)
from hyperkit.app import Game


class DisposableObject(
    GameObject
):
    def __init__(self):
        super().__init__()
        self.disposed = False

    def dispose(self):
        self.disposed = True


class LifecycleScene(
    Scene
):
    def __init__(self):
        super().__init__()
        self.pause_calls = 0
        self.background_calls = 0
        self.resume_calls = 0
        self.stop_calls = 0

    def start(self):
        self.add(
            DisposableObject()
        )
        self.start_game()

    def on_pause(self):
        self.pause_calls += 1

    def on_background(self):
        self.background_calls += 1

    def on_resume(self):
        self.resume_calls += 1

    def on_stop(self):
        self.stop_calls += 1


def test_touch_move_filter_ignores_noise():
    tracker = TouchTracker(
        move_min_distance=5
    )
    tracker.touch_down(
        0,
        0,
        timestamp=1.0,
    )

    assert tracker.touch_move(
        2,
        2,
        timestamp=1.1,
    ) is None

    event = tracker.touch_move(
        6,
        0,
        timestamp=1.2,
    )

    assert event is not None
    assert (
        tracker.get_touch_position()
        == (6.0, 0.0)
    )


def test_cancel_all_returns_cancelled_pointer_count():
    tracker = TouchTracker()

    tracker.touch_down(
        0,
        0,
        pointer_id="a",
    )
    tracker.touch_down(
        1,
        1,
        pointer_id="b",
    )

    assert tracker.cancel_all() == 2
    assert tracker.active_touch_count == 0


def test_scene_release_resources_disposes_objects():
    scene = Scene()
    obj = scene.add(
        DisposableObject()
    )

    assert (
        scene.release_resources()
        == 1
    )
    assert obj.disposed
    assert scene.objects == []


def test_game_stop_is_idempotent_and_releases_scene():
    game = Game()
    scene = LifecycleScene()
    game.set_scene(
        scene
    )

    scene.started = True
    scene.start()

    obj = scene.objects[0]

    game.stop()
    game.stop()

    assert game.is_stopped
    assert scene.stop_calls == 1
    assert obj.disposed
    assert scene.objects == []


def test_game_scene_transition_releases_previous_scene():
    game = Game()
    first = LifecycleScene()
    second = LifecycleScene()

    game.set_scene(
        first
    )
    first.started = True
    first.start()

    first_obj = first.objects[0]

    game.change_scene(
        second
    )

    assert first.stop_calls == 1
    assert first_obj.disposed
    assert first.objects == []
    assert first.started is False
    assert second.started is True
    assert len(
        second.objects
    ) == 1


def test_game_lifecycle_hooks_remain_idempotent():
    game = Game()
    scene = LifecycleScene()

    game.set_scene(
        scene
    )

    game.pause()
    game.pause()
    game.background()
    game.background()
    game.resume()
    game.resume()

    assert scene.pause_calls == 1
    assert scene.background_calls == 1
    assert scene.resume_calls == 1
