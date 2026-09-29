import pytest

from hyperkit import (
    Bounds,
    BoundsManager,
    GameObject,
    Rect,
    ScreenBounds,
    Vector2,
    WorldBounds,
)


def test_bounds_contains_point():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )

    assert bounds.contains_point(
        50,
        50,
    )
    assert not bounds.contains_point(
        120,
        50,
    )


def test_bounds_contains_object():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=10,
        y=10,
        width=20,
        height=20,
    )

    assert bounds.contains_object(
        obj
    )


def test_bounds_detects_outside_object():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=150,
        y=150,
        width=20,
        height=20,
    )

    assert bounds.is_outside(
        obj
    )


def test_bounds_clamps_object_inside():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=90,
        y=90,
        width=30,
        height=30,
    )

    bounds.clamp_object(
        obj
    )

    assert obj.x == 70
    assert obj.y == 70


def test_bounds_wraps_object_right_to_left():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=120,
        y=50,
        width=20,
        height=20,
    )

    bounds.wrap_object(
        obj
    )

    assert obj.x == -20


def test_bounds_wraps_object_left_to_right():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=-30,
        y=50,
        width=20,
        height=20,
    )

    bounds.wrap_object(
        obj
    )

    assert obj.x == 100


def test_bounds_bounces_object_on_right_wall():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=90,
        y=50,
        width=20,
        height=20,
        vx=50,
    )

    bounds.bounce_object(
        obj
    )

    assert obj.x == 80
    assert obj.vx == -50


def test_bounds_bounces_object_on_left_wall():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )
    obj = GameObject(
        x=-10,
        y=50,
        width=20,
        height=20,
        vx=-50,
    )

    bounds.bounce_object(
        obj
    )

    assert obj.x == 0
    assert obj.vx == 50


def test_screen_bounds_defaults_to_hyperkit_size():
    screen = ScreenBounds()

    assert screen.width == 720
    assert screen.height == 1280
    assert screen.left == 0
    assert screen.bottom == 0


def test_world_bounds_can_be_larger_than_screen():
    world = WorldBounds(
        x=-500,
        y=-500,
        width=2000,
        height=3000,
    )

    assert world.left == -500
    assert world.right == 1500
    assert world.top == 2500


def test_bounds_manager_keeps_object_in_world():
    manager = BoundsManager(
        screen=ScreenBounds(
            width=720,
            height=1280,
        ),
        world=WorldBounds(
            x=0,
            y=0,
            width=1000,
            height=1600,
        ),
    )

    obj = GameObject(
        x=980,
        y=1590,
        width=100,
        height=100,
    )

    manager.keep_in_world(
        obj
    )

    assert obj.x == 900
    assert obj.y == 1500


def test_bounds_manager_detects_outside_screen():
    manager = BoundsManager(
        screen=ScreenBounds(
            width=720,
            height=1280,
        )
    )
    obj = GameObject(
        x=800,
        y=500,
        width=100,
        height=100,
    )

    assert manager.is_outside_screen(
        obj
    )


def test_bounds_exposes_rect_and_center_helpers():
    bounds = Bounds(
        x=10,
        y=20,
        width=100,
        height=60,
    )

    assert bounds.rect == Rect(
        10,
        20,
        100,
        60,
    )
    assert bounds.center == Vector2(
        60,
        50,
    )


def test_bounds_clamp_point():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )

    assert bounds.clamp_point(
        150,
        -10,
    ) == Vector2(
        100,
        0,
    )


def test_bounds_rect_helpers():
    bounds = Bounds(
        x=0,
        y=0,
        width=100,
        height=100,
    )

    assert bounds.contains_rect(
        Rect(
            10,
            10,
            20,
            20,
        )
    )
    assert bounds.intersects_rect(
        Rect(
            90,
            90,
            20,
            20,
        )
    )
    assert not bounds.intersects_rect(
        Rect(
            150,
            150,
            20,
            20,
        )
    )


def test_bounds_rejects_negative_size():
    with pytest.raises(
        ValueError,
        match="width",
    ):
        Bounds(
            width=-1,
        )

    with pytest.raises(
        ValueError,
        match="height",
    ):
        Bounds(
            height=-1,
        )
