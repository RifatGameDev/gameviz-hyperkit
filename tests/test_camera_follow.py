from hyperkit import CameraFollow, GameObject


class DummyScene:
    pass


def test_camera_follow_sets_default_offset():
    scene = DummyScene()
    target = GameObject(x=310, y=590, width=100, height=100)

    follow = CameraFollow(scene=scene, target=target)

    assert scene.camera_follow_offset_x == 0.0
    assert scene.camera_follow_offset_y == 0.0
    assert follow.target is target


def test_camera_follow_centers_target_when_snapped():
    scene = DummyScene()
    target = GameObject(x=0, y=0, width=100, height=100)

    follow = CameraFollow(
        scene=scene,
        target=target,
        screen_width=720,
        screen_height=1280,
    )

    follow.snap_to_target()

    assert scene.camera_follow_offset_x == 310.0
    assert scene.camera_follow_offset_y == 590.0


def test_camera_follow_updates_smoothly():
    scene = DummyScene()
    target = GameObject(x=0, y=0, width=100, height=100)

    follow = CameraFollow(
        scene=scene,
        target=target,
        screen_width=720,
        screen_height=1280,
        smoothness=1.0,
    )

    offset_x, offset_y = follow.update(0.5)

    assert offset_x == 155.0
    assert offset_y == 295.0


def test_camera_follow_no_smoothness_snaps_immediately():
    scene = DummyScene()
    target = GameObject(x=0, y=0, width=100, height=100)

    follow = CameraFollow(
        scene=scene,
        target=target,
        screen_width=720,
        screen_height=1280,
        smoothness=0,
    )

    offset_x, offset_y = follow.update(0.1)

    assert offset_x == 310.0
    assert offset_y == 590.0


def test_camera_follow_stop_resets_offset():
    scene = DummyScene()
    target = GameObject(x=0, y=0, width=100, height=100)

    follow = CameraFollow(scene=scene, target=target)
    follow.snap_to_target()
    follow.stop()

    assert not follow.enabled
    assert scene.camera_follow_offset_x == 0.0
    assert scene.camera_follow_offset_y == 0.0


def test_camera_follow_can_change_target():
    scene = DummyScene()
    target_1 = GameObject(x=0, y=0, width=100, height=100)
    target_2 = GameObject(x=310, y=590, width=100, height=100)

    follow = CameraFollow(scene=scene, target=target_1)
    follow.set_target(target_2)
    follow.snap_to_target()

    assert follow.target is target_2
    assert scene.camera_follow_offset_x == 0.0
    assert scene.camera_follow_offset_y == 0.0
