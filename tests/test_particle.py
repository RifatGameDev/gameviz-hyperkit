import pytest

from hyperkit import ParticleConfig, ParticleEmitter


class DummyScene:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        return obj


def test_particle_emitter_creates_particles():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    particles = emitter.burst(x=100, y=200, count=5)

    assert len(particles) == 5
    assert len(scene.objects) == 5
    assert len(emitter.particles) == 5


def test_particle_update_removes_expired_particles():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    emitter.burst(x=100, y=200, count=3, lifetime=0.1)

    emitter.update(0.2)

    assert emitter.particles == []

    for obj in scene.objects:
        assert obj.active is False
        assert obj.visible is False


def test_particle_config_emits_particles():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    config = ParticleConfig(
        count=4,
        color=(1, 0, 0, 1),
        lifetime=0.5,
    )

    particles = emitter.emit_config(x=300, y=400, config=config)

    assert len(particles) == 4
    assert len(scene.objects) == 4
    assert scene.objects[0].color == (1, 0, 0, 1)


def test_particle_clear_disables_particles():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    emitter.burst(x=100, y=200, count=2)
    emitter.clear()

    assert emitter.particles == []

    for obj in scene.objects:
        assert obj.active is False
        assert obj.visible is False



def test_particle_config_validates_ranges():
    with pytest.raises(
        ValueError,
        match="count",
    ):
        ParticleConfig(
            count=-1
        )

    with pytest.raises(
        ValueError,
        match="speed",
    ):
        ParticleConfig(
            min_speed=200,
            max_speed=100,
        )

    with pytest.raises(
        ValueError,
        match="size",
    ):
        ParticleConfig(
            min_size=0,
        )

    with pytest.raises(
        ValueError,
        match="lifetime",
    ):
        ParticleConfig(
            lifetime=0,
        )


def test_particle_reports_age_and_progress():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    particle = emitter.burst(
        x=0,
        y=0,
        count=1,
        lifetime=2.0,
    )[0]

    particle.update(0.5)

    assert particle.age == pytest.approx(0.5)
    assert particle.progress == pytest.approx(0.25)


def test_particle_rejects_negative_dt():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    particle = emitter.burst(
        x=0,
        y=0,
        count=1,
    )[0]

    with pytest.raises(
        ValueError,
        match="dt",
    ):
        particle.update(-0.1)


def test_particle_emitter_requires_scene_add_method():
    with pytest.raises(
        ValueError,
        match="add",
    ):
        ParticleEmitter(object())


def test_particle_emitter_reports_active_count():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    emitter.burst(
        x=0,
        y=0,
        count=3,
    )

    assert emitter.active_count == 3

    emitter.update(1.0)

    assert emitter.active_count == 0


def test_particle_emitter_clear_returns_removed_count():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    emitter.burst(
        x=0,
        y=0,
        count=4,
    )

    assert emitter.clear() == 4
    assert emitter.active_count == 0


def test_particle_config_respects_fade_flag():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    config = ParticleConfig(
        count=1,
        lifetime=1.0,
        fade=False,
    )

    particle = emitter.emit_config(
        x=0,
        y=0,
        config=config,
    )[0]

    original_alpha = particle.obj.color[3]

    particle.update(0.5)

    assert particle.obj.color[3] == original_alpha


def test_particle_emitter_rejects_negative_dt():
    scene = DummyScene()
    emitter = ParticleEmitter(scene)

    with pytest.raises(
        ValueError,
        match="dt",
    ):
        emitter.update(-0.1)
