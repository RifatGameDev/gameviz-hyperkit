import pytest

from hyperkit.object import GameObject
from hyperkit.physics import (
    BodyType,
    PhysicsBody,
    PhysicsMaterial,
    PhysicsWorld,
    apply_drag,
    apply_gravity,
    clamp,
    move_towards,
    reflect_velocity,
)


def test_existing_physics_helpers_remain_compatible():
    assert clamp(12, 0, 10) == 10
    assert move_towards(0, 10, 3) == 3
    assert move_towards(9, 10, 3) == 10
    assert apply_gravity(10, -20, 0.5) == 0


def test_drag_and_reflection_helpers():
    assert apply_drag(10, 4, 0.5) == 8
    assert apply_drag(-10, 4, 0.5) == -8
    assert reflect_velocity(10, 0.5) == -5


def test_physics_material_clamps_values():
    material = PhysicsMaterial(
        restitution=2,
        friction=-1,
    )

    assert material.restitution == 1
    assert material.friction == 0


def test_dynamic_body_applies_gravity_and_integrates_position():
    obj = GameObject(
        x=0,
        y=0,
        width=10,
        height=10,
    )
    body = PhysicsBody(obj)
    world = PhysicsWorld(gravity_y=-10)
    world.bodies.append(body)

    world.step(1.0)

    assert obj.vy == -10
    assert obj.y == -10


def test_static_body_does_not_move():
    obj = GameObject(
        x=4,
        y=8,
        vx=100,
        vy=100,
    )
    body = PhysicsBody(
        obj,
        body_type=BodyType.STATIC,
    )

    body.step(
        1.0,
        gravity_y=-10,
    )

    assert obj.x == 4
    assert obj.y == 8


def test_impulse_respects_mass():
    obj = GameObject()
    body = PhysicsBody(
        obj,
        mass=2,
    )

    body.apply_impulse(10, 4)

    assert obj.vx == 5
    assert obj.vy == 2


def test_world_resolves_dynamic_body_against_static_body():
    moving = GameObject(
        x=0,
        y=0,
        width=10,
        height=10,
        vx=5,
    )
    wall = GameObject(
        x=8,
        y=0,
        width=10,
        height=10,
    )

    world = PhysicsWorld(gravity_y=0)
    world.add_body(
        moving,
        material=PhysicsMaterial(
            restitution=0,
        ),
    )
    world.add_body(
        wall,
        body_type=BodyType.STATIC,
    )

    collisions = world.step(0)

    assert len(collisions) == 1
    assert collisions[0].is_trigger is False
    assert moving.x < 0
    assert moving.vx == pytest.approx(0)


def test_trigger_reports_collision_without_resolution():
    a = GameObject(
        x=0,
        y=0,
        width=10,
        height=10,
    )
    b = GameObject(
        x=5,
        y=0,
        width=10,
        height=10,
    )

    world = PhysicsWorld(gravity_y=0)
    world.add_body(
        a,
        is_trigger=True,
    )
    world.add_body(
        b,
        body_type=BodyType.STATIC,
    )

    collisions = world.step(0)

    assert len(collisions) == 1
    assert collisions[0].is_trigger is True
    assert a.x == 0
    assert b.x == 5


def test_collision_layer_mask_can_filter_pairs():
    a = GameObject(
        x=0,
        y=0,
        width=10,
        height=10,
    )
    b = GameObject(
        x=5,
        y=0,
        width=10,
        height=10,
    )

    world = PhysicsWorld(gravity_y=0)
    world.add_body(
        a,
        layer=1,
        mask=1,
    )
    world.add_body(
        b,
        layer=2,
        mask=2,
    )

    assert world.step(0) == ()


def test_invalid_body_configuration_is_rejected():
    with pytest.raises(
        ValueError,
        match="mass",
    ):
        PhysicsBody(
            GameObject(),
            mass=0,
        )

    with pytest.raises(
        ValueError,
        match="linear_drag",
    ):
        PhysicsBody(
            GameObject(),
            linear_drag=-1,
        )
