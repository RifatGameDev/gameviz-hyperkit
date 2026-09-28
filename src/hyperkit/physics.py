from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import sqrt
from typing import Callable

from .collision import CollisionManifold, collision_manifold
from .geometry import Circle, Rect, Vector2
from .object import GameObject


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp ``value`` to the inclusive ``minimum``/``maximum`` range."""

    return max(minimum, min(value, maximum))


def move_towards(current: float, target: float, max_delta: float) -> float:
    """Move a scalar toward ``target`` without overshooting."""

    if abs(target - current) <= max_delta:
        return target
    return current + max_delta if target > current else current - max_delta


def apply_gravity(velocity_y: float, gravity: float, dt: float) -> float:
    """Apply constant gravity to vertical velocity."""

    return velocity_y + gravity * dt


def apply_drag(velocity: float, drag: float, dt: float) -> float:
    """Move a scalar velocity toward zero using linear drag."""

    if drag < 0:
        raise ValueError("drag must be non-negative")
    if dt < 0:
        raise ValueError("dt must be non-negative")
    return move_towards(velocity, 0.0, drag * dt)


def reflect_velocity(velocity: float, restitution: float = 1.0) -> float:
    """Reflect a scalar velocity using a restitution value from 0 to 1."""

    return -velocity * clamp(restitution, 0.0, 1.0)


class BodyType(str, Enum):
    """How a physics body participates in simulation."""

    STATIC = "static"
    KINEMATIC = "kinematic"
    DYNAMIC = "dynamic"


@dataclass
class PhysicsMaterial:
    """Simple material properties used by collision resolution."""

    restitution: float = 0.0
    friction: float = 0.0

    def __post_init__(self) -> None:
        self.restitution = clamp(float(self.restitution), 0.0, 1.0)
        self.friction = clamp(float(self.friction), 0.0, 1.0)


CollisionCallback = Callable[
    ["PhysicsBody", CollisionManifold],
    None,
]


@dataclass
class PhysicsBody:
    """Physics component attached to a :class:`GameObject`."""

    obj: GameObject
    body_type: BodyType = BodyType.DYNAMIC
    mass: float = 1.0
    gravity_scale: float = 1.0
    linear_drag: float = 0.0
    material: PhysicsMaterial = field(
        default_factory=PhysicsMaterial
    )
    is_trigger: bool = False
    layer: int = 1
    mask: int = 0xFFFFFFFF
    enabled: bool = True
    on_collision: CollisionCallback | None = None
    on_trigger: CollisionCallback | None = None
    _force: Vector2 = field(
        default_factory=Vector2,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        self.body_type = BodyType(self.body_type)
        self.mass = float(self.mass)
        self.gravity_scale = float(self.gravity_scale)
        self.linear_drag = float(self.linear_drag)

        if self.mass <= 0:
            raise ValueError("mass must be greater than zero")
        if self.linear_drag < 0:
            raise ValueError("linear_drag must be non-negative")
        if self.layer <= 0:
            raise ValueError("layer must be a positive bit mask")
        if self.mask < 0:
            raise ValueError("mask must be non-negative")

    @property
    def inverse_mass(self) -> float:
        if self.body_type is not BodyType.DYNAMIC:
            return 0.0
        return 1.0 / self.mass

    @property
    def velocity(self) -> Vector2:
        return Vector2(self.obj.vx, self.obj.vy)

    @velocity.setter
    def velocity(self, value: Vector2) -> None:
        self.obj.vx = float(value.x)
        self.obj.vy = float(value.y)

    @property
    def speed(self) -> float:
        return sqrt(
            self.obj.vx * self.obj.vx
            + self.obj.vy * self.obj.vy
        )

    @property
    def collider(self) -> Rect | Circle:
        if self.obj.shape == "circle":
            radius = min(
                self.obj.width,
                self.obj.height,
            ) / 2.0
            return Circle(
                self.obj.x + self.obj.width / 2.0,
                self.obj.y + self.obj.height / 2.0,
                radius,
            )

        return self.obj.rect

    def set_velocity(
        self,
        vx: float,
        vy: float,
    ) -> "PhysicsBody":
        self.obj.vx = float(vx)
        self.obj.vy = float(vy)
        return self

    def apply_force(
        self,
        fx: float,
        fy: float,
    ) -> "PhysicsBody":
        """Accumulate a force for the next simulation step."""

        if self.body_type is BodyType.DYNAMIC:
            self._force.x += float(fx)
            self._force.y += float(fy)
        return self

    def apply_impulse(
        self,
        ix: float,
        iy: float,
    ) -> "PhysicsBody":
        """Immediately change velocity using impulse / mass."""

        if self.body_type is BodyType.DYNAMIC:
            self.obj.vx += float(ix) * self.inverse_mass
            self.obj.vy += float(iy) * self.inverse_mass
        return self

    def clear_forces(self) -> None:
        self._force.x = 0.0
        self._force.y = 0.0

    def can_collide_with(
        self,
        other: "PhysicsBody",
    ) -> bool:
        return (
            self.enabled
            and other.enabled
            and self.obj.active
            and other.obj.active
            and bool(self.mask & other.layer)
            and bool(other.mask & self.layer)
        )

    def step(
        self,
        dt: float,
        gravity_y: float,
    ) -> None:
        """Advance this body by one fixed or variable time step."""

        if dt < 0:
            raise ValueError("dt must be non-negative")

        if not self.enabled or not self.obj.active:
            self.clear_forces()
            return

        if self.body_type is BodyType.STATIC:
            self.clear_forces()
            return

        if self.body_type is BodyType.DYNAMIC:
            self.obj.vx += (
                self._force.x * self.inverse_mass
            ) * dt
            self.obj.vy += (
                gravity_y * self.gravity_scale
                + self._force.y * self.inverse_mass
            ) * dt

            if self.linear_drag:
                self.obj.vx = apply_drag(
                    self.obj.vx,
                    self.linear_drag,
                    dt,
                )
                self.obj.vy = apply_drag(
                    self.obj.vy,
                    self.linear_drag,
                    dt,
                )

        self.obj.x += self.obj.vx * dt
        self.obj.y += self.obj.vy * dt
        self.clear_forces()


@dataclass(frozen=True)
class PhysicsCollision:
    """One collision reported during a physics-world step."""

    a: PhysicsBody
    b: PhysicsBody
    manifold: CollisionManifold
    is_trigger: bool


class PhysicsWorld:
    """Small deterministic 2D physics world for HyperKit games.

    The implementation intentionally uses a simple O(n²) pair scan. That is
    appropriate for the small object counts common in HyperKit's mobile
    hypercasual games and keeps the runtime dependency-free.
    """

    def __init__(
        self,
        gravity_y: float = -980.0,
    ) -> None:
        self.gravity_y = float(gravity_y)
        self.bodies: list[PhysicsBody] = []
        self.collisions: list[
            PhysicsCollision
        ] = []

    def add_body(
        self,
        obj: GameObject,
        **kwargs: object,
    ) -> PhysicsBody:
        body = PhysicsBody(
            obj=obj,
            **kwargs,
        )
        self.bodies.append(body)
        return body

    def remove_body(
        self,
        body: PhysicsBody,
    ) -> None:
        if body in self.bodies:
            self.bodies.remove(body)

    def clear(self) -> None:
        self.bodies.clear()
        self.collisions.clear()

    def get_body(
        self,
        obj: GameObject,
    ) -> PhysicsBody | None:
        for body in self.bodies:
            if body.obj is obj:
                return body
        return None

    def step(
        self,
        dt: float,
    ) -> tuple[PhysicsCollision, ...]:
        if dt < 0:
            raise ValueError("dt must be non-negative")

        self.collisions = []

        for body in self.bodies:
            body.step(
                dt,
                self.gravity_y,
            )

        count = len(self.bodies)
        for index in range(count):
            a = self.bodies[index]

            for other_index in range(
                index + 1,
                count,
            ):
                b = self.bodies[other_index]

                if not a.can_collide_with(b):
                    continue

                manifold = collision_manifold(
                    a.collider,
                    b.collider,
                )

                if not manifold.colliding:
                    continue

                is_trigger = (
                    a.is_trigger
                    or b.is_trigger
                )

                collision = PhysicsCollision(
                    a=a,
                    b=b,
                    manifold=manifold,
                    is_trigger=is_trigger,
                )
                self.collisions.append(
                    collision
                )

                if is_trigger:
                    self._notify_trigger(
                        a,
                        b,
                        manifold,
                    )
                    continue

                self._resolve(
                    a,
                    b,
                    manifold,
                )
                self._notify_collision(
                    a,
                    b,
                    manifold,
                )

        return tuple(self.collisions)

    @staticmethod
    def _notify_collision(
        a: PhysicsBody,
        b: PhysicsBody,
        manifold: CollisionManifold,
    ) -> None:
        if a.on_collision is not None:
            a.on_collision(
                b,
                manifold,
            )
        if b.on_collision is not None:
            b.on_collision(
                a,
                manifold.inverted(),
            )

    @staticmethod
    def _notify_trigger(
        a: PhysicsBody,
        b: PhysicsBody,
        manifold: CollisionManifold,
    ) -> None:
        if a.on_trigger is not None:
            a.on_trigger(
                b,
                manifold,
            )
        if b.on_trigger is not None:
            b.on_trigger(
                a,
                manifold.inverted(),
            )

    @staticmethod
    def _resolve(
        a: PhysicsBody,
        b: PhysicsBody,
        manifold: CollisionManifold,
    ) -> None:
        inv_a = a.inverse_mass
        inv_b = b.inverse_mass
        inv_sum = inv_a + inv_b

        if inv_sum <= 0:
            return

        normal = manifold.normal

        if manifold.penetration > 0:
            correction = (
                manifold.penetration
                / inv_sum
            )
            correction *= 0.8

            a.obj.x -= (
                normal.x
                * correction
                * inv_a
            )
            a.obj.y -= (
                normal.y
                * correction
                * inv_a
            )
            b.obj.x += (
                normal.x
                * correction
                * inv_b
            )
            b.obj.y += (
                normal.y
                * correction
                * inv_b
            )

        relative_x = b.obj.vx - a.obj.vx
        relative_y = b.obj.vy - a.obj.vy
        velocity_along_normal = (
            relative_x * normal.x
            + relative_y * normal.y
        )

        if velocity_along_normal >= 0:
            return

        restitution = min(
            a.material.restitution,
            b.material.restitution,
        )

        impulse_size = (
            -(1.0 + restitution)
            * velocity_along_normal
            / inv_sum
        )

        impulse_x = (
            impulse_size
            * normal.x
        )
        impulse_y = (
            impulse_size
            * normal.y
        )

        a.obj.vx -= impulse_x * inv_a
        a.obj.vy -= impulse_y * inv_a
        b.obj.vx += impulse_x * inv_b
        b.obj.vy += impulse_y * inv_b

        PhysicsWorld._apply_friction(
            a,
            b,
            normal,
            inv_sum,
            impulse_size,
        )

    @staticmethod
    def _apply_friction(
        a: PhysicsBody,
        b: PhysicsBody,
        normal: Vector2,
        inv_sum: float,
        normal_impulse: float,
    ) -> None:
        friction = sqrt(
            a.material.friction
            * b.material.friction
        )

        if friction <= 0:
            return

        relative_x = b.obj.vx - a.obj.vx
        relative_y = b.obj.vy - a.obj.vy

        normal_speed = (
            relative_x * normal.x
            + relative_y * normal.y
        )

        tangent_x = (
            relative_x
            - normal_speed * normal.x
        )
        tangent_y = (
            relative_y
            - normal_speed * normal.y
        )

        tangent_length = sqrt(
            tangent_x * tangent_x
            + tangent_y * tangent_y
        )

        if tangent_length <= 1e-12:
            return

        tangent_x /= tangent_length
        tangent_y /= tangent_length

        tangent_speed = (
            relative_x * tangent_x
            + relative_y * tangent_y
        )

        friction_impulse = (
            -tangent_speed
            / inv_sum
        )

        max_friction = (
            normal_impulse
            * friction
        )
        friction_impulse = clamp(
            friction_impulse,
            -max_friction,
            max_friction,
        )

        impulse_x = (
            friction_impulse
            * tangent_x
        )
        impulse_y = (
            friction_impulse
            * tangent_y
        )

        a.obj.vx -= (
            impulse_x
            * a.inverse_mass
        )
        a.obj.vy -= (
            impulse_y
            * a.inverse_mass
        )
        b.obj.vx += (
            impulse_x
            * b.inverse_mass
        )
        b.obj.vy += (
            impulse_y
            * b.inverse_mass
        )
