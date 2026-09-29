from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .geometry import Rect, Vector2


@dataclass
class Bounds:
    """Rectangle bounds helper for screen or world limits."""

    x: float = 0
    y: float = 0
    width: float = 720
    height: float = 1280

    def __post_init__(self) -> None:
        self.x = float(self.x)
        self.y = float(self.y)
        self.width = float(self.width)
        self.height = float(self.height)

        if self.width < 0:
            raise ValueError(
                "Bounds width must be non-negative"
            )
        if self.height < 0:
            raise ValueError(
                "Bounds height must be non-negative"
            )

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
    def center_x(self) -> float:
        return (
            self.x
            + self.width / 2
        )

    @property
    def center_y(self) -> float:
        return (
            self.y
            + self.height / 2
        )

    @property
    def center(self) -> Vector2:
        return Vector2(
            self.center_x,
            self.center_y,
        )

    @property
    def rect(self) -> Rect:
        return Rect(
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def contains_point(
        self,
        x: float,
        y: float,
    ) -> bool:
        return self.rect.contains(
            x,
            y,
        )

    def contains_rect(
        self,
        rect: Rect,
    ) -> bool:
        return (
            rect.left >= self.left
            and rect.right <= self.right
            and rect.bottom >= self.bottom
            and rect.top <= self.top
        )

    def intersects_rect(
        self,
        rect: Rect,
    ) -> bool:
        return not (
            rect.right < self.left
            or rect.left > self.right
            or rect.top < self.bottom
            or rect.bottom > self.top
        )

    def contains_object(
        self,
        obj: Any,
    ) -> bool:
        return self.contains_rect(
            Rect(
                float(obj.x),
                float(obj.y),
                float(obj.width),
                float(obj.height),
            )
        )

    def intersects_object(
        self,
        obj: Any,
    ) -> bool:
        return self.intersects_rect(
            Rect(
                float(obj.x),
                float(obj.y),
                float(obj.width),
                float(obj.height),
            )
        )

    def is_outside(
        self,
        obj: Any,
    ) -> bool:
        return not self.intersects_object(
            obj
        )

    def clamp_x(
        self,
        x: float,
        width: float = 0,
    ) -> float:
        max_x = (
            self.right
            - max(
                0.0,
                float(width),
            )
        )

        if max_x < self.left:
            return self.left

        return max(
            self.left,
            min(
                float(x),
                max_x,
            ),
        )

    def clamp_y(
        self,
        y: float,
        height: float = 0,
    ) -> float:
        max_y = (
            self.top
            - max(
                0.0,
                float(height),
            )
        )

        if max_y < self.bottom:
            return self.bottom

        return max(
            self.bottom,
            min(
                float(y),
                max_y,
            ),
        )

    def clamp_point(
        self,
        x: float,
        y: float,
    ) -> Vector2:
        return Vector2(
            max(
                self.left,
                min(
                    float(x),
                    self.right,
                ),
            ),
            max(
                self.bottom,
                min(
                    float(y),
                    self.top,
                ),
            ),
        )

    def clamp_object(
        self,
        obj: Any,
    ) -> Any:
        """Keep an object fully inside the bounds."""

        obj.x = self.clamp_x(
            obj.x,
            obj.width,
        )
        obj.y = self.clamp_y(
            obj.y,
            obj.height,
        )

        return obj

    def wrap_object(
        self,
        obj: Any,
    ) -> Any:
        """Wrap an object to the other side when it leaves the bounds."""

        if obj.x > self.right:
            obj.x = (
                self.left
                - obj.width
            )
        elif (
            obj.x
            + obj.width
            < self.left
        ):
            obj.x = self.right

        if obj.y > self.top:
            obj.y = (
                self.bottom
                - obj.height
            )
        elif (
            obj.y
            + obj.height
            < self.bottom
        ):
            obj.y = self.top

        return obj

    def bounce_object(
        self,
        obj: Any,
        bounce: float = 1.0,
    ) -> Any:
        """Bounce an object when it hits the bounds."""

        bounce = max(
            0.0,
            float(bounce),
        )

        if obj.x < self.left:
            obj.x = self.left
            obj.vx = (
                abs(obj.vx)
                * bounce
            )

        if (
            obj.x
            + obj.width
            > self.right
        ):
            obj.x = (
                self.right
                - obj.width
            )
            obj.vx = (
                -abs(obj.vx)
                * bounce
            )

        if obj.y < self.bottom:
            obj.y = self.bottom
            obj.vy = (
                abs(obj.vy)
                * bounce
            )

        if (
            obj.y
            + obj.height
            > self.top
        ):
            obj.y = (
                self.top
                - obj.height
            )
            obj.vy = (
                -abs(obj.vy)
                * bounce
            )

        return obj


@dataclass
class ScreenBounds(Bounds):
    """Default screen bounds using HyperKit virtual resolution."""

    def __init__(
        self,
        width: float = 720,
        height: float = 1280,
    ):
        super().__init__(
            x=0,
            y=0,
            width=width,
            height=height,
        )

    @classmethod
    def from_game(
        cls,
        game: Any,
    ) -> "ScreenBounds":
        return cls(
            width=float(
                getattr(
                    game,
                    "width",
                    720,
                )
            ),
            height=float(
                getattr(
                    game,
                    "height",
                    1280,
                )
            ),
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
        self.screen = (
            screen
            or ScreenBounds()
        )
        self.world = (
            world
            or WorldBounds(
                x=0,
                y=0,
                width=self.screen.width,
                height=self.screen.height,
            )
        )

    def keep_on_screen(
        self,
        obj: Any,
    ) -> Any:
        return self.screen.clamp_object(
            obj
        )

    def keep_in_world(
        self,
        obj: Any,
    ) -> Any:
        return self.world.clamp_object(
            obj
        )

    def bounce_on_screen(
        self,
        obj: Any,
        bounce: float = 1.0,
    ) -> Any:
        return self.screen.bounce_object(
            obj,
            bounce=bounce,
        )

    def bounce_in_world(
        self,
        obj: Any,
        bounce: float = 1.0,
    ) -> Any:
        return self.world.bounce_object(
            obj,
            bounce=bounce,
        )

    def wrap_on_screen(
        self,
        obj: Any,
    ) -> Any:
        return self.screen.wrap_object(
            obj
        )

    def wrap_in_world(
        self,
        obj: Any,
    ) -> Any:
        return self.world.wrap_object(
            obj
        )

    def is_outside_screen(
        self,
        obj: Any,
    ) -> bool:
        return self.screen.is_outside(
            obj
        )

    def is_outside_world(
        self,
        obj: Any,
    ) -> bool:
        return self.world.is_outside(
            obj
        )
