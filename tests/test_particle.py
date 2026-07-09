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
