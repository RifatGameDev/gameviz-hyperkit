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
