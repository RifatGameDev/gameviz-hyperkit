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
