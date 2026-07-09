from __future__ import annotations

from dataclasses import dataclass
from random import uniform
from typing import Any


@dataclass
class CameraShake:
    """Simple camera shake helper.

    It works by setting these values on the scene:

    - scene.camera_offset_x
    - scene.camera_offset_y

    The HyperKit renderer uses those values to shift the screen while drawing.
    """

    scene: Any | None = None
    intensity: float = 0.0
    duration: float = 0.0
    remaining: float = 0.0
    active: bool = False
    decay: bool = True

    def __post_init__(self) -> None:
        if self.scene is not None:
            self.bind(self.scene)

    def bind(self, scene: Any) -> "CameraShake":
        self.scene = scene
        self._set_offset(0.0, 0.0)
        return self

    def shake(
        self,
        intensity: float = 12.0,
        duration: float = 0.25,
        decay: bool = True,
    ) -> None:
        if duration <= 0:
            self.stop()
            return

        self.intensity = max(0.0, float(intensity))
        self.duration = float(duration)
        self.remaining = float(duration)
        self.decay = decay
        self.active = True

    def update(self, dt: float) -> tuple[float, float]:
        if not self.active:
            return 0.0, 0.0

        self.remaining -= dt

        if self.remaining <= 0:
            self.stop()
            return 0.0, 0.0

        strength = self.intensity

        if self.decay and self.duration > 0:
            strength *= self.remaining / self.duration

        offset_x = uniform(-strength, strength)
        offset_y = uniform(-strength, strength)

        self._set_offset(offset_x, offset_y)

        return offset_x, offset_y

    def stop(self) -> None:
        self.active = False
        self.remaining = 0.0
        self._set_offset(0.0, 0.0)

    def _set_offset(self, x: float, y: float) -> None:
        if self.scene is None:
            return

        self.scene.camera_offset_x = x
        self.scene.camera_offset_y = y
