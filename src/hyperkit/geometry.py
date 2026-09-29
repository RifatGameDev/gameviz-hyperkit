from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class Vector2:
    """Dependency-free 2D vector used across HyperKit."""

    x: float = 0.0
    y: float = 0.0

    def copy(self) -> "Vector2":
        return Vector2(
            self.x,
            self.y,
        )

    @property
    def length_squared(self) -> float:
        return (
            self.x * self.x
            + self.y * self.y
        )

    @property
    def length(self) -> float:
        return sqrt(
            self.length_squared
        )

    def normalized(self) -> "Vector2":
        magnitude = self.length

        if magnitude <= 1e-12:
            return Vector2()

        return self / magnitude

    def distance_to(
        self,
        other: "Vector2",
    ) -> float:
        return (
            self - other
        ).length

    def dot(
        self,
        other: "Vector2",
    ) -> float:
        return (
            self.x * other.x
            + self.y * other.y
        )

    def lerp(
        self,
        other: "Vector2",
        amount: float,
    ) -> "Vector2":
        t = max(
            0.0,
            min(
                float(amount),
                1.0,
            ),
        )

        return Vector2(
            self.x
            + (other.x - self.x) * t,
            self.y
            + (other.y - self.y) * t,
        )

    def as_tuple(
        self,
    ) -> tuple[float, float]:
        return (
            self.x,
            self.y,
        )

    def __add__(
        self,
        other: "Vector2",
    ) -> "Vector2":
        if not isinstance(
            other,
            Vector2,
        ):
            return NotImplemented

        return Vector2(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(
        self,
        other: "Vector2",
    ) -> "Vector2":
        if not isinstance(
            other,
            Vector2,
        ):
            return NotImplemented

        return Vector2(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(
        self,
        scalar: float,
    ) -> "Vector2":
        if not isinstance(
            scalar,
            (int, float),
        ):
            return NotImplemented

        return Vector2(
            self.x * scalar,
            self.y * scalar,
        )

    def __rmul__(
        self,
        scalar: float,
    ) -> "Vector2":
        return self * scalar

    def __truediv__(
        self,
        scalar: float,
    ) -> "Vector2":
        value = float(
            scalar
        )

        if value == 0:
            raise ZeroDivisionError(
                "Vector2 cannot be divided by zero"
            )

        return Vector2(
            self.x / value,
            self.y / value,
        )

    def __neg__(
        self,
    ) -> "Vector2":
        return Vector2(
            -self.x,
            -self.y,
        )


@dataclass
class Rect:
    """Axis-aligned rectangle for collision, layout, and hit testing."""

    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return (
            self.x
            + self.width
        )

    @property
    def bottom(self) -> float:
        return self.y

    @property
    def top(self) -> float:
        return (
            self.y
            + self.height
        )

    @property
    def center(self) -> Vector2:
        return Vector2(
            self.x
            + self.width / 2,
            self.y
            + self.height / 2,
        )

    @property
    def size(self) -> Vector2:
        return Vector2(
            self.width,
            self.height,
        )

    @property
    def area(self) -> float:
        return (
            self.width
            * self.height
        )

    def contains(
        self,
        x: float,
        y: float,
    ) -> bool:
        return (
            self.left
            <= x
            <= self.right
            and self.bottom
            <= y
            <= self.top
        )

    def translated(
        self,
        offset: Vector2,
    ) -> "Rect":
        return Rect(
            self.x + offset.x,
            self.y + offset.y,
            self.width,
            self.height,
        )


@dataclass
class Circle:
    """Circle helper for collision and hit testing."""

    x: float
    y: float
    radius: float

    @property
    def center(self) -> Vector2:
        return Vector2(
            self.x,
            self.y,
        )

    @property
    def diameter(self) -> float:
        return (
            self.radius
            * 2.0
        )

    def contains(
        self,
        x: float,
        y: float,
    ) -> bool:
        dx = x - self.x
        dy = y - self.y

        return (
            dx * dx
            + dy * dy
            <= self.radius * self.radius
        )

    def translated(
        self,
        offset: Vector2,
    ) -> "Circle":
        return Circle(
            self.x + offset.x,
            self.y + offset.y,
            self.radius,
        )
