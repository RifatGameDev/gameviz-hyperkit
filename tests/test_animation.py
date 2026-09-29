import pytest

from hyperkit import AnimationManager, GameObject, Tween


def test_tween_animates_numeric_property():
    obj = GameObject(x=0)

    tween = Tween(obj, "x", 100, duration=1.0, easing="linear")

    tween.update(0.5)

    assert obj.x == 50

    tween.update(0.5)

    assert obj.x == 100
    assert tween.completed


def test_animation_manager_removes_completed_tween():
    obj = GameObject(x=0)
    animations = AnimationManager()

    animations.animate(obj, "x", 100, duration=1.0, easing="linear")

    animations.update(1.0)

    assert obj.x == 100
    assert animations.animations == []


def test_animation_manager_move_to_creates_x_and_y_tweens():
    obj = GameObject(x=0, y=0)
    animations = AnimationManager()

    tweens = animations.move_to(
        obj, x=100, y=200, duration=1.0, easing="linear")

    assert len(tweens) == 2

    animations.update(1.0)

    assert obj.x == 100
    assert obj.y == 200


def test_animation_manager_resize_to_animates_size():
    obj = GameObject(width=50, height=50)
    animations = AnimationManager()

    animations.resize_to(obj, width=100, height=150,
                         duration=1.0, easing="linear")
    animations.update(1.0)

    assert obj.width == 100
    assert obj.height == 150


def test_animation_manager_color_to_animates_color():
    obj = GameObject(color=(0, 0, 0, 1))
    animations = AnimationManager()

    animations.color_to(obj, color=(1, 1, 1, 1), duration=1.0, easing="linear")
    animations.update(0.5)

    assert obj.color == (0.5, 0.5, 0.5, 1.0)

    animations.update(0.5)

    assert obj.color == (1.0, 1.0, 1.0, 1.0)


def test_animation_manager_stop_removes_target_animation():
    obj = GameObject(x=0)
    animations = AnimationManager()

    animations.animate(obj, "x", 100, duration=1.0)
    animations.stop(obj, "x")

    assert animations.animations == []


def test_loop_yoyo_animation_continues():
    obj = GameObject(x=0)
    animations = AnimationManager()

    animations.animate(obj, "x", 100, duration=1.0,
                       easing="linear", loop=True, yoyo=True)

    animations.update(1.0)

    assert obj.x == 100
    assert len(animations.animations) == 1

    animations.update(1.0)

    assert obj.x == 0
    assert len(animations.animations) == 1



def test_tween_rejects_negative_delay():
    obj = GameObject()

    with pytest.raises(
        ValueError,
        match="delay",
    ):
        Tween(
            obj,
            "x",
            100,
            duration=1.0,
            delay=-0.1,
        )


def test_tween_rejects_negative_dt():
    obj = GameObject()
    tween = Tween(
        obj,
        "x",
        100,
        duration=1.0,
    )

    with pytest.raises(
        ValueError,
        match="dt",
    ):
        tween.update(-0.1)


def test_tween_delay_uses_only_post_delay_time():
    obj = GameObject(x=0)
    tween = Tween(
        obj,
        "x",
        100,
        duration=1.0,
        easing="linear",
        delay=0.5,
    )

    tween.update(0.75)

    assert obj.x == pytest.approx(25.0)
    assert tween.delay == 0.0


def test_looping_tween_preserves_overshoot():
    obj = GameObject(x=0)
    tween = Tween(
        obj,
        "x",
        100,
        duration=1.0,
        easing="linear",
        loop=True,
    )

    tween.update(1.25)

    assert obj.x == pytest.approx(25.0)
    assert tween.elapsed == pytest.approx(0.25)


def test_tween_stop_is_chainable():
    obj = GameObject()
    tween = Tween(
        obj,
        "x",
        100,
        duration=1.0,
    )

    assert tween.stop() is tween
    assert tween.completed
    assert not tween.active


def test_animation_manager_stop_reports_count():
    obj = GameObject(x=0, y=0)
    animations = AnimationManager()

    animations.animate(
        obj,
        "x",
        100,
    )
    animations.animate(
        obj,
        "y",
        100,
    )

    assert animations.stop(
        obj,
        "x",
    ) == 1
    assert len(
        animations.animations
    ) == 1


def test_animation_manager_clear_reports_count():
    obj = GameObject(x=0, y=0)
    animations = AnimationManager()

    animations.animate(
        obj,
        "x",
        100,
    )
    animations.animate(
        obj,
        "y",
        100,
    )

    assert animations.clear() == 2
    assert animations.animations == []


def test_animation_manager_rejects_negative_dt():
    animations = AnimationManager()

    with pytest.raises(
        ValueError,
        match="dt",
    ):
        animations.update(-0.1)
