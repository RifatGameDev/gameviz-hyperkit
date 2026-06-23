import pytest

from hyperkit import GameObject, GameState, Scene, StateMachine


def test_state_machine_default_is_playing():
    state = StateMachine()

    assert state.value == "playing"
    assert state.is_state(GameState.PLAYING)


def test_state_machine_changes_state():
    state = StateMachine()

    state.menu()
    assert state.value == "menu"

    state.start()
    assert state.value == "playing"

    state.pause()
    assert state.value == "paused"

    state.resume()
    assert state.value == "playing"

    state.game_over()
    assert state.value == "game_over"


def test_state_machine_rejects_invalid_state():
    state = StateMachine()

    with pytest.raises(ValueError):
        state.set("invalid_state")


def test_scene_has_state_helpers():
    scene = Scene()

    assert scene.is_playing()

    scene.show_menu()
    assert scene.is_menu()

    scene.start_game()
    assert scene.is_playing()

    scene.pause_game()
    assert scene.is_paused()

    scene.end_game()
    assert scene.is_game_over()


def test_scene_default_object_update_only_when_playing():
    scene = Scene()
    obj = scene.add(GameObject(x=0, y=0, vx=100))

    scene.update(1.0)
    assert obj.x == 100

    scene.pause_game()
    scene.update(1.0)
    assert obj.x == 100

    scene.resume_game()
    scene.update(1.0)
    assert obj.x == 200
