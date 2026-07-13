from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Bounds:
    """Rectangle bounds helper for screen or world limits."""

    x: float = 0
    y: float = 0
    width: float = 720
    height: float = 1280

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
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def contains_point(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    def contains_object(self, obj: Any) -> bool:
        return (
            obj.x >= self.left
            and obj.y >= self.bottom
            and obj.x + obj.width <= self.right
            and obj.y + obj.height <= self.top
        )

    def intersects_object(self, obj: Any) -> bool:
        return not (
            obj.x + obj.width < self.left
            or obj.x > self.right
            or obj.y + obj.height < self.bottom
            or obj.y > self.top
        )

    def is_outside(self, obj: Any) -> bool:
        return not self.intersects_object(obj)

    def clamp_x(self, x: float, width: float = 0) -> float:
        return max(self.left, min(x, self.right - width))

    def clamp_y(self, y: float, height: float = 0) -> float:
        return max(self.bottom, min(y, self.top - height))

    def clamp_object(self, obj: Any) -> Any:
        """Keep an object fully inside the bounds."""
        obj.x = self.clamp_x(obj.x, obj.width)
        obj.y = self.clamp_y(obj.y, obj.height)
        return obj

    def wrap_object(self, obj: Any) -> Any:
        """Wrap an object to the other side when it leaves the bounds."""
        if obj.x > self.right:
            obj.x = self.left - obj.width
        elif obj.x + obj.width < self.left:
            obj.x = self.right

        if obj.y > self.top:
            obj.y = self.bottom - obj.height
        elif obj.y + obj.height < self.bottom:
            obj.y = self.top

        return obj

    def bounce_object(self, obj: Any, bounce: float = 1.0) -> Any:
        """Bounce an object when it hits the bounds."""
        bounce = max(0.0, float(bounce))

        if obj.x < self.left:
            obj.x = self.left
            obj.vx = abs(obj.vx) * bounce

        if obj.x + obj.width > self.right:
            obj.x = self.right - obj.width
            obj.vx = -abs(obj.vx) * bounce

        if obj.y < self.bottom:
            obj.y = self.bottom
            obj.vy = abs(obj.vy) * bounce

        if obj.y + obj.height > self.top:
            obj.y = self.top - obj.height
            obj.vy = -abs(obj.vy) * bounce

        return obj


@dataclass
class ScreenBounds(Bounds):
    """Default screen bounds using HyperKit virtual resolution."""

    def __init__(self, width: float = 720, height: float = 1280):
        super().__init__(x=0, y=0, width=width, height=height)

    @classmethod
    def from_game(cls, game: Any) -> "ScreenBounds":
        return cls(
            width=float(getattr(game, "width", 720)),
            height=float(getattr(game, "height", 1280)),
        )


@dataclass
class WorldBounds(Bounds):
    """World bounds helper.

    World bounds can be larger than the screen.
    """

    pass


class BoundsManager:
    """Manage screen and world bounds together."""

    def __init__(
        self,
        screen: ScreenBounds | None = None,
        world: WorldBounds | None = None,
    ) -> None:
        self.screen = screen or ScreenBounds()
        self.world = world or WorldBounds(
            x=0,
            y=0,
            width=self.screen.width,
            height=self.screen.height,
        )

    def keep_on_screen(self, obj: Any) -> Any:
        return self.screen.clamp_object(obj)

    def keep_in_world(self, obj: Any) -> Any:
        return self.world.clamp_object(obj)

    def bounce_on_screen(self, obj: Any, bounce: float = 1.0) -> Any:
        return self.screen.bounce_object(obj, bounce=bounce)

    def bounce_in_world(self, obj: Any, bounce: float = 1.0) -> Any:
        return self.world.bounce_object(obj, bounce=bounce)

    def wrap_on_screen(self, obj: Any) -> Any:
        return self.screen.wrap_object(obj)

    def wrap_in_world(self, obj: Any) -> Any:
        return self.world.wrap_object(obj)

    def is_outside_screen(self, obj: Any) -> bool:
        return self.screen.is_outside(obj)

    def is_outside_world(self, obj: Any) -> bool:
        return self.world.is_outside(obj)
