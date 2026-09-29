from hyperkit import Circle, GameObject, Rect


def test_game_object_can_store_image_path():
    obj = GameObject(
        image_path="assets/images/player.png"
    )

    assert (
        obj.image_path
        == "assets/images/player.png"
    )
    assert obj.has_image()


def test_game_object_without_image_returns_false():
    obj = GameObject()

    assert obj.image_path is None
    assert not obj.has_image()


def test_game_object_set_image_updates_image_path():
    obj = GameObject()

    obj.set_image(
        "assets/images/enemy.png"
    )

    assert (
        obj.image_path
        == "assets/images/enemy.png"
    )
    assert obj.has_image()


def test_game_object_can_clear_image():
    obj = GameObject(
        image_path="assets/images/player.png"
    )

    obj.set_image(None)

    assert obj.image_path is None
    assert not obj.has_image()


def test_rect_object_exposes_rect_collider():
    obj = GameObject(
        x=10,
        y=20,
        width=30,
        height=40,
    )

    assert obj.collider == Rect(
        10,
        20,
        30,
        40,
    )


def test_circle_object_exposes_centered_circle_collider():
    obj = GameObject(
        x=10,
        y=20,
        width=20,
        height=30,
        shape="circle",
    )

    assert obj.collider == Circle(
        20,
        35,
        10,
    )


def test_circle_contains_uses_circle_shape_not_bounding_box():
    obj = GameObject(
        x=0,
        y=0,
        width=10,
        height=10,
        shape="circle",
    )

    assert obj.contains(
        5,
        5,
    )
    assert not obj.contains(
        0,
        0,
    )


def test_game_object_collision_respects_object_shapes():
    circle = GameObject(
        x=0,
        y=0,
        width=10,
        height=10,
        shape="circle",
    )
    corner_rect = GameObject(
        x=9,
        y=9,
        width=2,
        height=2,
    )

    assert circle.rect.contains(
        9,
        9,
    )
    assert not circle.collides_with(
        corner_rect
    )
    assert not corner_rect.collides_with(
        circle
    )
