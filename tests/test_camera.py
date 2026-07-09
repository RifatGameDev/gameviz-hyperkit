from hyperkit import CameraShake


class DummyScene:
    pass


def test_camera_shake_binds_scene_and_sets_default_offset():
    scene = DummyScene()

    shake = CameraShake(scene)

    assert shake.scene is scene
    assert scene.camera_offset_x == 0.0
    assert scene.camera_offset_y == 0.0


def test_camera_shake_starts():
    scene = DummyScene()
    shake = CameraShake(scene)

    shake.shake(intensity=20, duration=0.5)

    assert shake.active
    assert shake.intensity == 20
    assert shake.duration == 0.5
    assert shake.remaining == 0.5


def test_camera_shake_updates_scene_offset():
    scene = DummyScene()
    shake = CameraShake(scene)

    shake.shake(intensity=20, duration=1.0)
    offset_x, offset_y = shake.update(0.1)

    assert -20 <= offset_x <= 20
    assert -20 <= offset_y <= 20
    assert scene.camera_offset_x == offset_x
    assert scene.camera_offset_y == offset_y


def test_camera_shake_stops_after_duration():
    scene = DummyScene()
    shake = CameraShake(scene)

    shake.shake(intensity=20, duration=0.2)
    shake.update(0.3)

    assert not shake.active
    assert scene.camera_offset_x == 0.0
    assert scene.camera_offset_y == 0.0


def test_camera_shake_stop_resets_offset():
    scene = DummyScene()
    shake = CameraShake(scene)

    shake.shake(intensity=20, duration=1.0)
    shake.update(0.1)
    shake.stop()

    assert not shake.active
    assert scene.camera_offset_x == 0.0
    assert scene.camera_offset_y == 0.0
