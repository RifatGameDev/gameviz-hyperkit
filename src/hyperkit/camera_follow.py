from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CameraFollow:
    """Simple camera follow helper.

    It follows a target object by setting:

    - scene.camera_follow_offset_x
    - scene.camera_follow_offset_y

    The renderer combines this with camera shake offset.
    """

    scene: Any
    target: Any
    screen_width: float = 720
    screen_height: float = 1280
    smoothness: float = 8.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    enabled: bool = True

    def __post_init__(self) -> None:
        self.current_x = 0.0
        self.current_y = 0.0
        self._apply_offset(0.0, 0.0)

    def set_target(self, target: Any) -> None:
        self.target = target

    def snap_to_target(self) -> None:
        desired_x, desired_y = self._desired_offset()
        self.current_x = desired_x
        self.current_y = desired_y
        self._apply_offset(self.current_x, self.current_y)

    def update(self, dt: float) -> tuple[float, float]:
        if not self.enabled or self.target is None:
            self._apply_offset(0.0, 0.0)
            return 0.0, 0.0

        desired_x, desired_y = self._desired_offset()

        if self.smoothness <= 0:
            self.current_x = desired_x
            self.current_y = desired_y
        else:
            t = min(1.0, self.smoothness * dt)
            self.current_x += (desired_x - self.current_x) * t
            self.current_y += (desired_y - self.current_y) * t

        self._apply_offset(self.current_x, self.current_y)
        return self.current_x, self.current_y

    def stop(self) -> None:
        self.enabled = False
        self.current_x = 0.0
        self.current_y = 0.0
        self._apply_offset(0.0, 0.0)

    def start(self) -> None:
        self.enabled = True

    def _desired_offset(self) -> tuple[float, float]:
        target_center_x = float(self.target.x + self.target.width / 2)
        target_center_y = float(self.target.y + self.target.height / 2)

        screen_center_x = self.screen_width / 2 + self.offset_x
        screen_center_y = self.screen_height / 2 + self.offset_y

        desired_x = screen_center_x - target_center_x
        desired_y = screen_center_y - target_center_y

        return desired_x, desired_y

    def _apply_offset(self, x: float, y: float) -> None:
        self.scene.camera_follow_offset_x = x
        self.scene.camera_follow_offset_y = y
