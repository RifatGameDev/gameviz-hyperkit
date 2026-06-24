from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CanvasScaler:
    """Scale a virtual game canvas to the real screen/window size.

    HyperKit games use a virtual resolution, for example 720x1280.
    This scaler maps that virtual resolution into any real window/screen size.

    It uses "fit" scaling, so the game keeps its aspect ratio.
    """

    virtual_width: float = 720
    virtual_height: float = 1280
    actual_width: float = 720
    actual_height: float = 1280

    @property
    def scale(self) -> float:
        if self.virtual_width <= 0 or self.virtual_height <= 0:
            return 1.0

        scale_x = self.actual_width / self.virtual_width
        scale_y = self.actual_height / self.virtual_height
        return min(scale_x, scale_y)

    @property
    def content_width(self) -> float:
        return self.virtual_width * self.scale

    @property
    def content_height(self) -> float:
        return self.virtual_height * self.scale

    @property
    def offset_x(self) -> float:
        return (self.actual_width - self.content_width) / 2

    @property
    def offset_y(self) -> float:
        return (self.actual_height - self.content_height) / 2

    def update_actual_size(self, width: float, height: float) -> None:
        self.actual_width = max(float(width), 1.0)
        self.actual_height = max(float(height), 1.0)

    def to_screen_x(self, x: float) -> float:
        return self.offset_x + x * self.scale

    def to_screen_y(self, y: float) -> float:
        return self.offset_y + y * self.scale

    def to_screen_size(self, value: float) -> float:
        return value * self.scale

    def to_screen_rect(self, x: float, y: float, width: float, height: float) -> tuple[float, float, float, float]:
        return (
            self.to_screen_x(x),
            self.to_screen_y(y),
            self.to_screen_size(width),
            self.to_screen_size(height),
        )

    def to_virtual_x(self, x: float) -> float:
        return (x - self.offset_x) / self.scale

    def to_virtual_y(self, y: float) -> float:
        return (y - self.offset_y) / self.scale

    def to_virtual_point(self, x: float, y: float, clamp: bool = True) -> tuple[float, float]:
        vx = self.to_virtual_x(x)
        vy = self.to_virtual_y(y)

        if clamp:
            vx = max(0.0, min(self.virtual_width, vx))
            vy = max(0.0, min(self.virtual_height, vy))

        return vx, vy
