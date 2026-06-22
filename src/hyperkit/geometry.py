from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class Vector2:
    """Small 2D vector helper."""

    x: float = 0.0
    y: float = 0.0

    def copy(self) -> "Vector2":
        return Vector2(self.x, self.y)

    def distance_to(self, other: "Vector2") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx * dx + dy * dy)

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y


@dataclass
class Rect:
    """Axis-aligned rectangle for simple collision and hit testing."""

    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y

    @property
    def top(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Vector2:
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)

    def contains(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.bottom <= y <= self.top


@dataclass
class Circle:
    """Circle helper for simple collision."""

    x: float
    y: float
    radius: float

    @property
    def center(self) -> Vector2:
        return Vector2(self.x, self.y)
