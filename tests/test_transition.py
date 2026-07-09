from hyperkit import Scene, SceneTransition


class DummyGame:
    width = 720
    height = 1280

    def __init__(self):
        self.changed_scene = None

    def change_scene(self, scene):
        self.changed_scene = scene


class DummyScene(Scene):
    def start(self):
        pass


def test_scene_transition_creates_overlay():
    scene = DummyScene()
    scene.bind_game(DummyGame())

    transition = SceneTransition(scene)

    assert transition.overlay is not None
    assert transition.overlay in scene.objects
    assert transition.overlay.name == "scene_transition_overlay"


def test_scene_transition_fade_in_reduces_alpha():
    scene = DummyScene()
    scene.bind_game(DummyGame())

    transition = SceneTransition(scene)
    transition.fade_in(duration=1.0)

    assert transition.overlay.color[3] == 1.0

    transition.update(0.5)

    assert transition.overlay.color[3] == 0.5

    transition.update(0.5)

    assert transition.overlay.color[3] == 0.0
    assert not transition.is_running()


def test_scene_transition_fade_out_increases_alpha():
    scene = DummyScene()
    scene.bind_game(DummyGame())

    transition = SceneTransition(scene)
    transition.fade_out(duration=1.0)

    assert transition.overlay.color[3] == 0.0

    transition.update(0.5)

    assert transition.overlay.color[3] == 0.5

    transition.update(0.5)

    assert transition.overlay.color[3] == 1.0
    assert not transition.is_running()


def test_scene_transition_calls_callback_after_complete():
    scene = DummyScene()
    scene.bind_game(DummyGame())

    completed = {"value": False}

    transition = SceneTransition(scene)
    transition.fade_out(
        duration=0.2, on_complete=lambda: completed.update(value=True))
    transition.update(0.2)

    assert completed["value"] is True


def test_scene_transition_fade_to_scene_changes_scene():
    game = DummyGame()

    scene = DummyScene()
    scene.bind_game(game)

    next_scene = DummyScene()

    transition = SceneTransition(scene)
    transition.fade_to_scene(next_scene, duration=0.2)
    transition.update(0.2)

    assert game.changed_scene is next_scene
