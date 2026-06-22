from __future__ import annotations

from math import sqrt

from .geometry import Circle, Rect


def rect_intersects_rect(a: Rect, b: Rect) -> bool:
    """Return True if two axis-aligned rectangles overlap."""

    return not (a.right < b.left or a.left > b.right or a.top < b.bottom or a.bottom > b.top)


def circle_intersects_circle(a: Circle, b: Circle) -> bool:
    """Return True if two circles overlap."""

    dx = a.x - b.x
    dy = a.y - b.y
    return sqrt(dx * dx + dy * dy) <= a.radius + b.radius


def rect_intersects_circle(rect: Rect, circle: Circle) -> bool:
    """Return True if an axis-aligned rectangle overlaps a circle."""

    closest_x = max(rect.left, min(circle.x, rect.right))
    closest_y = max(rect.bottom, min(circle.y, rect.top))
    dx = circle.x - closest_x
    dy = circle.y - closest_y
    return (dx * dx + dy * dy) <= circle.radius * circle.radius
