from hyperkit import GameObject


def test_game_object_can_store_image_path():
    obj = GameObject(image_path="assets/images/player.png")

    assert obj.image_path == "assets/images/player.png"
    assert obj.has_image()


def test_game_object_without_image_returns_false():
    obj = GameObject()

    assert obj.image_path is None
    assert not obj.has_image()


def test_game_object_set_image_updates_image_path():
    obj = GameObject()

    obj.set_image("assets/images/enemy.png")

    assert obj.image_path == "assets/images/enemy.png"
    assert obj.has_image()


def test_game_object_can_clear_image():
    obj = GameObject(image_path="assets/images/player.png")

    obj.set_image(None)

    assert obj.image_path is None
    assert not obj.has_image()
