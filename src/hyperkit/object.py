from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .collision import rect_intersects_rect
from .geometry import Rect, Vector2


@dataclass
class GameObject:
    """A small 2D game object used by HyperKit scenes."""

    x: float = 0.0
    y: float = 0.0
    width: float = 64.0
    height: float = 64.0
    vx: float = 0.0
    vy: float = 0.0
    color: tuple[float, float, float, float] = (1, 1, 1, 1)
    shape: str = "rect"  # rect or circle
    image_path: str | None = None
    active: bool = True
    visible: bool = True
    name: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def position(self) -> Vector2:
        return Vector2(self.x, self.y)

    @position.setter
    def position(self, value: Vector2) -> None:
        self.x = value.x
        self.y = value.y

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.width, self.height)

    @property
    def center(self) -> Vector2:
        return self.rect.center

    def contains(self, x: float, y: float) -> bool:
        return self.rect.contains(x, y)

    def collides_with(self, other: "GameObject") -> bool:
        return rect_intersects_rect(self.rect, other.rect)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def set_image(self, image_path: str | None) -> None:
        self.image_path = image_path

    def has_image(self) -> bool:
        return self.image_path is not None and self.image_path != ""
