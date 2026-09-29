from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .bounds import Bounds


@dataclass
class CameraFollow:
    """Camera target-follow helper with optional world clamping.

    It follows a target object by setting:

    - scene.camera_follow_offset_x
    - scene.camera_follow_offset_y

    The renderer combines this offset with camera shake.
    """

    scene: Any
    target: Any | None
    screen_width: float = 720
    screen_height: float = 1280
    smoothness: float = 8.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    enabled: bool = True
    world_bounds: Bounds | None = None

    def __post_init__(
        self,
    ) -> None:
        self.screen_width = float(
            self.screen_width
        )
        self.screen_height = float(
            self.screen_height
        )
        self.smoothness = float(
            self.smoothness
        )
        self.offset_x = float(
            self.offset_x
        )
        self.offset_y = float(
            self.offset_y
        )

        if self.screen_width <= 0:
            raise ValueError(
                "screen_width must be greater than zero"
            )
        if self.screen_height <= 0:
            raise ValueError(
                "screen_height must be greater than zero"
            )

        self.current_x = 0.0
        self.current_y = 0.0
        self._apply_offset(
            0.0,
            0.0,
        )

    def set_target(
        self,
        target: Any | None,
    ) -> "CameraFollow":
        self.target = target
        return self

    def set_world_bounds(
        self,
        bounds: Bounds | None,
    ) -> "CameraFollow":
        self.world_bounds = bounds
        return self

    def snap_to_target(
        self,
    ) -> tuple[float, float]:
        if self.target is None:
            self.current_x = 0.0
            self.current_y = 0.0
        else:
            (
                self.current_x,
                self.current_y,
            ) = self._desired_offset()

        self._apply_offset(
            self.current_x,
            self.current_y,
        )

        return (
            self.current_x,
            self.current_y,
        )

    def update(
        self,
        dt: float,
    ) -> tuple[float, float]:
        dt = float(
            dt
        )

        if dt < 0:
            raise ValueError(
                "dt must be non-negative"
            )

        if (
            not self.enabled
            or self.target is None
        ):
            self.current_x = 0.0
            self.current_y = 0.0
            self._apply_offset(
                0.0,
                0.0,
            )
            return (
                0.0,
                0.0,
            )

        (
            desired_x,
            desired_y,
        ) = self._desired_offset()

        if self.smoothness <= 0:
            self.current_x = (
                desired_x
            )
            self.current_y = (
                desired_y
            )
        else:
            t = min(
                1.0,
                self.smoothness
                * dt,
            )

            self.current_x += (
                desired_x
                - self.current_x
            ) * t

            self.current_y += (
                desired_y
                - self.current_y
            ) * t

            (
                self.current_x,
                self.current_y,
            ) = self._clamp_offset(
                self.current_x,
                self.current_y,
            )

        self._apply_offset(
            self.current_x,
            self.current_y,
        )

        return (
            self.current_x,
            self.current_y,
        )

    def stop(
        self,
    ) -> None:
        self.enabled = False
        self.current_x = 0.0
        self.current_y = 0.0
        self._apply_offset(
            0.0,
            0.0,
        )

    def start(
        self,
    ) -> None:
        self.enabled = True

    def _desired_offset(
        self,
    ) -> tuple[float, float]:
        if self.target is None:
            return (
                0.0,
                0.0,
            )

        target_center_x = float(
            self.target.x
            + self.target.width / 2
        )
        target_center_y = float(
            self.target.y
            + self.target.height / 2
        )

        screen_center_x = (
            self.screen_width / 2
            + self.offset_x
        )
        screen_center_y = (
            self.screen_height / 2
            + self.offset_y
        )

        desired_x = (
            screen_center_x
            - target_center_x
        )
        desired_y = (
            screen_center_y
            - target_center_y
        )

        return self._clamp_offset(
            desired_x,
            desired_y,
        )

    def _clamp_offset(
        self,
        x: float,
        y: float,
    ) -> tuple[float, float]:
        bounds = (
            self.world_bounds
        )

        if bounds is None:
            return (
                x,
                y,
            )

        if (
            bounds.width
            <= self.screen_width
        ):
            x = (
                (
                    self.screen_width
                    - bounds.width
                )
                / 2.0
                - bounds.left
            )
        else:
            min_x = (
                self.screen_width
                - bounds.right
            )
            max_x = (
                -bounds.left
            )
            x = max(
                min_x,
                min(
                    x,
                    max_x,
                ),
            )

        if (
            bounds.height
            <= self.screen_height
        ):
            y = (
                (
                    self.screen_height
                    - bounds.height
                )
                / 2.0
                - bounds.bottom
            )
        else:
            min_y = (
                self.screen_height
                - bounds.top
            )
            max_y = (
                -bounds.bottom
            )
            y = max(
                min_y,
                min(
                    y,
                    max_y,
                ),
            )

        return (
            x,
            y,
        )

    def _apply_offset(
        self,
        x: float,
        y: float,
    ) -> None:
        self.scene.camera_follow_offset_x = x
        self.scene.camera_follow_offset_y = y
