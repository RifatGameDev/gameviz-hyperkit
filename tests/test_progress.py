import pytest

from hyperkit import ProgressBar, ProgressBarError


class DummyScene:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        return obj


def test_progress_bar_creates_background_fill_and_label():
    scene = DummyScene()

    bar = ProgressBar(scene=scene, x=10, y=20, width=200, height=30)

    assert bar.background in scene.objects
    assert bar.fill in scene.objects
    assert bar.label in scene.objects
    assert len(scene.objects) == 3


def test_progress_bar_can_hide_text():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        show_text=False,
    )

    assert bar.label is None
    assert len(scene.objects) == 2


def test_progress_bar_sets_fill_width_by_value():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        value=50,
        max_value=100,
    )

    assert bar.progress == 0.5
    assert bar.fill.width == 100


def test_progress_bar_clamps_value_to_max():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        value=150,
        max_value=100,
    )

    assert bar.value == 100
    assert bar.fill.width == 200


def test_progress_bar_clamps_value_to_zero():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        value=-50,
        max_value=100,
    )

    assert bar.value == 0
    assert bar.fill.width == 0


def test_progress_bar_add_and_subtract_value():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        value=50,
        max_value=100,
    )

    bar.add_value(25)
    assert bar.value == 75

    bar.subtract_value(50)
    assert bar.value == 25


def test_progress_bar_updates_label_text():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        value=75,
        max_value=100,
        text_format="{value:.0f}/{max_value:.0f}",
    )

    assert bar.label.text == "75/100"


def test_progress_bar_set_max_value_keeps_percent():
    scene = DummyScene()

    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=200,
        height=30,
        value=50,
        max_value=100,
    )

    bar.set_max_value(200, keep_percent=True)

    assert bar.value == 100
    assert bar.progress == 0.5
    assert bar.fill.width == 100


def test_progress_bar_hide_and_show():
    scene = DummyScene()

    bar = ProgressBar(scene=scene, x=10, y=20, width=200, height=30)

    bar.hide()

    assert not bar.background.visible
    assert not bar.fill.visible
    assert not bar.label.visible

    bar.show()

    assert bar.background.visible
    assert bar.fill.visible
    assert bar.label.visible


def test_progress_bar_rejects_invalid_size():
    scene = DummyScene()

    with pytest.raises(ProgressBarError):
        ProgressBar(scene=scene, x=0, y=0, width=0, height=30)

    with pytest.raises(ProgressBarError):
        ProgressBar(scene=scene, x=0, y=0, width=100, height=0)


def test_progress_bar_rejects_invalid_max_value():
    scene = DummyScene()

    with pytest.raises(ProgressBarError):
        ProgressBar(scene=scene, x=0, y=0, width=100, height=30, max_value=0)



def test_progress_bar_reports_empty_full_and_visible():
    scene = DummyScene()
    bar = ProgressBar(
        scene=scene,
        x=0,
        y=0,
        width=100,
        height=20,
        value=0,
        max_value=100,
    )

    assert bar.is_empty
    assert not bar.is_full
    assert bar.visible

    bar.set_value(100)

    assert not bar.is_empty
    assert bar.is_full


def test_progress_bar_methods_are_chainable():
    scene = DummyScene()
    bar = ProgressBar(
        scene=scene,
        x=0,
        y=0,
        width=100,
        height=20,
    )

    assert bar.set_value(50) is bar
    assert bar.add_value(10) is bar
    assert bar.subtract_value(5) is bar
    assert bar.set_max_value(200) is bar
    assert bar.set_fill_color((1, 0, 0, 1)) is bar
    assert bar.set_background_color((0, 0, 0, 1)) is bar
    assert bar.hide() is bar
    assert bar.show() is bar
    assert bar.set_position(10, 20) is bar


def test_progress_bar_set_size_updates_geometry():
    scene = DummyScene()
    bar = ProgressBar(
        scene=scene,
        x=10,
        y=20,
        width=100,
        height=20,
        value=50,
        max_value=100,
    )

    assert bar.set_size(200, 40) is bar
    assert bar.background.width == 200
    assert bar.background.height == 40
    assert bar.fill.width == 100
    assert bar.fill.height == 40


def test_progress_bar_set_size_rejects_invalid_values():
    scene = DummyScene()
    bar = ProgressBar(
        scene=scene,
        x=0,
        y=0,
        width=100,
        height=20,
    )

    with pytest.raises(ProgressBarError):
        bar.set_size(0, 20)

    with pytest.raises(ProgressBarError):
        bar.set_size(100, 0)


def test_progress_bar_requires_scene_add_method():
    with pytest.raises(
        ProgressBarError,
        match="add",
    ):
        ProgressBar(
            scene=object(),
            x=0,
            y=0,
            width=100,
            height=20,
        )
