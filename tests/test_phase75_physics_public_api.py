from pathlib import Path

import hyperkit


PHYSICS_PUBLIC_NAMES = {
    "BodyType",
    "CollisionManifold",
    "PhysicsBody",
    "PhysicsCollision",
    "PhysicsMaterial",
    "PhysicsWorld",
    "apply_drag",
    "circle_collision",
    "circle_intersects_rect",
    "circle_rect_collision",
    "collision_manifold",
    "intersects",
    "point_in_circle",
    "rect_circle_collision",
    "rect_collision",
    "reflect_velocity",
}


def test_phase75_physics_and_collision_are_public():
    assert PHYSICS_PUBLIC_NAMES <= set(
        hyperkit.__all__
    )

    for name in PHYSICS_PUBLIC_NAMES:
        assert hasattr(
            hyperkit,
            name,
        )


def test_simple_physics_template_uses_physics_world():
    source = Path(
        "src/hyperkit/templates/simple_physics/main.py"
    ).read_text(
        encoding="utf-8"
    )

    compile(
        source,
        "simple_physics/main.py",
        "exec",
    )

    assert "PhysicsWorld" in source
    assert "PhysicsMaterial" in source
    assert "BodyType" in source
    assert "self.physics.step(dt)" in source
    assert "is_trigger=True" in source
    assert "ball_velocity_y" not in source
    assert "ball_velocity_x" not in source
