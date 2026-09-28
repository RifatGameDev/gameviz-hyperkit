from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Union

from .geometry import Circle, Rect, Vector2


Collider = Union[Rect, Circle]
_EPSILON = 1e-12


@dataclass(frozen=True)
class CollisionManifold:
    """Detailed result for a 2D collision test.

    ``normal`` points from the first collider toward the second collider.
    ``penetration`` is the minimum overlap distance needed to separate them.
    """

    colliding: bool
    normal: Vector2
    penetration: float

    @classmethod
    def none(cls) -> "CollisionManifold":
        return cls(False, Vector2(), 0.0)

    def inverted(self) -> "CollisionManifold":
        if not self.colliding:
            return self
        return CollisionManifold(
            True,
            Vector2(-self.normal.x, -self.normal.y),
            self.penetration,
        )


def rect_intersects_rect(a: Rect, b: Rect) -> bool:
    """Return True if two axis-aligned rectangles overlap or touch."""

    return not (
        a.right < b.left
        or a.left > b.right
        or a.top < b.bottom
        or a.bottom > b.top
    )


def circle_intersects_circle(a: Circle, b: Circle) -> bool:
    """Return True if two circles overlap or touch."""

    dx = a.x - b.x
    dy = a.y - b.y
    radius = a.radius + b.radius
    return (dx * dx + dy * dy) <= radius * radius


def rect_intersects_circle(rect: Rect, circle: Circle) -> bool:
    """Return True if an axis-aligned rectangle overlaps or touches a circle."""

    closest_x = max(rect.left, min(circle.x, rect.right))
    closest_y = max(rect.bottom, min(circle.y, rect.top))
    dx = circle.x - closest_x
    dy = circle.y - closest_y
    return (dx * dx + dy * dy) <= circle.radius * circle.radius


def circle_intersects_rect(circle: Circle, rect: Rect) -> bool:
    """Circle-first alias of :func:`rect_intersects_circle`."""

    return rect_intersects_circle(rect, circle)


def point_in_circle(x: float, y: float, circle: Circle) -> bool:
    """Return True when a point lies inside or on a circle."""

    dx = x - circle.x
    dy = y - circle.y
    return (dx * dx + dy * dy) <= circle.radius * circle.radius


def rect_collision(a: Rect, b: Rect) -> CollisionManifold:
    """Return the collision manifold for two axis-aligned rectangles."""

    if not rect_intersects_rect(a, b):
        return CollisionManifold.none()

    overlap_x = min(a.right, b.right) - max(a.left, b.left)
    overlap_y = min(a.top, b.top) - max(a.bottom, b.bottom)

    center_a = a.center
    center_b = b.center

    if overlap_x <= overlap_y:
        normal_x = 1.0 if center_b.x >= center_a.x else -1.0
        return CollisionManifold(
            True,
            Vector2(normal_x, 0.0),
            max(0.0, overlap_x),
        )

    normal_y = 1.0 if center_b.y >= center_a.y else -1.0
    return CollisionManifold(
        True,
        Vector2(0.0, normal_y),
        max(0.0, overlap_y),
    )


def circle_collision(a: Circle, b: Circle) -> CollisionManifold:
    """Return the collision manifold for two circles."""

    dx = b.x - a.x
    dy = b.y - a.y
    radius = a.radius + b.radius
    distance_squared = dx * dx + dy * dy

    if distance_squared > radius * radius:
        return CollisionManifold.none()

    if distance_squared <= _EPSILON:
        return CollisionManifold(
            True,
            Vector2(1.0, 0.0),
            max(0.0, radius),
        )

    distance = sqrt(distance_squared)
    return CollisionManifold(
        True,
        Vector2(dx / distance, dy / distance),
        max(0.0, radius - distance),
    )


def rect_circle_collision(rect: Rect, circle: Circle) -> CollisionManifold:
    """Return the collision manifold from ``rect`` toward ``circle``."""

    closest_x = max(rect.left, min(circle.x, rect.right))
    closest_y = max(rect.bottom, min(circle.y, rect.top))

    dx = circle.x - closest_x
    dy = circle.y - closest_y
    distance_squared = dx * dx + dy * dy
    radius_squared = circle.radius * circle.radius

    if distance_squared > radius_squared:
        return CollisionManifold.none()

    if distance_squared > _EPSILON:
        distance = sqrt(distance_squared)
        return CollisionManifold(
            True,
            Vector2(dx / distance, dy / distance),
            max(0.0, circle.radius - distance),
        )

    distances = (
        (circle.x - rect.left, Vector2(-1.0, 0.0)),
        (rect.right - circle.x, Vector2(1.0, 0.0)),
        (circle.y - rect.bottom, Vector2(0.0, -1.0)),
        (rect.top - circle.y, Vector2(0.0, 1.0)),
    )
    distance_to_face, normal = min(
        distances,
        key=lambda item: item[0],
    )

    return CollisionManifold(
        True,
        normal,
        max(0.0, circle.radius + distance_to_face),
    )


def circle_rect_collision(circle: Circle, rect: Rect) -> CollisionManifold:
    """Return the collision manifold from ``circle`` toward ``rect``."""

    return rect_circle_collision(rect, circle).inverted()


def collision_manifold(a: Collider, b: Collider) -> CollisionManifold:
    """Dispatch a detailed collision test for supported collider types."""

    if isinstance(a, Rect) and isinstance(b, Rect):
        return rect_collision(a, b)
    if isinstance(a, Circle) and isinstance(b, Circle):
        return circle_collision(a, b)
    if isinstance(a, Rect) and isinstance(b, Circle):
        return rect_circle_collision(a, b)
    if isinstance(a, Circle) and isinstance(b, Rect):
        return circle_rect_collision(a, b)

    raise TypeError(
        "Unsupported collider pair: "
        f"{type(a).__name__}, {type(b).__name__}"
    )


def intersects(a: Collider, b: Collider) -> bool:
    """Return True when two supported colliders overlap or touch."""

    return collision_manifold(a, b).colliding
